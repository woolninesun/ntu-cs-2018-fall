#!/usr/bin/env python3
import json
from Crypto.Util.number import *
from gmpy2 import iroot
from multiprocessing import Pool

n, e, c = json.loads( open( 'data', 'r' ).read() )

def calc(i):
    print (i)
    decflag, isInt = iroot( c + i * n, e)
    if isInt:
        print( long_to_bytes(decflag).decode('ascii') )
        pool.terminate()
        exit()

pool = Pool(8)

pool.map( calc, range(1000000, 10000000) )
pool.close()
pool.join()
