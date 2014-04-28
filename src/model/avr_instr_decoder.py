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

    # String Representation
    def __str__(self):
        retstr = self.instruction_str + " "
        retstr = retstr + self.operand1_str
        if (self.operand2_str != ""):
            retstr = retstr + ", " + self.operand2_str
        return retstr

    # Instance methods
    def load(self, opcode):
        if (type(opcode) is AVRFlashWord):
            opcode_val = opcode.read()
            if (opcode_val == 0b00000000):
                self.instruction_str = "NOP"
                self.operand1_str = ""
                self.operand2_str = ""
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
                    print reg
                except:
                    pass
                
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
        program_counter = AVRProgramCounter()
        decoder = AVRInstructionDecoder(sram, program_counter)
        decoder.load(flash.get(program_counter.read()))
        print decoder
        decoder.load(flash.get(program_counter.read()))
        print decoder
        decoder.load(flash.get(program_counter.read()))
        print decoder
