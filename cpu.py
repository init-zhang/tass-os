"""
Simple 16-bit CPU. All arithmetic inaccurately take one cycle to complete.

Raises VakueError on unknown opcode. Raises Exception on inaccessible memory
or register access.
"""


from constants import *


# Instruction set
# 0000   00 00 00000000
# opcode rA rB Imm

# Valid registers:
# 0 $r0
# 1 $r1
# 2 $r2
# 3 $acc

# [rA] refers to value inside register rA.
# [rB] refers to value inside register rB.
# [constant] refers to bits made of rB + Imm, only when Imm is not 0.

# opcodes:
#  0 NOP
#  1 HALT
#  2 LOAD value inside memory address at [rB] or [constant] into rA.
#  3 STORE value in rA into memory address at [rB] or [constant].
#  4 MOV [rB] or [constant] into rA.
#  5 ADD [rA] + [rB] or [constant] into $acc.
#  6 SUB [rA] - [rB] or [constant] into $acc.
#  7 AND [rA] & [rB] or [constant] into $acc.
#  8 OR [rA] | [rB] or [constant] into $acc.
#  9 SHIFT [rA] >> [rB] or [constant] into $acc.
# 10 NOT inverse of [rB] or [constant] into rA.
# 11 LT store 1 into $acc if [rA] < [rb] or [constant], otherwise 0.
# 12 EQ store 1 into $acc if [rA] = [rb] or [constant], otherwise 0.
# 13 JUMP to [rA] or [constant].
# 14 BRANCH to [rB] or [constant] if [rA] = 1.
# 15 RESERVED


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
