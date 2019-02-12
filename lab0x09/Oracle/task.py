#!/usr/bin/python3.6 -u

import os
import sys
import msgpack
import traceback
from Crypto.Cipher import AES


IV = os.urandom(16)
key = os.urandom(32)

with open('/home/challenge/flag.txt') as f:
    FLAG = f.read().strip()


def chunk(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]


def encrypt(s):
    size = len(s)
    assert(size >= 16)
    s = s + b'\0' * (-size % 16)
    aes = AES.new(key, AES.MODE_CBC, IV)
    enc = aes.encrypt(s)
    if len(enc) != size:
        blocks = chunk(enc, 16)
        blocks[-2], blocks[-1] = blocks[-1], blocks[-2]
        enc = b''.join(blocks)[:size]
    return enc


def decrypt(s):
    size = len(s)
    assert(size >= 16)
    if size % 16:
        blocks = chunk(s, 16)
        aes = AES.new(key, AES.MODE_ECB)
        tail = aes.decrypt(blocks[-2])[size % 16:]
        blocks[-2], blocks[-1] = blocks[-1] + tail, blocks[-2]
        s = b''.join(blocks)
    aes = AES.new(key, AES.MODE_CBC, IV)
    dec = aes.decrypt(s)
    return dec[:size]


def sendToPhone(usr, pwd, vc):
    raise NotImplementedError('Oops')


def login():
    usr = input('[>] Username: ')
    pwd = input('[>] Password: ')
    vc = os.urandom(20).hex()
    token = {'usr': usr, 'pwd': pwd, 'vc': vc}
    token = msgpack.dumps(token)
    token = encrypt(token).hex()
    print(f'[+] Token: {token}')
    sendToPhone(usr, pwd, vc)


def verify():
    token = input('[>] Token: ')
    vc = input('[>] Verification Code: ')
    token = decrypt(bytes.fromhex(token))
    token = msgpack.loads(token)
    if vc == token[b'vc'].decode('ascii'):
        print(f'[!] No hacking')
    else:
        print(f"Welcome {token[b'usr'].decode('ascii')}")
        print(f"Here's your flag: {FLAG}")
    exit(255)


def main():
    print(f'[*] Environment:')
    print(f"Python {sys.version.splitlines()[0]}")
    print(f"Msgpack {'.'.join(map(str, msgpack.version))}")
    print(f'')

    while True:
        print('[?] l - login')
        print('[?] v - verify')
        print('[?] e - exit')
        
        cmd = input('[>] ')
        try:
            if cmd == 'l':
                login()
            elif cmd == 'v':
                verify()
            elif cmd == 'e':
                print('Bye~')
                exit(0)
            else:
                raise KeyError('Unknown command')
        except Exception as e:
            print(f'[!] {type(e).__name__}')
            # traceback.print_exc()
        print('')


if __name__ == '__main__':
    main()
