"""
OS kernel to demonstrate the First Come, First Serve scheduler.

CPU: 3B
Memory size: 768B (256 * 3B)

Notes:
- word size is 3B rather than 1
- fixed partition memory
"""


from cpu.cpu3b import cpu3b
from scheduler.fcfs import *


# Memory
# 0-31 OS and scheduler
# 15 Current PID
# 16 Queue tail
# 17 Queue head
# 18-23 Process queue
# 24 Next free PID
# 25-31 Process list
# 32-1023 Processes
M_CURRENT_PID = 15
M_QUEUE_TAIL = 16
M_QUEUE_HEAD = 17
M_QUEUE_BASE = 18
M_QUEUE_END = 23
M_PROCESS_LIST = 24
M_PROCESSES = 32
# Hex structure
# +--+--------+------+--+--+--+--+--+--------+--+
# |0 |        |      |  |  |  |  |  |        |7 |
# +--+--------+------+--+--+--+--+--+--------+--+
# |8 |        |      |  |  |  |  |  |PID_curr|15|
# +--+--------+------+--+--+--+--+--+--------+--+
# |16|Q_tail  |Q_head|q1|q2|q3|q4|q5|q6      |23|
# +--+--------+------+--+--+--+--+--+--------+--+
# |24|PID_next|p1    |p2|p3|p4|p5|p6|p7      |31|
# +--+--------+------+--+--+--+--+--+--------+--+

# Processes
P_SIZE = 32
# 0-7 Process control block
PCB_PID = 0
PCB_PC = 1
PCB_ACC = 2
PCB_R0 = 3
PCB_R1 = 4
PCB_R2 = 5
# State of process, 1 - alive, 0 - dead
PCB_S = 6
# 8-15 words of data
PD_BASE = 8
PD_LENGTH = 8
# 16-31 words of code
PC_BASE = 16
PC_LENGTH = 16
# Hex structure
# +--+----+----+----+----+----+----+----+----+
# |- |0   |1   |2   |3   |4   |5   |6   |7   |
# +--+----+----+----+----+----+----+----+----+
# |0 |PID |PC  |ACC |r0  |R1  |R2  |S   |    |
# +--+----+----+----+----+----+----+----+----+
# |8 |Data|Data|Data|Data|Data|Data|Data|Data|
# +--+----+----+----+----+----+----+----+----+
# |16|Inst|Inst|Inst|Inst|Inst|Inst|Inst|Inst|
# +--+----+----+----+----+----+----+----+----+
# |24|Inst|Inst|Inst|Inst|Inst|Inst|Inst|Inst|
# +--+----+----+----+----+----+----+----+----+


def init_memory():
    """
    256 long integer array used to simulate memory. Each word is 3 bytes long
    due to 3B CPU used.
    """
    memory = [0xFFFFFF] * 256
    memory[M_PROCESS_LIST] = 0
    memory[M_QUEUE_TAIL] = M_QUEUE_BASE
    memory[M_QUEUE_HEAD] = M_QUEUE_BASE
    return memory


memory = init_memory()
registers = cpu3b.init_cpu()

print(memory, registers)
