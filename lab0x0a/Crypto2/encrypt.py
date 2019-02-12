#!/usr/bin/env python3
import json
from Crypto.Util.number import *

flag = open('flag', 'rb').read()

def genkeys():
    e = 5
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

pub, priv = genkeys()

n, e = pub

message = b"Let me sleep, just let me sleep. Maybe go to sleep. I want to go to sleep. When can I go to sleep." + flag
m = bytes_to_long(message)
c = pow(m, e, n)

open('data', 'w').write(json.dumps((n, e, c)))
