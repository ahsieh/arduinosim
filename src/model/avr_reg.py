#!/usr/bin/python

# Imports -------------------------------------------------------------------
from avr_mem import AVRMemoryByte

# Classes -------------------------------------------------------------------
## Generic Memory Byte Object 
class AVRRegister(AVRMemoryByte):
    # Instance variables

    # Override methods
    # Initialization
    def __init__(self, addr, contents=0x00, rd_bm=0xFF, wr_bm=0xFF):
        AVRMemoryByte.__init__(self, addr, contents)
        self.read_bitmask = rd_bm
        self.write_bitmask = wr_bm

    # String Representation
    def __str__(self):
        return "reg@0x%(addr)02X: 0x%(val)02X" % \
                { "addr" : self.addr , "val" : self.read() }

    # Instance methods
    # Set bits in register
    def set_bits(self, bm):
        self.contents = (self.contents | bm) & self.write_bitmask

    # Clear bits in register
    def clear_bits(self, bm):
        self.contents = (self.contents & ~bm) & self.write_bitmask

    # Nibble swap
    # TODO?

# Main function --------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    print "Creating new register object"
    reg = AVRRegister(0x00)
    print reg

    print "Writing 0x55 to register"
    reg.write(0x55)
    print reg

    print "Writing 0xFE to register"
    reg.write(0xFE)
    print reg

    print "Incrementing register (should be 0xFF, no overflow/carry)"
    ovf = reg.incr()
    print str(reg) + " overflow: " + str(ovf)

    print "Incrementing register (should be 0x00 with overflow/carry)"
    ovf = reg.incr()
    print str(reg) + " overflow: " + str(ovf)

    print "Decrementing register (should be 0xFF with overflow/carry)"
    ovf = reg.decr()
    print str(reg) + " overflow: " + str(ovf)

    print "Incrementing register (should be 0xFE, no overflow/carry)"
    ovf = reg.decr()
    print str(reg) + " overflow: " + str(ovf)

    print "Setting bit 0 (should be 0xFF)"
    reg.set_bits(0x01)
    print reg

    print "Clearing bit 5 (should be 0xDF)"
    reg.clear_bits(0x20)
    print reg

