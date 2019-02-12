#!/usr/bin/env python3
from pwn import *
import binascii

r = remote( 'csie.ctf.tw', 10138 )

user, password = b'A'*5, b'A'*28

## get token
r.sendlineafter( '[>]'  , 'l'       )
r.sendlineafter( ': '   , user      )
r.sendlineafter( ': '   , password  )
token = r.recvuntil('\n\n').strip().decode('utf-8').split(': ')[1].split('\n')[0]

## Leave only the first three blocks
token2 = bytes.fromhex(token)[:48]

## Set b'\xda' to b'\xa0'
token2 = list( token2 )
token2[31] = token2[31]^0xda^0xa0
token2 = binascii.hexlify( bytes(token2) )

## get flag
vc = ''
r.sendlineafter( '[>]'  , 'v'       )
r.sendlineafter( ': '   , token2    )
r.sendlineafter( ': '   , vc        )

r.recvuntil( "Welcome AAAAA\n", drop=True )
print ( r.recvuntil( "\n" ) )
