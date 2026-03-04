REGS = {
    "$ac": 4,
    "$r0": 5,
    "$r1": 6,
    "$r2": 7,
}

OPCODES = {
    # Control
    "nop":  0x00,
    "die":  0x01,
    "j":    0x02,
    "je":   0x03,
    "jne":  0x04,

    # Registers and memory
    "wr":   0x10,
    "wri":  0x11,
    "rm":   0x12,
    "wm":   0x13,
    "wmi":  0x14,

    # ALU (register–register)
    "add":  0x30,
    "sub":  0x31,
    "mul":  0x32,
    "and":  0x33,
    "or":   0x34,
    "xor":  0x35,
    "sl":   0x36,
    "sr":   0x37,
    "div":  0x38,
    "mod":  0x39,
    "g":    0x3A,
    "not":  0x3B,

    # Immediate ALU
    "addi": 0x40,
    "subi": 0x41,
    "muli": 0x42,
    "andi": 0x43,
    "ori":  0x44,
    "xori": 0x45,
    "sli":  0x46,
    "sri":  0x47,
    "divi": 0x48,
    "modi": 0x49,
    "gi":   0x4A,
}

def parse_operand(x):
    x = x.strip()
    if x in REGS:
        return REGS[x]
    if x.startswith("0x"):
        return int(x, 16)
    return int(x)

def assemble_line(line):
    line = line.split("#")[0].strip()
    if not line or line.startswith("#"):
        return None

    parts = line.replace(",", " ").split()
    mnemonic = parts[0].lower()

    if mnemonic not in OPCODES:
        raise ValueError(f"Unknown instruction '{mnemonic}'")

    opcode = OPCODES[mnemonic]
    operands = parts[1:]

    op1 = 0
    op2 = 0

    if len(operands) == 1:
        op1 = parse_operand(operands[0])
    elif len(operands) == 2:
        op1 = parse_operand(operands[0])
        op2 = parse_operand(operands[1])

    return (opcode << 16) | (op1 << 8) | op2

def assemble(program_text):
    instructions = []
    for n, line in enumerate(program_text.splitlines()):
        if (inst := assemble_line(line)) is not None:
            instructions.append(inst)
    return instructions

if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        raise Exception("No file provided")

    with open(argv[1], "r") as f:
        program = f.read()

    assembled = assemble(program)
    for i, word in enumerate(assembled):
        print(f"0x{word:06X},")
