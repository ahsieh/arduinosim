#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Generic Register Object
class AVRFlashWord(object):
    # Instance variables
    addr = 0x0000
    contents = 0x0000
    bitmask = 0xFFFF

    # Override methods
    # Initialization
    def __init__(self, addr):
        self.addr = addr

    # String Representation
    def __str__(self):
        return "flash @0x%(addr)04X: 0x%(val)04X" % \
                { "addr" : self.addr , "val" : self.read() }

    # Object Comparison
    # TODO

    # Instance methods
    # Read flash word contents
    def read(self):
        return self.contents & self.bitmask

    # Modify flash word contents
    def write(self, contents):
        self.contents = contents & self.bitmask

    # Read flash low byte contents
    def read_lo(self):
        return self.contents & 0x00FF

    # Write flash low byte contents
    def write_lo(self, contents):
        self.contents = (self.contents & 0xFF00) + (contents & 0x00FF)

    # Read flash high byte contents
    def read_hi(self):
        return (self.contents >> 8) & 0x00FF

    # Write flash high byte contents
    def write_hi(self, contents):
        self.contents = (self.contents & 0x00FF) + ((contents << 8) & 0xFF00)

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    flashbyte = AVRFlashWord(0x0000)
    flashbyte.write(0xABCD)
    flashbyte.read()
    print flashbyte
