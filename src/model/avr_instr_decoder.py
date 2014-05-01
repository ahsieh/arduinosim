#!/usr/bin/python

# Imports -------------------------------------------------------------------
from avr_flashmem import AVRFlashWord
from avr_flash import AVRFlash
from avr_sram import AVRDataMemory
from avr_program_counter import AVRProgramCounter

# Classes -------------------------------------------------------------------
## Atmega AVR Instruction Decoder Structure
class AVRInstructionDecoder(object):
    # Instance variables
    
    # Override methods
    # Initialization
    def __init__(self, data_memory, program_counter):
        self.instruction_str = ""
        self.operand1_str = ""
        self.operand2_str = ""
        self.data_memory = data_memory
        self.program_counter = program_counter
        self.instr_addr = self.program_counter.read()

    # String Representation
    def __str__(self):
        retstr = "PC: 0x%(pc)04X  " % { "pc" : self.instr_addr }
        retstr = retstr + self.instruction_str + " "
        retstr = retstr + self.operand1_str
        if (self.operand2_str != ""):
            retstr = retstr + ", " + self.operand2_str
        return retstr

    # Instance methods
    def load(self, opcode):
        self.reset()
        self.instr_addr = self.program_counter.read()
        if (type(opcode) is AVRFlashWord):
            opcode_val = opcode.read()
            if (opcode_val == 0b00000000):
                # NOP
                self.instruction_str = "NOP"
                self.operand1_str = ""
                self.operand2_str = ""

            elif ((opcode_val & 0b1111111100000000) == 0b0000000100000000):
                # MOVW (Copy Register Word)
                Rd0 = ((opcode_val & 0x00F0) >> 4) * 2
                Rd1 = Rd0 + 1
                Rr0 = (opcode_val & 0x000F) * 2
                Rr1 = Rr0 + 1
                self.data_memory.memory[Rd1].write(self.data_memory.memory[Rr1].read())
                self.data_memory.memory[Rd0].write(self.data_memory.memory[Rr0].read())

                self.instruction_str = "MOVW"
                self.operand1_str = "r" + str(Rd1) + ":" + str(Rd0)
                self.operand2_str = "r" + str(Rr1) + ":" + str(Rr0)

            elif ((opcode_val & 0b1111111100001111) == 0b1001010000001000):
                # Set/Clear bit in SREG
                bit = (opcode_val & 0x0070) >> 4
                if (opcode_val & 0x80):
                    self.instruction_str = "CLx"
                    mask = ~(1 << bit)
                else:
                    self.instruction_str = "SEx"
                    mask = 1 << bit

                # Update SREG
                try:
                    reg = next(r for r in self.data_memory.memory if r.name == "SREG")
                    reg.set_bits(mask)
                except:
                    pass

            elif ((opcode_val & 0b1111111000001111) == 0b1001010000001010):
                # Decrement register
                Rd = ((opcode_val & 0x01F0) >> 4)
                self.data_memory.memory[Rd].decr() # Carry flag NOT affected
                self.instruction_str = "DEC"
                self.operand1_str = "r" + str(Rd)

            elif ((opcode_val & 0b1100000000000000) == 0b1100000000000000):
                # Relative Jump/Call
                offset = opcode_val & 0x0FFF
                if (opcode_val & 0b0001000000000000):
                    # Call - TODO Stack stuffz
                    self.instruction_str = "RCALL"
                else:
                    # Jump
                    self.instruction_str = "RJMP"
                    
                # Update PC
                if (opcode_val & 0x0800):
                    self.program_counter.sub(opcode_val & 0x07FF)
                    self.operand1_str = "-" + str(opcode_val & 0x07FF)
                else:
                    self.program_counter.add(opcode_val & 0x07FF)
                    self.operand1_str = "+" + str(opcode_val & 0x07FF)


            # ----- END BIG IF/ELIF STATEMENT -----

            # PC
            self.program_counter.add(1)
        else:
            print "Type err: Type was " + str(type(opcode))
            self.reset()

    def reset(self):
        self.instruction_str = ""
        self.operand1_str = ""
        self.operand2_str = ""
    

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    def_file = "arch/atmega328p.def"
    sram = AVRDataMemory(def_file)
    if (sram.sram_size != 0):
        flash = AVRFlash(def_file)
        flash.write(0, 0b1001010000001000)
        flash.write(1, 0b1001010000101000)
        flash.write(2, 0b0000000100010011)
        flash.write(3, 0b1001010000001010)
        flash.write(4, 0b1001010000011010)
        flash.write(5, 0b1100000000000000 + 5)
        flash.write(11, 0b1001010001011010)
        program_counter = AVRProgramCounter()
        decoder = AVRInstructionDecoder(sram, program_counter)

        while (decoder.instruction_str != "NOP"):
            decoder.load(flash.get(program_counter.read()))
            print decoder

        # 
        print "========= Final Results =========="
        sram.debug_print_genregs()
        sram.debug_print_sreg()
