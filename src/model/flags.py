#!/usr/bin/python

# Imports -------------------------------------------------------------------

class AtmegaFlags:
    # Instance variables
    character = ""
    bitmask = 1
    description = ""

    # Override methods
    # Initialization
    def __init__(self, character, bitmask, description):
        self.character = character
        self.bitmask = bitmask
        self.description = description

    # String Representation
    def __str__(self):
        #return str(self.character + " @" + str(self.bitmask))
        return str(self.character + " @" + "%(bm)02x" % {'bm': self.bitmask})
    
class AtmegaSREG:
    # Instance variables
    flags = [None] * 8
    status_reg = 0b00000000

    # Override methods
    # Initialization
    def __init__(self):
        # Setup the flags in the status register
        self.flags[0] = AtmegaFlags("C", 0b00000001, "Carry Flag")
        self.flags[1] = AtmegaFlags("Z", 0b00000010, "Zero Flag")
        self.flags[2] = AtmegaFlags("N", 0b00000100, "Negative Flag")
        self.flags[3] = AtmegaFlags("V", 0b00001000, "Overflow Flag")
        self.flags[4] = AtmegaFlags("S", 0b00010000, "Sign Flag")
        self.flags[5] = AtmegaFlags("H", 0b00100000, "Half Carry")
        self.flags[6] = AtmegaFlags("T", 0b01000000, "BIt Copy")
        self.flags[7] = AtmegaFlags("I", 0b10000000, "Interrupt Flag")

        # Set the default value of the status register
        status_reg = 0b00000000

    # String Representation
    def __str__(self):
        retstr = ""
        for i in xrange(8):
            retstr = retstr + str(self.flags[i]) + "\r\n"
        return retstr

if __name__ == "__main__":
    sreg = AtmegaSREG()
    print sreg
