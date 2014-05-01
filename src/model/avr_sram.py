#!/usr/bin/python

# Imports -------------------------------------------------------------------
from avr_mem import AVRMemoryByte
from avr_reg import AVRRegister

# Classes -------------------------------------------------------------------
## Atmega Memory Structure
class AVRDataMemory(object):
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

                # Set the stack pointer to the top of SRAM
                self.write_sp(sram_end - 1)

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
        retval = (self.memory[addr + 1].read() << 8) & 0xFF00
        retval = retval + self.memory[addr].read()
        return retval

    # Write memory contents (word addressed)
    def write_word(self, addr, data):
        data_lo = data & 0xFF
        data_hi = (data >> 8) & 0xFF
        self.memory[addr].write(data_lo)
        self.memory[addr + 1].write(data_hi)

    # Set Stack Pointer
    def write_sp(self, val):
        try:
            spl = next(r for r in self.memory if r.name == "SPL")
            sph = next(r for r in self.memory if r.name == "SPH")
            val_lo = val & 0xFF
            val_hi = (val >> 8) & 0xFF
            spl.write(val_lo)
            sph.write(val_hi)
        except:
            pass

    # Get Stack Pointer
    def read_sp(self):
        try:
            spl = next(r for r in self.memory if r.name == "SPL")
            sph = next(r for r in self.memory if r.name == "SPH")
            val_lo = spl.read()
            val_hi = sph.read()
            val = (val_hi << 8) + val_lo
            return val
        except:
            return 0

    # Decrement Stack Pointer
    def dec_sp(self, dec):
        val = self.read_sp()
        self.write_sp(val - dec)

    # Increment Stack Pointer
    def inc_sp(self, inc):
        val = self.read_sp()
        self.write_sp(val + inc)

    # DEBUG - Print the contents of a general register 
    def debug_print_genreg(self, r):
        if (0 <= r and r <= 32):
            retstr = "Contents of R:" + str(r) + "\r\n"
            retstr = retstr + "---------------\r\n"
            retstr = retstr + str(self.memory[r]) + "\r\n"
            print retstr

    # DEBUG - Print the contents of general registers (default range: R0-R32)
    def debug_print_genregs(self, r1=0, r2=32):
        if (r1 <= r2 and 0 <= r1 and r1 < 32 and 0 <= r2 and r2 <= 32):
            retstr = "Contents of R" + str(r1) + " - R" + str(r2) + ":\r\n"
            retstr = retstr + "---------------------\r\n"
            for r in xrange(r1, r2):
                retstr = retstr + str(self.memory[r]) + "\r\n"
            print retstr

    # DEBUG - Print SREG
    def debug_print_sreg(self):
        try:
            reg = next(r for r in self.memory if r.name == "SREG")
            print reg
        except:
            pass

    # DEBUG - Print SP
    def debug_print_sp(self):
        try:
            print "SP 0x%(sp)03X" % { "sp" : self.read_sp() }
        except:
            pass
        
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
