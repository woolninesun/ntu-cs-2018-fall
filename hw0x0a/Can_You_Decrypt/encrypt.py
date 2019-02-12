#!/usr/bin/env python3
import json
from Crypto.Util.number import *
from gmpy2 import next_prime
from random import randint

flag = open('flag', 'rb').read()

def genkey():
    while True:
        while True:
            p = 2
            while size(p) < 512:
                p *= getPrime(randint(2, 12))
            if isPrime(p + 1):
                p = p + 1
                break
        r = randint(100, 2 ** 512)
        q1, q2 = int(next_prime(r)), int(next_prime(3 * next_prime(r)))
        n, phi = p * q1 * q2, (p - 1) * (q1 - 1) * (q2 - 1)
        e = 4 * randint(10, 100)
        if GCD(e, phi) == 4:
            return (p, q1, q2, n, e)

p, q1, q2, n, e = genkey()
m = bytes_to_long(flag)
c = pow(m, e, n)

print(json.dumps((n, e, c)))
