#!/usr/bin/env python2
from pwn import *

file = "./migration"
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10131

r, context.binary = remote(server, port), file
# ========================================================================
e = ELF(file)

r.interactive()
