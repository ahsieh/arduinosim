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
                            print "SRAM size: " + str(self.sram_size)

            # If SRAM wasn't defined, we default to the lowest
            #  value.
            if self.sram_size == 0:
                self.sram_size = 512

            # Lastly, add the internal SRAM to the data memory
            sram_start = memptr
            sram_end = sram_start + self.sram_size
            for addr in xrange(sram_start, sram_end):
              self.memory.append(AVRMemoryByte(addr))

        except:
            print "Err: File does not exist!"

    # String Representation
    def __str__(self):
        retstr = ""
        for mem in self.memory:
          retstr = retstr + str(mem) + "\r\n"
        return retstr
        
# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    sram = AVRDataMemory("arch/atmega328p.def")
    print sram
