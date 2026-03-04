# Tass-OS

## CPUs

### [3B](https://github.com/init-zhang/tass-os/tree/main/cpu/cpu3b)

Simple 24-bit CPU. Named after it's 3 byte long CPU instructions.

- only works on 3 byte-long word memory
- all arithmetic instructions inaccurately take one cycle to complete
- raises ValueError on unknown opcode. Raises Exception on inaccessible memory or register access.

## OSes

### [FCFS](https://github.com/init-zhang/tass-os/tree/main/os/fcfs)

First Come, First Serve scheduler.

- smallest unit is processes, not threads
- all processes get one instruction call before being context switched out