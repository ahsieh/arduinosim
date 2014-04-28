#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Generic Register Object
class AVRMemoryByte(object):
    # Instance variables
    size_in_bytes = 1
    addr = 0x0000
    contents = 0x00
    read_bitmask = 0xFF
    write_bitmask = 0xFF

    # Override methods
    # Initialization
    def __init__(self, addr, contents=0x00):
        self.addr = addr
        self.contents = contents & 0xFF

    # String Representation
    def __str__(self):
        return "mem @0x%(addr)02X: 0x%(val)02X" % \
                { "addr" : self.addr , "val" : self.read() }

    # Object Comparison
    # TODO

    # Instance methods
    # Read memory contents
    def read(self):
        return self.contents & self.read_bitmask

    # Modify memory contents
    def write(self, contents):
        self.contents = contents & self.write_bitmask

    # Increment memory contents
    # Return 1 if overflow occurs, 0 otherwise
    def incr(self):
        retval = 0
        result = self.contents + 1
        if (result > 0xFF):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Decrement memory contents
    # Return 1 if overflow occurs, 0 otherwise
    def decr(self):
        retval = 0
        result = self.contents - 1
        if (result < 0):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Add to memory contents
    # Return 1 if overflow occurs, 0 otherwise
    def add(self, value):
        retval = 0
        result = self.contents + value
        if (result > 0xFF):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

    # Subtract from memory contents
    # Return 1 if overflow occurs, 0 otherwise
    def sub(self, value):
        retval = 0
        result = self.contents - value
        if (result < 0):
            retval = 1
        self.contents = result & self.write_bitmask
        return retval

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    print "Creating new memory byte object"
    mem = AVRMemoryByte(0x00)
    print mem

    print "Writing 0xAA to memory byte"
    mem.write(0xAA)
    print mem

    print "Writing 0x3F to memory byte"
    mem.write(0x3F)
    print mem

    print "Writing 0xFE to memory byte"
    mem.write(0xFE)
    print mem

    print "Incrementing memory byte (should be 0xFF, no overflow/carry)"
    ovf = mem.incr()
    print str(mem) + " overflow: " + str(ovf)

    print "Incrementing memory byte (should be 0x00 with overflow/carry)"
    ovf = mem.incr()
    print str(mem) + " overflow: " + str(ovf)

    print "Decrementing memory byte (should be 0xFF with overflow/carry)"
    ovf = mem.decr()
    print str(mem) + " overflow: " + str(ovf)

    print "Decrementing memory byte (should be 0xFE, no overflow/carry)"
    ovf = mem.decr()
    print str(mem) + " overflow: " + str(ovf)

