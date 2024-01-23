# Simple Encryptor

> Challenge: [Simple Encryptor](https://app.hackthebox.com/challenges/simple-encryptor)

## Solution
### Analysing code
Decompile the source `encrypt` with `ghidra`:

```C

undefined8 main(void)

{
  int r1;
  time_t timest;
  long in_FS_OFFSET;
  uint seed;
  uint r2;
  long i;
  FILE *inp_file;
  size_t flag_len;
  void *flag;
  FILE *out_file;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  inp_file = fopen("flag","rb");
  fseek(inp_file,0,2);
  flag_len = ftell(inp_file);
  fseek(inp_file,0,0);
  flag = malloc(flag_len);
  fread(flag,flag_len,1,inp_file);
  fclose(inp_file);
  timest = time((time_t *)0x0);
  seed = (uint)timest;
  srand(seed);
  for (i = 0; i < (long)flag_len; i = i + 1) {
    r1 = rand();
    *(byte *)((long)flag + i) = *(byte *)((long)flag + i) ^ (byte)r1;
    r2 = rand();
    r2 = r2 & 7;
    *(byte *)((long)flag + i) =
         *(byte *)((long)flag + i) << (sbyte)r2 | *(byte *)((long)flag + i) >> 8 - (sbyte)r2;
  }
  out_file = fopen("flag.enc","wb");
  fwrite(&seed,1,4,out_file);
  fwrite(flag,1,flag_len,out_file);
  fclose(out_file);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

This code is seperated into these parts:

+ **Read the flag:**
  ```
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  inp_file = fopen("flag","rb");
  fseek(inp_file,0,2);
  flag_len = ftell(inp_file);
  fseek(inp_file,0,0);
  flag = malloc(flag_len);
  fread(flag,flag_len,1,inp_file);
  fclose(inp_file);
  ```
+ **Create the random seed:**
  ```
  timest = time((time_t *)0x0);
  seed = (uint)timest;
  srand(seed);
  ```
+ **Encrypt the flag:**
  ```C
  for (i = 0; i < (long)flag_len; i = i + 1) {
    r1 = rand();
    *(byte *)((long)flag + i) = *(byte *)((long)flag + i) ^ (byte)r1;
    r2 = rand();
    r2 = r2 & 7;
    *(byte *)((long)flag + i) =
         *(byte *)((long)flag + i) << (sbyte)r2 | *(byte *)((long)flag + i) >> 8 - (sbyte)r2;
  }
  ```
  Go through each character of flag, and xor it with `r1` (a random value). Then swap the bits by shifting with `r2` (
  another random value).

  Example: After xor, `flag[i] = flag[i] ^ r1` is `b1|b2|b3|b4|b5|b6|b7|b8` and `r2=3` it becomes:
  
  ```
  flag[i] << r2 => b4|b5|b6|b7|b8|0|0|0
  flag[i] >> (8-r2) => 0|0|0|0|0|b1|b2|b3
  flag[i] << r2 | flag[i] >> (8-r2) => b4|b5|b6|b7|b8|b1|b2|b3
  ```
+ **Print encrypted flag and random seed**:
  ```C
  out_file = fopen("flag.enc","wb");
  fwrite(&seed,1,4,out_file);
  fwrite(flag,1,flag_len,out_file);
  fclose(out_file);
  ```
  Realizing that, the random seed is written to 4-first bytes in output file
### Solution code
[decrypt.c](rev_simpleencryptor/decrypt.c)
```
$ gcc -o decrypt decrypt.c

$ ./decrypt               
Random seed: 1655780698
Flag:
HTB{vRy_s1MplE_F1LE3nCryp0r}
```
Flag: `HTB{vRy_s1MplE_F1LE3nCryp0r}`

  