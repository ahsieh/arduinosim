#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Atmega Memory Structure
class AtmegaMemory:
    # Instance variables
    size = 0

    # Override methods
    # Initialization
    def __init__(self, size):
        self.size = size
        self.memory = [0x00] * size

    # String Representation
    def __str__(self):
        return "Memory Size: " + str(len(self.memory))

    # Instance functions
    # Write memory location (byte addressed)
    def write_memory_byte(self, address, value):
        self.memory[address] = value & 0xFF

    # Read memory location (byte addressed)
    def read_memory_byte(self, address):
        return self.memory[address]

    # Write memory location (word addressed i.e. 16-bit)
    def write_memory_word(self, address, value):
        word_addr = address << 1
        self.memory[word_addr] = value & 0xFF
        self.memory[word_addr + 1] = (value >> 8) & 0xFF

    # Read memory location (word addressed i.e. 16-bit)
    def read_memory_word(self, address):
        word_addr = address << 1
        msb = (self.memory[word_addr + 1] << 8) & 0xFF00
        lsb = self.memory[word_addr] & 0xFF
        return (msb | lsb)


# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    mem = AtmegaMemory(32768)
    print mem

    print "%(val)02X" % {"val" : mem.read_memory_byte(0x00)}
    mem.write_memory_byte(0x00, 0xAA)
    mem.write_memory_byte(0x01, 0x55)
    print "%(val)02X" % {"val" : mem.read_memory_byte(0x00)}
    print "%(val)04X" % {"val" : mem.read_memory_word(0x00)}

    print "%(val)04X" % {"val" : mem.read_memory_word(0x01)}
    mem.write_memory_word(0x01, 0xDEAD)
    print "%(val)04X" % {"val" : mem.read_memory_word(0x01)}
    print "%(val)02X" % {"val" : mem.read_memory_byte(0x02)}
    print "%(val)02X" % {"val" : mem.read_memory_byte(0x03)}

