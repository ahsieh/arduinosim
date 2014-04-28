#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Atmega Memory Structure
class AVRProgramCounter(object):
    # Instance variables
    bitmask = 0xFFFF

    # Override methods
    # Initialization
    def __init__(self, bitmask=0xFFFF):
        self.pc = 0

    # String Representation
    def __str__(self):
        return "PC: " + str(self.pc)

    # Instance methods
    # Add to program counter
    def add(self, value):
        self.pc = (self.pc + value) & self.bitmask

    # Subtract from program counter
    def sub(self, value):
        self.pc = (self.pc - value) & self.bitmask

    # Write value to program counter
    def write(self, value):
        self.pc = value & self.bitmask

    # Read value from program counter
    def read(self):
        return self.pc


# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    pc = AVRProgramCounter()
    print pc
    pc.add(2)
    print pc
    pc.add(1)
    print pc
    pc.write(0x32)
    print pc
    print pc.read()
