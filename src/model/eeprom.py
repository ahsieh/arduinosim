#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Atmega EEPROM Structure
class AVREeprom:
    # Instance variables
    size = 0

    # Override methods
    # Initialization
    def __init__(self, size):
        self.size = size
        self.eeprom= [0x00] * size

    # String Representation
    def __str__(self):
        return "EEPROM Size: " + str(len(self.eeprom))

    # Instance functions
    # Write eeprom location (byte addressed)
    def write_eeprom_byte(self, address, value):
        self.eeprom[address] = value & 0xFF

    # Read eeprom location (byte addressed)
    def read_eeprom_byte(self, address):
        return self.eeprom[address]

    # Write eeprom location (word addressed i.e. 16-bit)
    def write_eeprom_word(self, address, value):
        word_addr = address << 1
        self.eeprom[word_addr] = value & 0xFF
        self.eeprom[word_addr + 1] = (value >> 8) & 0xFF

    # Read eeprom location (word addressed i.e. 16-bit)
    def read_eeprom_word(self, address):
        word_addr = address << 1
        msb = (self.eeprom[word_addr + 1] << 8) & 0xFF00
        lsb = self.eeprom[word_addr] & 0xFF
        return (msb | lsb)


# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    eeprom = AVREeprom(512)
    print eeprom

    print "8-bit addressing"
    print "%(val)02X" % {"val" : eeprom.read_eeprom_byte(0x00)}
    eeprom.write_eeprom_byte(0x00, 0xAA)
    eeprom.write_eeprom_byte(0x01, 0x55)
    print "%(val)02X" % {"val" : eeprom.read_eeprom_byte(0x00)}
    print "%(val)04X" % {"val" : eeprom.read_eeprom_word(0x00)}

    print "16-bit addressing"
    print "%(val)04X" % {"val" : eeprom.read_eeprom_word(0x01)}
    eeprom.write_eeprom_word(0x01, 0xDEAD)
    print "%(val)04X" % {"val" : eeprom.read_eeprom_word(0x01)}
    print "%(val)02X" % {"val" : eeprom.read_eeprom_byte(0x02)}
    print "%(val)02X" % {"val" : eeprom.read_eeprom_byte(0x03)}

