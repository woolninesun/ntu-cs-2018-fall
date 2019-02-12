#!/usr/bin/env python2
from pwn import *

file = "./fmt2"
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10130

r, context.binary = remote(server, port), file
# ========================================================================
e = ELF(file)

r.interactive()
