#!/usr/bin/python3 -u 

import sys
import os
from Crypto.Util.number import getRandomRange
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from phe import paillier


aeskey, aesiv = os.urandom(32), os.urandom(16)
rsa = RSA.generate(1024, e=65537)

f = open('/home/challenge/secret.txt', 'rb')

# p, q are primes
p = int(f.readline())
q = int(f.readline())
# N = p * q
N = 3355606018780219439641525028884199752769801998561640011737388608153379282249382897148298658962575535024085284928972539734583078821643846525056379100313329257692793347640441779084228476012774165371914928109864718335414973965255366726816214172666968247116508581832522056479503720544089865656910596305589
# d = lcm(p - 1, q - 1)
d = int(f.readline())
# u = inverse_mod(d, N)
u = int(f.readline())

N2 = N * N

g = 1
while pow(g, d // 2, N) == 1:
    g = getRandomRange(0, N)

ppub = paillier.PaillierPublicKey(n=N)
ppri = paillier.PaillierPrivateKey(ppub, p, q)


FLAG1 = f.readline().strip()
FLAG2 = f.readline().strip()
assert len(FLAG2) < 24
FLAG2 = FLAG2 + os.urandom(31 - len(FLAG2))
FLAG2 = int.from_bytes(FLAG2, 'little')

f.close()


def aesenc(m):
    aes = AES.new(aeskey, AES.MODE_CBC, aesiv)
    return aes.encrypt(m.to_bytes(2048 // 8, 'little')).hex()


def aesdec(m):
    aes = AES.new(aeskey, AES.MODE_CBC, aesiv)
    m = bytes.fromhex(m)
    assert(len(m) == 2048 // 8)
    return int.from_bytes(aes.decrypt(m), 'little')


def paienc(m):
    assert(m < N)
    m = ppub.raw_encrypt(m)
    return aesenc(m)


def paidec(m):
    m = aesdec(m)
    return ppri.raw_decrypt(m)


def mul():
    A = aesdec(input("[>] What's wrong? "))
    B = aesdec(input("[>] Hmm... "))
    R = aesenc(A * B % N2)
    print(f'[+] The Force will be with you.')
    print(R)


def imul():
    A = paidec(input("[>] What's wrong? "))
    B = int(input("[>] Hmm... "))
    R = paienc(A * B % N)
    print(f'[+] The Force will be with you. Always.')
    print(R)


def POWEEERRR():
    palpatine = paidec(input('[>] Who are you? '))
    force = int(input('[>] How strong do you want to be? '))
    force = rsa.decrypt(force) % N
    palpatine = pow(palpatine, force, N)
    palpatine = paienc(palpatine)
    print('[+] POWAHHHHHHHHHHHH!!!!!!!!!!!!')
    print(palpatine)


def whoru():
    A = paidec(input('[>] Who are you? '))
    B = paidec(input('[>] Who am I? '))
    if A == B:
        print('[+] You were my brother, Anakin.')
    else:
        print('[+] No, I am your father.')


def main():
    print(f'[*] RSA Modulus: {rsa.n}')
    print(f'[*] Paillier Lambda: {rsa.encrypt(d, None)[0]}')
    print(f'[*] N Generator: {g}')
    print(f'[*] Flag2: {paienc(pow(g, FLAG2, N))}')
    print(f'[*] One: {paienc(1)}')
    
    for _ in range(150000):
        cmd = input('[>] Command: ')
        if cmd == 'Abandoned me.':
            print('[+] Goodbye.')
        elif cmd == 'Power! Unlimited power!':
            POWEEERRR()
        elif cmd == 'Help me!':
            mul()
        elif cmd == "You're my only hope!":
            imul()
        elif cmd == 'What happened?':
            whoru()
        elif cmd == str(d):
            print(f"[+] Oh, my dear friend.")
            print(f'[+] Flag1: {FLAG1}')
        else:
            print("[-] What a piece o' junk!")
        print('')


if __name__ == '__main__':
    main()

