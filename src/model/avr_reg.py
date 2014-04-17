#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Generic Register Object
class AVRRegister:
    # Instance variables
    size_in_bytes = 1
    start_addr = 0x0000
    contents = 0x00
    read_bitmask = 0xFF
    write_bitmask = 0xFF

    # Override methods
    # Initialization
    def __init__(self, start_addr, contents=0x00, rd_bm=0xFF, wr_bm=0xFF):
        self.start_addr = start_addr
        self.contents = contents & 0xFF
        self.read_bitmask = rd_bm
        self.write_bitmask = wr_bm

    # String Representation
    def __str__(self):
        return "reg@0x%(addr)02X: 0x%(val)02X" % \
                { "addr" : self.start_addr , "val" : self.read() }

    # Object Comparison
    # TODO

    # Instance methods
    # Read register contents
    def read(self):
        return self.contents & self.read_bitmask

    # Modify register contents
    def write(self, contents):
        self.contents = contents & self.write_bitmask

    # Increment register contents
    # Return 1 if overflow occurs, 0 otherwise
    def incr(self):
        retval = 0
        result = self.contents + 1
        if (result > 0xFF):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Decrement register contents
    # Return 1 if overflow occurs, 0 otherwise
    def decr(self):
        retval = 0
        result = self.contents - 1
        if (result < 0):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Add to register contents
    # Return 1 if overflow occurs, 0 otherwise
    def add(self, value):
        retval = 0
        result = self.contents + value
        if (result > 0xFF):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Subtract from register contents
    # Return 1 if overflow occurs, 0 otherwise
    def sub(self, value):
        retval = 0
        result = self.contents - value
        if (result < 0):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Set bits in register
    def set_bits(self, bm):
        self.contents = (self.contents | bm) & self.write_bitmask

    # Clear bits in register
    def clear_bits(self, bm):
        self.contents = (self.contents & ~bm) & self.write_bitmask

    # Nibble swap
    # TODO?

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    reg = AVRRegister(0x00)
    print reg
    reg.write(0xAA)
    print reg
    reg.write(0x3F)
    print reg
    reg.set_bits(0xC0)
    print reg
    reg.clear_bits(0xC0)
    print reg
    reg.write(0xFE)
    print reg
    print reg.incr()
    print reg
    print reg.incr()
    print reg
    print reg.decr()
    print reg
    print reg.decr()
    print reg

    print "............................"
    regs = []
    for x in xrange(32):
        regs.append(AVRRegister(x))
    for x in xrange(len(regs)):
        print regs[x]

