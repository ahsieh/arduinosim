#!/usr/bin/python

# Imports -------------------------------------------------------------------
from avr_mem import AVRMemoryByte
from avr_reg import AVRRegister

# Classes -------------------------------------------------------------------
## Atmega Memory Structure
class AVRDataMemory:
    # Instance variables
    sram_size = 0

    # Override methods
    # Initialization
    def __init__(self, def_filename):
        try:
            errflag = 0

            # First, initialize the memory by adding all the
            # standard registers.
            memptr = 0
            self.memory = []
            for addr in xrange(0, 32):
                regname = "R%(num)d" % { "num" : addr }
                self.memory.append(AVRRegister(addr, regname))
                memptr = memptr + 1

            # Open the file for reading
            f = open(def_filename, "r")

            # Go through all the lines to find the necessary data
            # (IO registers, ext. IO regsiters, and SRAM size)
            for line in f:
                if (line[0] != ';'):
                    words = line.split()
                    if (len(words) > 0):
                        if (words[0] == "SRAM" and words[1] == "="):
                            # Save the SRAM size. This does NOT include
                            #  the standard registers, IO register, and
                            #  external IO registers
                            self.sram_size = int(words[2])
                        else:
                            # Register definitions:
                            # Error check to make sure these are valid.
                            if (len(words) == 4):
                                try:
                                    if (words[0].strip()[:2] == "0x" or \
                                                words[0].strip()[:2] == "0X"):
                                        addr = int(words[0].strip(), 16)
                                    else:
                                        addr = int(words[0].strip())

                                    regname = str(words[1].strip())

                                    if (words[2].strip()[:2] == "0x" or \
                                                words[0].strip()[:2] == "0X"):
                                        read_bm = int(words[2].strip(), 16)
                                    else:
                                        read_bm = int(words[2].strip())

                                    if (words[3].strip()[:2] == "0x" or \
                                                words[3].strip()[:2] == "0X"):
                                        write_bm = int(words[3].strip(), 16)
                                    else:
                                        write_bm = int(words[3].strip())

                                    if (memptr == addr):
                                        memptr = memptr + 1
                                        self.memory.append(AVRRegister(addr, \
                                               regname, 0, read_bm, write_bm))
                                    else:
                                        print "**Error: missing register at " + \
                                                "address " + str(memptr)
                                        errflag = 1
                                        break
                                except:
                                    print "**Error: definition file has errors"
                                    errflag = 1
                                    break

            if (errflag == 1):
                # Error occured! Return an object with NO memory
                self.memory = []
                self.sram_size = 0
            else:
                # If SRAM wasn't defined, we default to the lowest
                #  value.
                if self.sram_size == 0:
                    self.sram_size = 512

                # Lastly, add the internal SRAM to the data memory
                sram_start = memptr
                sram_end = sram_start + self.sram_size
                for addr in xrange(sram_start, sram_end):
                  self.memory.append(AVRMemoryByte(addr))

            f.close()
        except:
            print "Err: File does not exist!"

    # String Representation
    def __str__(self):
        retstr = ""
        for mem in self.memory:
          retstr = retstr + str(mem) + "\r\n"
        return retstr

    # Instance methods
    # Read memory contents (byte addressed)
    def read_byte(self, addr):
        return self.memory[addr].read()

    # Write to memory (byte addressed)
    def write_byte(self, addr, data):
        self.memory[addr].write(data)

    # Read memory contents (word addressed)
    def read_word(self, addr):
        retval = (self.memory[addr].read() << 8) & 0xFF00
        retval = retval + self.memory[addr + 1].read()
        return retval
        
# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    sram = AVRDataMemory("arch/atmega328p.def")
    if (sram.sram_size != 0):
        sram.write_byte(0x1A, 0xDE)
        sram.write_byte(0x1B, 0xAD)
        print "0x%(val)02X" % { "val" : sram.read_byte(0x1A) }
        print "0x%(val)02X" % { "val" : sram.read_byte(0x1B) }
        print "0x%(val)04X" % { "val" : sram.read_word(0x1A) }
        sram.write_byte(0x8F0, 0xAC)
        print sram
