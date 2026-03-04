"""
Provides an shell to interact with an arbitrary kernel, register, and memory.
"""


def padded_hex(n):
    return hex(n)[2:].zfill(6) if n != 0xFFFF else "------"

def hexdump(src):
    for i in range(0, len(src), 8):
        print("\033[7m" if i % 32 == 0 else "\033[0m", end="")
        print(f"{padded_hex(i)}-{padded_hex(i+7)}:", " ".join(padded_hex(src[i]) for i in range(i, i+8)))
    print("\033[0m", end="")


while 1:
    user = input("> ")

    if user == "n":
        print(f"{memory[M_CURRENT_PID] = }")
        cpu_cycle(registers, memory)

    elif user == "hex":
        hexdump(memory)
        hexdump(registers)

    elif user == "rex":
        hexdump(registers)

    elif user == "mex":
        hexdump(memory)

    elif user == "q":
        break