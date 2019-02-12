#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *

r = remote( 'csie.ctf.tw', 10140 )
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

def LSB_search( c, e, n, bits ):
    inv = inverse( (2**bits), n ) # 16^-1
    i, m, ri_1 = 0, 0, 0
    while n >> ( i*bits ):
        print(n >> ( i*bits ))
        p = c * pow( inv, i*e, n ) % n
        
        xi = ( menu_decrypt(p) - ri_1 ) % (2**bits)
        m += xi * pow( (2**bits), i )
        ri_1 = ( ( xi + ri_1 )*inv ) % n

        i += 1


    return m

c, e, n = menu_info()

decflag = LSB_search(c, e, n, 4)

print( long_to_bytes(decflag).decode('ascii').rstrip('\x00') )

r.close()
