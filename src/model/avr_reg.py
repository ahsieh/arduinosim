#!/usr/bin/python

# Imports -------------------------------------------------------------------
from avr_mem import AVRMemoryByte

# Classes -------------------------------------------------------------------
## Generic Memory Byte Object 
class AVRRegister(AVRMemoryByte):
    # Instance variables

    # Override methods
    # Initialization
    def __init__(self, addr, name, contents=0x00, rd_bm=0xFF, wr_bm=0xFF):
        AVRMemoryByte.__init__(self, addr, contents)
        self.name = name
        self.read_bitmask = rd_bm
        self.write_bitmask = wr_bm

    # String Representation
    def __str__(self):
        return "%(reg)s@0x%(addr)02X: 0x%(val)02X" % \
                { "reg" : self.name, "addr" : self.addr , "val" : self.read() }

    # Instance methods
    # Set bits in register
    def set_bits(self, bm):
        self.contents = (self.contents | bm) & self.write_bitmask

    # Clear bits in register
    def clear_bits(self, bm):
        self.contents = (self.contents & ~bm) & self.write_bitmask

    # Logical shift left
    # Return 1 if bit is shifted into the carry bit
    def shift_left(self):
        self.contents = self.contents << 1
        if (self.contents & 0x100):
            return 1
        return 0

    # Logical shift right
    # Return 1 if bit is shifted into the carry bit
    def shift_right(self):
        retval = 0
        if (self.contents & 0x01):
            retval = 1
        self.contents = (self.contents & 0xFF) >> 1
        return retval

    # Rotate left through carry
    def rotate_left(self, carry):
        retval = 0
        if (self.contents & 0x80):
            retval = 1
        if (carry):
            self.contents = ((self.contents << 1) & 0xFF) | 0x01
        else:
            self.contents = (self.contents << 1) & 0xFF
        return retval

    # Rotate left through carry
    def rotate_right(self, carry):
        retval = 0
        if (self.contents & 0x01):
            retval = 1
        if (carry):
            self.contents = (self.contents & 0xFF) | 0x100
        self.contents = self.contents >> 1
        return retval

    # Nibble swap
    # TODO?

# Main function --------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    print "Creating new register object"
    reg = AVRRegister(0x00, "R0")
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

    print "Writing 0x05 to register, carry = 0"
    reg.write(0x05)
    print reg

    carry = 0
    print "Shift register right (carry = 1, reg = 0x02)"
    carry = reg.shift_right()
    print str(reg) + " carry: " + str(carry)
    
    print "Shift register right (carry = 0, reg = 0x01)"
    carry = reg.shift_right()
    print str(reg) + " carry: " + str(carry)

    print "Shift register right (carry = 1, reg = 0x00)"
    carry = reg.shift_right()
    print str(reg) + " carry: " + str(carry)

    print "Rotate register right (carry = 0, reg = 0x80)"
    carry = reg.rotate_right(carry)
    print str(reg) + " carry: " + str(carry)

    print "Rotate register left (carry = 1, reg = 0x00)"
    carry = reg.rotate_left(carry)
    print str(reg) + " carry: " + str(carry)

    print "Writing 0x40 to register, carry = 1"
    reg.write(0x40)
    print str(reg) + " carry: " + str(carry)

    print "Shift register left (carry = 0, reg = 0x80)"
    carry = reg.shift_left()
    print str(reg) + " carry: " + str(carry)
    
    print "Shift register left (carry = 1, reg = 0x00)"
    carry = reg.shift_left()
    print str(reg) + " carry: " + str(carry)
    
