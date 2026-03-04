# 3B

## CPU registers

```
C_PC  = 0
C_IR  = 1
C_MAR = 2
C_MDR = 3
C_ACC = 4
C_R0  = 5  General purpose
C_R1  = 6
C_R2  = 7
```

## Instruction set

```
Instruction layout:
  00000000 00000000 00000000
  opcode   r1       r2/immediate
```

Valid registers: `$ac`, `$r0`, `$r1`, `$r2`

### Categories

- `0X` control
- `1X` registers and memory
- `2X` ALU

### Control

```
00 nop
01 die
02 j:   reg1
03 je:  reg1, reg2 = 0?
04 jne: reg1, reg2 != 0?
```

### Registers and Memory

```
10 wr:  reg1 = reg2
11 wri: reg = immediate
12 rm:  reg = mem
13 wm:  mem = reg
14 wmi: mem = immediate
```

### ALU

All results are stored in ALU

```
30 add: reg1 + reg2
31 sub: reg1 - reg2
32 mul: reg1 * reg2
33 and: reg1 & reg2
34 or:  reg1 | reg2
35 xor: reg1 ^ reg2
36 sl:  reg1 << reg2
37 sr:  reg1 >> reg2
38 div: reg1 / reg2
39 mod: reg1 % reg2
3a g:   reg1 > reg2
3b not: !reg
```

### Immediate ALU

All results are stored in ALU

```
40 addi: reg1 + immediate
41 subi: reg1 - immediate
42 muli: reg1 * immediate
43 andi: reg1 & immediate
44 ori:  reg1 | immediate
45 xori: reg1 ^ immediate
46 sli:  reg1 << immediate
47 sri:  reg1 >> immediate
48 divi: reg1 / immediate
49 modi: reg1 % immediate
4a gi:   reg1 > immediate
```