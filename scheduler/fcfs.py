"""
First Come, First Serve scheduler.

- smallest unit is processes, not threads
- all processes get one instruction call before being context switched out
"""


def start_process(reg, mem, binary):
    pid = mem[M_PROCESS_LIST]+1
    # Validate process limit and check for gaps
    mem[M_PROCESS_LIST] += 1
    process_base = M_PROCESSES+(pid-1)*P_SIZE
    mem[M_PROCESS_LIST+pid] = process_base
    mem[process_base + PCB_PID] = pid
    mem[process_base + PCB_PC] = process_base + PC_BASE
    for i, instruction in enumerate(binary):
        mem[process_base + PC_BASE + i] = instruction
    mem[M_CURRENT_PID] = pid
    enqueue(reg, mem)

def save_process(reg, mem):
    process_base = mem[M_PROCESS_LIST+mem[M_CURRENT_PID]]
    mem[process_base + PCB_PC] = reg[C_PC]
    mem[process_base + PCB_ACC] = reg[C_ACC]
    mem[process_base + PCB_R0] = reg[C_R0]
    mem[process_base + PCB_R1] = reg[C_R1]
    mem[process_base + PCB_R2] = reg[C_R2]

def load_process(reg, mem):
    process_base = mem[M_PROCESS_LIST+mem[M_CURRENT_PID]]
    reg[C_PC] = mem[process_base + PCB_PC]
    reg[C_ACC] = mem[process_base + PCB_ACC]
    reg[C_R0] = mem[process_base + PCB_R0]
    reg[C_R1] = mem[process_base + PCB_R1]
    reg[C_R2] = mem[process_base + PCB_R2]

def enqueue(reg, mem):
    mem[mem[M_QUEUE_TAIL]] = mem[M_CURRENT_PID]
    mem[M_QUEUE_TAIL] += 1
    if mem[M_QUEUE_TAIL] > M_QUEUE_END:
        mem[M_QUEUE_TAIL] = M_QUEUE_BASE

def dequeue(reg, mem):
    mem[M_CURRENT_PID] = mem[mem[M_QUEUE_HEAD]]
    mem[M_QUEUE_HEAD] += 1
    if mem[M_QUEUE_HEAD] > M_QUEUE_END:
        mem[M_QUEUE_HEAD] = M_QUEUE_BASE

# No local variables for the fun and realism
def cpu_cycle(reg, mem):
    reg[C_IR] = mem[reg[C_PC]]
    reg[C_PC] += 1

    decode(reg, mem)

    # Scheduler calls
    # Check queue
    # Save/load if needed
    save_process(reg, mem)
    enqueue(reg, mem)
    dequeue(reg, mem)
    load_process(reg, mem)
