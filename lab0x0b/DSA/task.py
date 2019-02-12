#!/usr/bin/python3 -u

from hashlib import sha256
from Crypto.PublicKey import DSA
from Crypto.Util.number import getRandomRange, long_to_bytes


DSAkey = DSA.generate(1024)
q = DSAkey.q
k0 = 1
while pow(k0, (q - 1) // 2, q) != q - 1:
    k0 = getRandomRange(1, q)


with open('/home/challenge/flag.txt') as f:
    FLAG = f.read().strip()
MSG = b'GIMME THE FLAG !!!!!!!'
MSG = int.from_bytes(MSG, 'little') % q


def digest(s):
    return sha256(long_to_bytes(s)).digest()
    

def sign(s):
    k = pow(k0, s, q)
    return DSAkey.sign(digest(s), k)


def main():
    print(f'[+] p: {DSAkey.p}')
    print(f'[+] q: {DSAkey.q}')
    print(f'[+] g: {DSAkey.g}')
    print(f'[+] y: {DSAkey.y}')

    while True:
        cmd = input('[>] Command: ')
        if cmd == 'sign':
            msg = input('[>] Message: ')
            msg = int(msg, 16)
            assert(2 < msg < q - 2)
            assert(msg != MSG)
            sig = sign(msg)
            print(f'[+] r: {sig[0]}')
            print(f'[+] s: {sig[1]}')
        elif cmd == 'flag':
            r = int(input('[>] r: '))
            s = int(input('[>] s: '))
            if DSAkey.verify(digest(MSG), (r, s)):
                print(f'[+] Flag: {FLAG}')
            else:
                print(f'[-] Noop')
            exit(0)
        print('')


if __name__ == '__main__':
    main()
