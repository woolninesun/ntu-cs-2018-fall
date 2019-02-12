#!/usr/bin/env python2
from pwn import *

# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10123

r = remote(server, port)
# ========================================================================

# Sort these 100 numbers for me
# Return the numbers each seperated by a space and ending with a newline.
# For example:
# 1 2 3 4 5

for i in range(100, 0, -1):
    r.recvuntil( str(i) + " times left\n", drop=True )
    a = sorted( r.recvuntil( "\n@" ).split(' ')[:-1], key=int )

    r.sendline( ' '.join(a) )

r.recvuntil( "You're awesome! Here is the flag:\n", drop=True )
print (r.recvline())
