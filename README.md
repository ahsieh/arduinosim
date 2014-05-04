arduinosim
==========

Attempt at an Arduino simulator in Python.


Current set of instructions implemented:
----------------------------------------
| Mnemonic |       Description                   | Implemented? |
| -------- | ----------------------------------- |:------------:|
|             **ARITHMETIC AND LOGIC INSTRUCTIONS**           |||
| ADD      | Add two registers                   |      x       |
| ADC      | ADD with Carry                      |      x       |
| ADIW     | Add immediate to word               |              |
| SUB      | Subtract registers                  |              |
| SUBI     | Subtract constant from register     |              |
| SBC      | SUB with Carry                      |              |
| SBCI     | SUBI with Carry                     |              |
| SBIW     | Subtract immediate from word        |              |
| AND      | Logical AND register                |              |
| ANDI     | Logical AND immediate               |              |
| OR       | Logical OR register                 |              |
| ORI      | Logical OR immediate                |              |
| EOR      | Exclusive OR Registers              |              |
| COM      | 1's compliment                      |       x      |
| NEG      | 2's compliment                      |       x      |
| SBR      | Set bit(s) in register              |              |
| CBR      | Clear bit(s) in register            |              |
| INC      | Increment register                  |       x      |
| DEC      | Decrement register                  |       x      |
| TST      | Test zero or minus                  |              |
| CLR      | Clear register                      |              |
| SER      | Set register                        |              |
| MUL      | Multiply unsigned                   |              |
| MULS     | Multiply signed                     |              |
| MULSU    | Multiply signed/unsigned            |              |
| FMUL     | Fractional multiply unsigned        |              |
| FMULS    | Fractional mulitply signed          |              |
| FMULSU   | Fractional multiply signed/unsigned |              |
|          |                                     |              |
|                    **BRANCH INSTRUCTIONS**                  |||
| RET      | Subroutine return                   |       x      |
| RETI     | Interrupt return                    |       x      |
|              **BIT AND BIT-TEST INSTRUCTIONS**              |||
| SEC      |                                     |       x      |
| CLC      |                                     |       x      |
| SEN      |                                     |       x      |
| CLN      |                                     |       x      |
| SEZ      |                                     |       x      |
| CLZ      |                                     |       x      |
| SEI      |                                     |       x      |
| CLI      |                                     |       x      |
| SES      |                                     |       x      |
| CLS      |                                     |       x      |
| SEV      |                                     |       x      |
| CLV      |                                     |       x      |
| SET      |                                     |       x      |
| CLT      |                                     |       x      |
| SEH      |                                     |       x      |
| CLH      |                                     |       x      |
|                 **DATA TRANSFER INSTRUCTIONS**              |||
| MOVW     | Copy register word                  |       x      |
|                 **MCU CONTROL INSTRUCTIONS**                |||
| NOP      | No operation                        |       x      |
| SLEEP    |                                     |       x      |
