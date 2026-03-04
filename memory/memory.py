"""
256 long integer array used to simulate memory.

The OS variables `M_PROCESS_LIST`, `M_QUEUE_TAIL`, and `M_QUEUE_HEAD` are set
here, though should be moved to OS code.
"""


from constants import *

def init_memory():
    memory = [0xFFFF] * 256
    memory[M_PROCESS_LIST] = 0
    memory[M_QUEUE_TAIL] = M_QUEUE_BASE
    memory[M_QUEUE_HEAD] = M_QUEUE_BASE
    return memory
