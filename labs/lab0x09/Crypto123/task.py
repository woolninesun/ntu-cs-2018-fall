#!/usr/bin/python3 -u

import sys
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long


with open('../flags.txt') as f:
    flags = [l.strip() for l in f]

#-- Common utils --#


def pad(s):
    p = 16 - len(s) % 16
    return s + bytes([p] * p)


def unpad(s):
    return s[:-s[-1]]


#-- Lab 1 --#


def lab1():
    import urllib.parse
    key = os.urandom(32)
    aes = AES.new(key, AES.MODE_ECB)
    while True:
        print(f'[?] Available commands: register, login')
        cmd = input('[>] ')
        if cmd == 'register':
            usr = input('[>] Username: ')
            token = urllib.parse.urlencode({'usr': usr, 'admin': 'N'})
            token = aes.encrypt(pad(token.encode('utf8'))).hex()
            print(f'[+] Token: {token}')
        elif cmd == 'login':
            token = input('[>] Token: ')
            token = unpad(aes.decrypt(bytes.fromhex(token))).decode('utf8')
            token = urllib.parse.parse_qs(token)
            for k, vs in token.items():
                assert(len(vs) == 1)
                token[k] = vs[0]
            if token['admin'][0] == 'Y':
                print(f'[+] {flags[0]}')
            else:
                print(f'[!] Try harder')
            exit(0)
        print('')


#-- Lab 2 --#Gimme 2 


def lab2():
    key = os.urandom(32)
    iv = os.urandom(16)

    def CBC_MAC(s):
        aes = AES.new(key, AES.MODE_CBC, iv)
        rawmac = aes.encrypt(pad(s))[-16:]
        # Encrypt-last-block
        aes = AES.new(key, AES.MODE_ECB)
        mac = aes.encrypt(rawmac).hex().rjust(32, '0')
        return mac

    while True:
        print(f'[?] Gimme 2 plaintext with same MAC')
        m1 = input('[>] First (hex): ')
        m2 = input('[>] Second (hex): ')
        m1, m2 = bytes.fromhex(m1), bytes.fromhex(m2)
        mac1, mac2 = CBC_MAC(m1), CBC_MAC(m2)
        if m1 != m2 and mac1 == mac2:
            print(f'[+] {flags[1]}')
            exit(0)
        elif m1 == m2:
            print(f'[+] Wat ???')
        else:
            print(f'[!] Try harder: {mac1} != {mac2}')
        print('')


#-- Lab 3 --#


def lab3():
    key = os.urandom(32)
    registered = {}

    def getAES(iv=None):
        if iv is None:
            iv = os.urandom(16)
        ctr = Counter.new(128, initial_value=bytes_to_long(iv))
        aes = AES.new(key, AES.MODE_CTR, counter=ctr)
        return aes, iv

    while True:
        print(f'[?] Available commands: register, login')
        cmd = input('[>] ')
        if cmd == 'register':
            assert(len(registered) < 3)
            usr = input('[>] Username (hex): ')
            usr = bytes.fromhex(usr)
            mac = hashlib.md5(b'Crypto is fun' + usr + key).digest()
            aes, iv = getAES()
            token = (iv + aes.encrypt(usr + mac)).hex()
            registered[usr] = 1
            print(f'[+] Token: {token}')
        elif cmd == 'login':
            token = input('[>] Token: ')
            token = bytes.fromhex(token)
            iv, token = token[:16], token[16:]
            aes, iv = getAES(iv)
            token = aes.decrypt(token)
            usr, mac = token[:-16], token[-16:]
            mac2 = hashlib.md5(b'Crypto is fun' + usr + key).digest()
            if mac2 != mac:
                print(f'[!] Invalid mac')
            elif usr not in registered:
                print(f'[+] {flags[2]}')
            else:
                print(f'[!] Try harder')
            exit(0)
        print('')


#-- Select Lab --#


def main():
    print(f'[*] Environment:')
    print(f"Python {sys.version.splitlines()[0]}")
    print(f'')

    try:
        labID = int(input('[>] Select Labs [1~3]: '))
        assert(1 <= labID <= 3)
        lab = eval('lab' + str(labID))
    except (KeyboardInterrupt, EOFError, ConnectionResetError):
        pass
    except:
        print(f'[!] This is not a pwn challenge :)')
    else:
        lab()


if __name__ == '__main__':
    main()
