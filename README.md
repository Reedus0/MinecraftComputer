# Computer specs

* 8 general purpose registers
* 0.25 HZ clock
* ALU capable of adding and subtracting
* 64 bytes of RAM
* 64 bytes of ROM
* Machine word length - 16-bit

# Instruction set
Currently computer have 9 possible operations

## NOP 
Do nothing
## HLT 
Halt clock
## ADD rdest, r1, r2 
Add two number and write result in rdest
## SUB rdest, r1, r2
Sub r1 from r2 and write result in rdest
## STR rsource, address
Load data from rsource to RAM 
## LOD rdest, address
Load data from RAM to rdest 
## LDI rdest, value
Load 8-bit value to rdest
## JMP address
Set PC to address
## JIZ address
Set PC to address if result of previous ALU operation was zero