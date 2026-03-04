"""
Simple 24-bit CPU. Named after it's 3 byte long CPU instructions.

- only works on 3 byte-long word memory
- all arithmetic instructions inaccurately take one cycle to complete
- raises VakueError on unknown opcode. Raises Exception on inaccessible memory
  or register access.
"""


# CPU registers
C_PC = 0
C_IR = 1
C_MAR = 2
C_MDR = 3
C_ACC = 4
C_R0 = 5
C_R1 = 6
C_R2 = 7


# Instruction set
# 00000000 00000000 00000000
# opcode   r1       r2/immediate
#
# Valid registers: $ac, $r0, $r1, $r2
#
# Categories
# 0X control
# 1X registers and memory
# 2X ALU
#
# Control
# 00 nop
# 01 die
# 02 j:   reg1
# 03 je:  reg1, reg2 = 0?
# 04 jne: reg1, reg2 != 0?
#
# registers and memory
# 10 wr:  reg1 = reg2
# 11 wri: reg = immediate
# 12 rm:  reg = mem
# 13 wm:  mem = reg
# 14 wmi: mem = immediate
#
# ALU, all results are stored in ALU
# 30 add: reg1 + reg2
# 31 sub: reg1 - reg2
# 32 mul: reg1 * reg2
# 33 and: reg1 & reg2
# 34 or:  reg1 | reg2
# 35 xor: reg1 ^ reg2
# 36 sl:  reg1 << reg2
# 37 sr:  reg1 >> reg2
# 38 div: reg1 / reg2
# 39 mod: reg1 % reg2
# 3a g: reg1 > reg2
# 3b not: !reg
#
# Immediate ALU, all results are stored in ALU
# 40 addi: reg1 + immediate
# 41 subi: reg1 - immediate
# 42 muli: reg1 * immediate
# 43 andi: reg1 & immediate
# 44 ori:  reg1 | immediate
# 45 xori: reg1 ^ immediate
# 46 sli:  reg1 << immediate
# 47 sri:  reg1 >> immediate
# 48 divi: reg1 / immediate
# 49 modi: reg1 % immediate
# 4a gi: reg1 > immediate


def init_cpu():
    return [0] * 8

def read_memory(reg, mem):
    # Implement virtual memory checks
    if reg[C_MAR] < 0 or reg[C_MAR] > 7:
        raise Exception("Out of bounds")
    reg[C_MDR] = mem[
        mem[M_PROCESS_LIST + mem[M_CURRENT_PID]]
        + PD_BASE
        + reg[C_MAR]
    ]

def write_memory(reg, mem):
    # Implement virtual memory checks
    if reg[C_MAR] < 0 or reg[C_MAR] > 7:
        raise Exception("Out of bounds")
    mem[
        mem[M_PROCESS_LIST + mem[M_CURRENT_PID]]
        + PD_BASE
        + reg[C_MAR]
    ] = reg[C_MDR]

def decode(reg, mem):
    instruct = reg[C_IR]
    opcode = instruct >> 16
    operand1 = (instruct & 0xFF00) >> 8
    operand2 = instruct & 0xFF

    print(f"{opcode = :X}, {operand1 = :X}, {operand2 = :X}")

    # Begin the if chain
    if opcode == 0x00:  # nop
        pass
    elif opcode == 0x01:  # die
        pass
    elif opcode == 0x02:  # j adrr
        # Get virtual memory offset
        reg[C_PC] = (
            mem[M_PROCESS_LIST + mem[M_CURRENT_PID]]
            + PC_BASE
            + int(str(operand1), 16)
        )
    elif opcode == 0x03:  # je addr, reg
        if reg[operand2] == 0:
            reg[C_PC] = (
                mem[M_PROCESS_LIST + mem[M_CURRENT_PID]]
                + PC_BASE
                + int(str(operand1), 16)
            )
    elif opcode == 0x04:  # jne addr, reg
        if reg[operand2] != 0:
            reg[C_PC] = (
                mem[M_PROCESS_LIST + mem[M_CURRENT_PID]]
                + PC_BASE
                + int(str(operand1), 16)
            )

    # Registers and memory
    elif opcode == 0x10:  # wr reg1 = reg2
        reg[operand1] = reg[operand2]

    elif opcode == 0x11:  # wri reg = immediate
        reg[operand1] = operand2

    elif opcode == 0x12:  # rm reg = mem
        reg[C_MAR] = operand2
        read_memory(reg, mem)
        reg[operand1] = reg[C_MDR]

    elif opcode == 0x13:  # wm mem = reg
        reg[C_MAR] = reg[operand1]
        reg[C_MDR] = reg[operand2]
        write_memory(reg, mem)

    elif opcode == 0x14:  # wmi mem = immediate
        reg[C_MAR] = reg[operand1]
        reg[C_MDR] = operand2
        write_memory(reg, mem)

    # ALU operations (results go to ALU register)
    elif opcode == 0x30:  # add
        reg[C_ACC] = reg[operand1] + reg[operand2]

    elif opcode == 0x31:  # sub
        reg[C_ACC] = reg[operand1] + reg[operand2]

    elif opcode == 0x32:  # mul
        reg[C_ACC] = reg[operand1] * reg[operand2]

    elif opcode == 0x33:  # and
        reg[C_ACC] = reg[operand1] & reg[operand2]

    elif opcode == 0x34:  # or
        reg[C_ACC] = reg[operand1] | reg[operand2]

    elif opcode == 0x35:  # xor
        reg[C_ACC] = reg[operand1] ^ reg[operand2]

    elif opcode == 0x36:  # sl
        reg[C_ACC] = reg[operand1] << reg[operand2]

    elif opcode == 0x37:  # sr
        reg[C_ACC] = reg[operand1] >> reg[operand2]

    elif opcode == 0x38:  # div
        reg[C_ACC] = reg[operand1] // reg[operand2] if reg[operand2] != 0 else 0

    elif opcode == 0x39:  # mod
        reg[C_ACC] = reg[operand1] % reg[operand2] if reg[operand2] != 0 else 0

    elif opcode == 0x3a:  # g
        reg[C_ACC] = int(reg[operand1] > reg[operand2])

    elif opcode == 0x3b:  # not
        reg[C_ACC] = ~reg[operand1]

    # Immediate ALU operations (results go to ALU register)
    elif opcode == 0x40:  # add
        reg[C_ACC] = reg[operand1] + operand2

    elif opcode == 0x41:  # subi
        reg[C_ACC] = reg[operand1] + operand2

    elif opcode == 0x42:  # muli
        reg[C_ACC] = reg[operand1] * operand2

    elif opcode == 0x43:  # andi
        reg[C_ACC] = reg[operand1] & operand2

    elif opcode == 0x44:  # ori
        reg[C_ACC] = reg[operand1] | operand2

    elif opcode == 0x45:  # xori
        reg[C_ACC] = reg[operand1] ^ operand2

    elif opcode == 0x46:  # sli
        reg[C_ACC] = reg[operand1] << operand2

    elif opcode == 0x47:  # sri
        reg[C_ACC] = reg[operand1] >> operand2

    elif opcode == 0x48:  # divi
        reg[C_ACC] = reg[operand1] // operand2 if operand2 != 0 else 0

    elif opcode == 0x49:  # modi
        reg[C_ACC] = reg[operand1] % operand2 if operand2 != 0 else 0

    elif opcode == 0x4a:  # gi
        reg[C_ACC] = int(reg[operand1] > operand2)

    else:
        raise ValueError(f"Unknown opcode: {opcode:02X}")
