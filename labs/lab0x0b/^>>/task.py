#!/usr/bin/python3 -u

from Crypto.Util.number import getRandomRange
import os


MASK = (1 << 64) - 1
with open('/home/challenge/flag.txt') as f:
    FLAG = f.read().strip()


def xorshift(s):
    s ^= (s & MASK) << 13
    s ^= (s & MASK) >> 7
    s ^= (s & MASK) << 17
    return s & MASK


def main():
    s = getRandomRange(0, (1 << 64))

    r = ''
    for _ in range(200):
        s = xorshift(s)
        if os.urandom(1)[0] >= 128:
            r += str(s & 1)
        else:
            r += '.'
    print(f'[+] Here is the output')
    print(r)
    print('')

    inp = int(input('[>] What is current state? '))
    if inp == s:
        print(f'[+] Flag: {FLAG}')
    else:
        print('[-] Noop')
            

if __name__ == '__main__':
    main()
