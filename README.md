arduinosim
==========

Attempt at an Arduino simulator in Python.


Current set of instructions implemented:
----------------------------------------
| Mnemonic |       Description       | Implemented? |
| -------- | ----------------------- |:------------:|
|      **ARITHMETIC AND LOGIC INSTRUCTIONS**      |||
|
| COM      | 1's compliment          |       x      |
| NEG      | 2's compliment          |       x      |
| INC      | Increment register      |       x      |
| DEC      | Decrement register      |       x      |
|              **BRANCH INSTRUCTIONS**            |||
| RET      | Subroutine return       |       x      |
| RETI     | Interrupt return        |       x      |
|        **BIT AND BIT-TEST INSTRUCTIONS**        |||
| SEC      |                         |       x      |
| CLC      |                         |       x      |
| SEN      |                         |       x      |
| CLN      |                         |       x      |
| SEZ      |                         |       x      |
| CLZ      |                         |       x      |
| SEI      |                         |       x      |
| CLI      |                         |       x      |
| SES      |                         |       x      |
| CLS      |                         |       x      |
| SEV      |                         |       x      |
| CLV      |                         |       x      |
| SET      |                         |       x      |
| CLT      |                         |       x      |
| SEH      |                         |       x      |
| CLH      |                         |       x      |
|           **DATA TRANSFER INSTRUCTIONS**        |||
| MOVW     | Copy register word      |       x      |
|           **MCU CONTROL INSTRUCTIONS**          |||
| NOP      | No operation            |       x      |
| SLEEP    |                         |       x      |
