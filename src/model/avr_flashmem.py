#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Generic Register Object
class AVRFlashWord:
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
    # Read memister contents
    def read(self):
        return self.contents & self.bitmask

    # Modify memister contents
    def write(self, contents):
        self.contents = contents & self.bitmask

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    flashbyte = AVRFlashWord(0x0000)
    flashbyte.write(0xABCD)
    flashbyte.read()
    print flashbyte
