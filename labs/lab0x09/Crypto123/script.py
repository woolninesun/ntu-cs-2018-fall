#!/usr/bin/env python3
import sys
from pwn import *

server = 'csie.ctf.tw'

#-- Lab 1 --#

def lab1():
    """    
    use AES.MODE_ECB ==> can Cut and Paste attack

                | 0:32           | 32:64          | 64:96          |
    token1    = |usr=aaaaa&admin=|N...............|................|
    token2    = |usr=aaaaaaaaaaaa|YOOOOOOOOOOOOOOO|&admin=N........|
    faketoken = |usr=aaaaa&admin=|YOOOOOOOOOOOOOOO|YOOOOOOOOOOOOOOO|...
    O = 79 => urlencode unreserved char and (16 * n - 1, n:int)

    unpadding = usr=aaaaa&admin=Y
    """

    r = remote(server, 10136)
    r.recvuntil(    '[*] Environment:\n'                                              )
    print(          '[*] Environment:', r.recvuntil('\n\n').decode("utf-8").rstrip()  )
    r.sendlineafter('[>] Select Labs [1~3]: '                    , '1'                )

    r.recvuntil(    '[?] Available commands: register, login\n'                       )
    r.sendlineafter('[>] '                                       , 'register'         )
    r.sendlineafter('[>] Username: '                             , 'a'*5              )
    r.recvuntil(    '[+] Token: '                                                     )
    token1 = r.recvuntil( '\n' )[:-1]

    r.recvuntil(    '[?] Available commands: register, login\n'                       )
    r.sendlineafter('[>] '                                       , 'register'         )
    r.sendlineafter('[>] Username: '                             , 'a'*12 +'Y'+'O'*15 )
    r.recvuntil(    '[+] Token: '                                                     )
    token2 = r.recvuntil( '\n' )[:-1]

    faketoken = token1[:32] + token2[32:64] * 5
    r.recvuntil(    '[?] Available commands: register, login\n'                       )
    r.sendlineafter('[>] '                                       , 'login'            )
    r.sendlineafter('[>] Token: '                                , faketoken          )
    print( r.recvline().decode("utf-8").rstrip() )

#-- Lab 2 --#

def lab2():
    r = remote(server, 10136)
    r.recvuntil(    '[*] Environment:\n'                                              )
    print(          '[*] Environment:', r.recvuntil('\n\n').decode("utf-8").rstrip()  )
    r.sendlineafter('[>] Select Labs [1~3]: '                    , '2'                )


    r.recvuntil(    '[?] Gimme 2 plaintext with same MAC\n'                           )
    r.sendlineafter('[>] First (hex): '                          , '1e'               )
    r.sendlineafter('[>] Second (hex): '                         , '1e'               )

    print( r.recv() )

#-- Lab 3 --#

def lab3():
    r = remote(server, 10136)
    r.recvuntil(    '[*] Environment:\n'                                              )
    print(          '[*] Environment:', r.recvuntil('\n\n').decode("utf-8").rstrip()  )
    r.sendlineafter('[>] Select Labs [1~3]: '                    , '3'                )

#-- Select Lab --#

def main():
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
