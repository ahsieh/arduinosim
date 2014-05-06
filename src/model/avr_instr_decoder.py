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

            elif ((opcode_val & 0b1111110000000000) == 0b0000110000000000):
                # ADD (Add two registers)
                Rd = (opcode_val & 0x01F0) >> 4
                Rr = (opcode_val & 0x000F) + ((opcode_val & 0x0200) >> 5)
                self.data_memory.memory[Rd].add(self.data_memory.memory[Rr].read())
                self.instruction_str = "ADD"
                self.operand1_str = "r" + str(Rd)
                self.operand2_str = "r" + str(Rr)

            elif ((opcode_val & 0b1111110000000000) == 0b0001110000000000):
                # ADC (Add with carry)
                try:
                    reg = next(r for r in self.data_memory.memory if r.name == "SREG")
                except:
                    pass
                Rd = (opcode_val & 0x01F0) >> 4
                Rr = (opcode_val & 0x000F) + ((opcode_val & 0x0200) >> 5)
                carry = reg.read() & 0x01
                self.data_memory.memory[Rd].add(self.data_memory.memory[Rr].read() + carry)
                self.instruction_str = "ADC"
                self.operand1_str = "r" + str(Rd)
                self.operand2_str = "r" + str(Rr)

            elif ((opcode_val & 0b1111111000000000) == 0b1001011000000000):
                # ADIW/SBIW (Add/Sub immediate to word)
                Rd = (((opcode_val & 0x0030) >> 4) * 2) + 24
                Rd1 = Rd + 1
                K = ((opcode_val & 0x00C0) >> 2) + (opcode_val & 0x000F)
                contents = (self.data_memory.memory[Rd1].read() << 8) & 0xFF00
                contents = contents + (self.data_memory.memory[Rd].read() & 0xFF)
                
                if (opcode_val & 0x0100):
                    # SBIW
                    contents = contents - K
                    self.instruction_str = "SBIW"
                else:
                    # ADIW
                    contents = contents + K
                    self.instruction_str = "ADIW"

                self.data_memory.memory[Rd1].write(contents >> 8)
                self.data_memory.memory[Rd].write(contents & 0xFF)
                
                self.operand1_str = "r" + str(Rd1) + ":" + str(Rd)
                self.operand2_str = str(K)

            elif ((opcode_val & 0b1100000000000000) == 0b0100000000000000):
                # Register Immediate Instructions (ORI, ANDI, etc.)
                Rd = ((opcode_val & 0x00F0) >> 4) + 16
                K = ((opcode_val & 0x0F00) >> 4) + (opcode_val & 0x000F)
                try:
                    reg = next(r for r in self.data_memory.memory if r.name == "SREG")
                    carry = reg.read() & 0x01
                except:
                    pass

                if (opcode_val & 0x3000 == 0x0000):
                    # SBCI
                    self.data_memory.memory[Rd].sub(K + carry)
                    self.instruction_str = "SBCI"
                elif (opcode_val & 0x3000 == 0x1000):
                    # SUBI
                    self.data_memory.memory[Rd].sub(K)
                    self.instruction_str = "SUBI"
                elif (opcode_val & 0x3000 == 0x2000):
                    # ORI
                    self.data_memory.memory[Rd].logical_or(K)
                    self.instruction_str = "ORI"
                elif (opcode_val & 0x3000 == 0x3000):
                    # ANDI
                    self.data_memory.memory[Rd].logical_and(K)
                    self.instruction_str = "ANDI"
                    
                self.operand1_str = "r" + str(Rd)
                self.operand2_str = "$" + str(K)

            elif ((opcode_val & 0b1111111100001111) == 0b1001010000001000):
                # Set/Clear bit in SREG
                try:
                    reg = next(r for r in self.data_memory.memory if r.name == "SREG")
                except:
                    pass

                bit = (opcode_val & 0x0070) >> 4
                if (opcode_val & 0x80):
                    self.instruction_str = "CLx"
                    reg.clear_bits(1 << bit)
                else:
                    self.instruction_str = "SEx"
                    reg.set_bits(1 << bit)

            elif ((opcode_val & 0b1111000000000000) == 0b1110000000000000):
                # Load Immediate (r16 - r31 only)
                Rd = ((opcode_val & 0x00F0) >> 4) + 16
                k = ((opcode_val & 0x0F00) >> 4) + (opcode_val & 0x000F)
                self.data_memory.memory[Rd].write(k)
                self.instruction_str = "LDI"
                self.operand1_str = "r" + str(Rd)
                self.operand2_str = "$" + str(k)

            elif ((opcode_val & 0b1111111000001111) == 0b1001010000001010):
                # Decrement register
                Rd = ((opcode_val & 0x01F0) >> 4)
                self.data_memory.memory[Rd].decr() # Carry flag NOT affected
                self.instruction_str = "DEC"
                self.operand1_str = "r" + str(Rd)

            elif ((opcode_val & 0b1111111000001000) == 0b1001010000000000):
                # 1-Operand Instructions (COM, NEG, SWAP, INC, etc.)
                Rd = ((opcode_val & 0x01F0) >> 4)
                if (opcode_val & 0x07 == 0b011):
                    # INC (increment)
                    self.data_memory.memory[Rd].incr() # Carry flag NOT affected
                    self.instruction_str = "INC"
                    self.operand1_str = "r" + str(Rd)
                elif (opcode_val & 0x07 == 0b000):
                    # COM (1's compliment)
                    self.data_memory.memory[Rd].ones_compliment()
                    self.instruction_str = "COM"
                    self.operand1_str = "r" + str(Rd)
                elif (opcode_val & 0x07 == 0b001):
                    # NEG (2's compliment)
                    self.data_memory.memory[Rd].negate()
                    self.instruction_str = "NEG"
                    self.operand1_str = "r" + str(Rd)
                else:
                    pass
                    
            elif ((opcode_val & 0b1111111011111111) == 0b1001010000001001):
                # Indirect Jump/Call
                new_pc = (self.data_memory.memory[31].read() << 8) & 0xFF00
                new_pc = new_pc + self.data_memory.memory[30].read() - 1
                
                if (opcode_val & 0b0000000100000000):
                    # Call
                    self.instruction_str = "ICALL"
                    ram_addr = self.data_memory.read_sp()
                    if (self.data_memory.sram_size < 0x10000):
                        ram_addr = ram_addr - 1
                        self.data_memory.write_word(ram_addr, self.program_counter.read())
                        self.data_memory.dec_sp(2)
                    else:
                        pass  # Not handled yet!
                    self.program_counter.write(new_pc)
                else:
                    # Jump
                    self.instruction_str = "IJMP"
                    self.program_counter.write(new_pc)
                    
                    
            elif ((opcode_val & 0b1110000000000000) == 0b1100000000000000):
                # Relative Jump/Call
                offset = opcode_val & 0x0FFF
                if (opcode_val & 0b0001000000000000):
                    # Call - TODO Stack stuffz
                    self.instruction_str = "RCALL"
                    ram_addr = self.data_memory.read_sp()
                    if (self.data_memory.sram_size < 0x10000):
                        ram_addr = ram_addr - 1
                        self.data_memory.write_word(ram_addr, self.program_counter.read())
                        self.data_memory.dec_sp(2)
                    else:
                        pass  # Not handled yet!
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

            elif ((opcode_val & 0b1111111100001111) == 0b1001010100001000):
                # Misc. (RET, RETI, )
                if (self.data_memory.sram_size < 0x1000):
                    if (((opcode_val & 0x00F0) >> 4) == 0b0000):
                        # RET
                        self.data_memory.inc_sp(2)
                        ram_addr = self.data_memory.read_sp() - 1
                        new_pc = self.data_memory.read_word(ram_addr)
                        self.program_counter.write(new_pc)
                        self.instruction_str = "RET"
                    elif (((opcode_val & 0x00F0) >> 4) == 0b0001):
                        # RETI (TODO set I flag in SREG)
                        self.data_memory.inc_sp(2)
                        ram_addr = self.data_memory.read_sp() - 1
                        new_pc = self.data_memory.read_word(ram_addr)
                        self.program_counter.write(new_pc)
                        self.instruction_str = "RETI"
                    elif (((opcode_val & 0x00F0) >> 4) == 0b1000):
                        # SLEEP
                        # TODO check documentation
                        pass
                    else:
                        pass
                else:
                    pass  # Not handled yet!

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
        flash.write(0, 0b1001010000001000)          # SEC
        flash.write(1, 0b1001010000101000)          # SEN
        flash.write(2, 0b0000000100010011)          # MOVW  r3:2, r7:6
        flash.write(3, 0b1001010000001010)          # DEC   r0
        flash.write(4, 0b1001010000011010)          # DEC   r1
        flash.write(5, 0b1100000000000000 + 5)      # RJMP  +5
        flash.write(11, 0b1001010001011010)         # DEC   r5
        flash.write(12, 0b1101000000000000 + 5)     # RCALL +5
        flash.write(13, 0b1001010000001010)         # DEC   r0
        flash.write(14, 0b1110000111101101)         # LDI   r30, $1D
        flash.write(15, 0b1110000011110000)         # LDI   r31, $00
        flash.write(16, 0b1001010000001001)         # IJMP
        flash.write(18, 0b1001010010001000)         # CLC
        flash.write(19, 0b1001010111100011)         # INC   r30
        flash.write(20, 0b1001010000001010)         # DEC   r0
        flash.write(21, 0b0000000100010000)         # MOVW  r3:2, r1:0
        flash.write(22, 0b1001010000000000)         # COM   r0
        flash.write(23, 0b1001010000010001)         # NEG   r1
        flash.write(24, 0b0000110000000001)         # ADD   r0, r1
        flash.write(25, 0b1001010000001000)         # SEC
        flash.write(26, 0b0001110000000010)         # ADC   r0, r2
        flash.write(27, 0b1001010010001000)         # CLC
        flash.write(28, 0b1001010100001000)         # RET
        flash.write(29, 0b1001011011010010)         # ADIW  r27:26, 50
        flash.write(30, 0b1001011101011001)         # SBIW  r27:26, 25
        flash.write(31, 0b0101000000001000)         # SUBI  r16, $8
        flash.write(32, 0b0100000100010111)         # SBCI  r17, $23
        flash.write(33, 0b0111101000001010)         # ANDI  r18, $AA
        flash.write(34, 0b0110000000011111)         # ORI   r19, $0F
        """
        """
        program_counter = AVRProgramCounter()
        decoder = AVRInstructionDecoder(sram, program_counter)

        while (decoder.instruction_str != "NOP"):
            decoder.load(flash.get(program_counter.read()))
            #print sram.memory[0]
            print decoder

        # 
        print "========= Final Results =========="
        sram.debug_print_genregs()
        sram.debug_print_sreg()
        sram.debug_print_sp()
