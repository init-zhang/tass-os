# Tass-OS

List of theory operating systems based off my OS module content. Name is a reference to a lecturer.

The primary aim of this repository is to apply the content and learning into practice.

All OSes run on simulated hardware (see CPUs). There have been attempts to make the OS realistic, such as only using the simulated hardware.

Different OSes will use different hardware and components (see schedulers). Not all OSes and hardware are compatible.

## CPUs

### [3B](https://github.com/init-zhang/tass-os/tree/main/cpu/cpu3b)

Simple 24-bit CPU. Named after its 3 byte-long CPU instructions.

- only works on memory with 3 byte-long words
- all arithmetic instructions inaccurately take one cycle to complete
- raises ValueError on unknown opcode. Raises Exception on inaccessible memory or register access.

## OSes

### [FCFS](https://github.com/init-zhang/tass-os/tree/main/os/fcfs)

First Come, First Serve scheduler.

- smallest unit is processes, not threads
- all processes get one instruction call before being context switched out
