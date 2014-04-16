#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## ATmega Flag Class
class AtmegaFlags:
    # Instance variables
    character = ""
    bitmask = 0
    value = 0
    description = ""

    # Override methods
    # Initialization
    def __init__(self, character, bitmask, description):
        self.character = character
        self.bitmask = bitmask
        self.description = description
        self.value = 0

    # String Representation
    def __str__(self):
        return str(self.character + " @" + "%(bm)02x" % {'bm': self.bitmask})

    # Comparison
    def __cmp__(self, other):
        return cmp(self.character, other)

    # Instance functions
    # Set flag
    def set_flag(self):
        self.value = 1
    
    # Clear flag
    def clear_flag(self):
        self.value = 0

    # Get flag
    def get_flag(self):
        return self.value
    
## ATmega Status Register Class
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
        self.flags[6] = AtmegaFlags("T", 0b01000000, "Bit Copy")
        self.flags[7] = AtmegaFlags("I", 0b10000000, "Interrupt Flag")

        # Set the default value of the status register
        status_reg = 0b00000000

    # String Representation
    def __str__(self):
        retstr = ""
        for i in xrange(8):
            retstr = retstr + str(self.flags[i]) + "\r\n"
        return retstr

    # Instance functions
    # Set flag
    def set_flag(self, character):
        try:
            idx = self.flags.index(character)
            self.flags[idx].set_flag()
            self.status_reg = self.status_reg | (1 << idx)
        except:
            return

    # Clear flag
    def clear_flag(self, character):
        try:
            idx = self.flags.index(character)
            self.flags[idx].clear_flag()
            self.status_reg = self.status_reg & ~(1 << idx)
        except:
            return

    # Get flag
    def get_flag(self, character):
        try:
            idx = self.flags.index(character)
            return self.flags[idx].get_flag()
        except:
            return 0

    # Set Status Register
    def set_sreg(self, value):
        self.status_reg = value
        for i in xrange(0, 8):
            if ((1 << i) & value) > 0:
                self.flags[i].set_flag()
            else:
                self.flags[i].clear_flag()

    # Get Status Register
    def get_sreg(self):
        return self.status_reg

# Main Function -------------------------------------------------------------
## Main (for testing purposes)
if __name__ == "__main__":
    sreg = AtmegaSREG()
    print sreg
    print "%(sreg)02X" % {"sreg" : sreg.get_sreg()}
    sreg.set_flag("C")
    sreg.set_flag("N")
    sreg.set_flag("T")
    sreg.set_flag("I")

    print sreg.get_flag("C")
    print sreg.get_flag("Z")
    print sreg.get_flag("N")
    print sreg.get_flag("T")
    print sreg.get_flag("I")
    print "%(sreg)02X" % {"sreg" : sreg.get_sreg()}

    sreg.set_sreg(0x32)
    print sreg.get_flag("C")
    print sreg.get_flag("Z")
    print sreg.get_flag("N")
    print sreg.get_flag("V")
    print sreg.get_flag("S")
    print sreg.get_flag("H")
    print sreg.get_flag("T")
    print sreg.get_flag("I")
    print "%(sreg)02X" % {"sreg" : sreg.get_sreg()}

