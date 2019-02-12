#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *

r = remote( 'csie.ctf.tw', 10139 )
# r = remote( 'localhost', 9999 )

# ======= menu =======
# 1) info
# 2) decrypt
# > 

def menu_info():
    r.sendlineafter( '> ', '1' )
    return map( lambda raw : int(raw.split()[2]), r.recvlines(3) )

def menu_decrypt( c ):
    r.sendlineafter( '> ', '2' )
    r.sendline( str(c) )
    return int(r.recvline().split()[2])

c, e, n = menu_info()

i, x = 0, 0
while n >> i:
    p = c * pow( (1 << i+1), e, n ) % n
    x = (x << 1) + menu_decrypt(p)
    i += 1
decflag = (x+1) * n // 2 ** i

print( long_to_bytes(decflag).decode('ascii') )

r.close()
