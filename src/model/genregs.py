#!/usr/bin/python

# Imports -------------------------------------------------------------------

# Classes -------------------------------------------------------------------
## Atmega General Purpose Working Registers
class AVRGeneralPurposeWorkingRegisters:
    # Instance variables
    size = 0

    # Override methods
    # Initialization
    def __init__(self):
        self.R = [0x00] * 32    # 32 General Purpose Registers

    # String Representation
    def __str__(self):
        retstr = "AVR General Purpose Working Registers\r\n"
        for i in xrange(32):
            retstr = retstr + "R[" + str(i) + "] = " + str(self.R[i]) + "\r\n"
        return retstr

    # Instance functions
    # Increment register value
    def incr_reg(self, index):
        self.R[index] = (self.R[index] + 1) & 0xFF

    # Decrement register value
    def decr_reg(self, index):
        self.R[index] = (self.R[index] - 1) & 0xFF

    # Add to register value (no carry)
    def add_reg(self, index, value):
        value = value & 0xFF
        self.R[index] = (self.R[index] + value) & 0xFF

    # Add to register value (with carry)
    # Return 1 if carry should be set, 0 otherwise
    def addc_reg(self, index, value):
        retval = 0
        value = value & 0xFF
        summation = self.R[index] + value
        if (summation & 0x100 > 0):
            retval = 1
        self.R[index] = summation & 0xFF
        return retval

    # Subtract from register value (no carry)
    def sub_reg(self, index, value):
        value = value & 0xFF
        self.R[index] = (self.R[index] - value) & 0xFF

    # Subtract from register value (with carry)
    def subc_reg(self, index, value):
        retval = 0
        value = value & 0xFF
        subtraction = self.R[index] - value
        if (subtraction < 0):
            retval = 1
        self.R[index] = subtraction & 0xFF
        return retval

    # Write to a register
    def write_reg(self, index, value):
        self.R[index] = value & 0xFF

    # Read from a register
    def read_reg(self, index):
        return self.R[index] & 0xFF

    # Write to the X-register
    def write_xreg(self, value):
        self.R[26] = value & 0xFF
        self.R[27] = (value >> 8) & 0xFF

    # Write to the X-register Low Byte
    def write_xlreg(self, value):
        self.R[26] = value & 0xFF

    # Write to the X-register High Byte
    def write_xhreg(self, value):
        self.R[27] = (value >> 8) & 0xFF

    # Read from the X-register
    def read_xreg(self):
        low = self.R[26] & 0xFF
        high = (self.R[27] << 8) & 0xFF00
        return (high | low)

    # Read from the X-register Low Byte
    def read_xlreg(self):
        return self.R[26] & 0xFF

    # Read from the X-register High Byte
    def read_xhreg(self):
        return self.R[27] & 0xFF

    # Write to the Y-register
    def write_yreg(self, value):
        self.R[28] = value & 0xFF
        self.R[29] = (value >> 8) & 0xFF

    # Write to the Y-register Low Byte
    def write_ylreg(self, value):
        self.R[28] = value & 0xFF

    # Write to the Y-register High Byte
    def write_yhreg(self, value):
        self.R[29] = (value >> 8) & 0xFF

    # Read from the Y-register
    def read_yreg(self):
        low = self.R[28] & 0xFF
        high = (self.R[29] << 8) & 0xFF00
        return (high | low)

    # Read from the Y-register Low Byte
    def read_ylreg(self):
        return self.R[28] & 0xFF

    # Read from the Y-register High Byte
    def read_yhreg(self):
        return self.R[29] & 0xFF

    # Write to the Z-register
    def write_zreg(self, value):
        self.R[30] = value & 0xFF
        self.R[31] = (value >> 8) & 0xFF

    # Write to the Z-register Low Byte
    def write_zlreg(self, value):
        self.R[30] = value & 0xFF

    # Write to the Z-register High Byte
    def write_zhreg(self, value):
        self.R[31] = (value >> 8) & 0xFF

    # Read from the Z-register
    def read_zreg(self):
        low = self.R[30] & 0xFF
        high = (self.R[31] << 8) & 0xFF00
        return (high | low)

    # Read from the Z-register Low Byte
    def read_zlreg(self):
        return self.R[30] & 0xFF

    # Read from the Z-register High Byte
    def read_zhreg(self):
        return self.R[31] & 0xFF

## Atmega Stack Pointer Register
class AVRStackPointerRegister:
    # Override methods
    # Initialization
    def __init__(self, ram_size):
        self.sp = [0x00] * 2    # 16-bit stack pointer register
        self.ram_size = ram_size
        self.write_sp(ram_size - 1)

    # String Representation
    def __str__(self):
        val_low = self.sp[0] & 0xFF
        val_high = (self.sp[1] << 8) & 0xFF00
        return "SP: %(v)04X" % { "v" : (val_high | val_low) }

    # Instance functions
    # Increment Stack Pointer 
    def incr_sp(self, inc):
        val = self.read_sp()
        val = val + inc
        self.write_sp(val)

    # Decrement Stack Pointer 
    def decr_sp(self, dec):
        val = self.read_sp()
        val = val - dec
        self.write_sp(val)

    # Write to Stack Pointer Register
    def write_sp(self, value):
        value = value & (self.ram_size - 1)
        self.sp[0] = value & 0xFF
        self.sp[1] = (value >> 8) & 0xFF

    # Write to Stack Pointer Register Low Byte (SPL)
    def write_spl(self, value):
        self.sp[0] = value & 0xFF & (self.ram_size - 1)

    # Write to Stack Pointer Register High Byte (SPH)
    def write_sph(self, value):
        self.sp[1] = value & 0xFF & ((self.ram_size - 1) >> 8)

    # Read from Stack Pointer Register
    def read_sp(self):
        val_low = self.sp[0] & 0xFF
        val_high = (self.sp[1] << 8) & 0xFF00
        return (val_high | val_low)

    # Read from Stack Pointer Register Low Byte (SPL)
    def read_spl(self):
        return self.sp[0]

    # Read from Stack Pointer Register High Byte (SPH)
    def read_sph(self):
        return self.sp[1]

## ATmega Flag Class
class AVRSregFlags:
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
class AVRSreg:
    # Instance variables
    flags = [None] * 8
    status_reg = 0b00000000

    # Override methods
    # Initialization
    def __init__(self):
        # Setup the flags in the status register
        self.flags[0] = AVRSregFlags("C", 0b00000001, "Carry Flag")
        self.flags[1] = AVRSregFlags("Z", 0b00000010, "Zero Flag")
        self.flags[2] = AVRSregFlags("N", 0b00000100, "Negative Flag")
        self.flags[3] = AVRSregFlags("V", 0b00001000, "Overflow Flag")
        self.flags[4] = AVRSregFlags("S", 0b00010000, "Sign Bit (N xor V)")
        self.flags[5] = AVRSregFlags("H", 0b00100000, "Half Carry Flag")
        self.flags[6] = AVRSregFlags("T", 0b01000000, "Bit Copy Storage")
        self.flags[7] = AVRSregFlags("I", 0b10000000, "Global Interrupt Enable")

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

        
# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    regs = AVRGeneralPurposeWorkingRegisters()
    print regs

    print "Testing General Purporse Working Registers"
    print "Testing X register"
    regs.write_xreg(0xDEAD)
    print "%(val)04X" % {"val" : regs.read_xreg()}
    regs.write_xlreg(0x32)
    print "%(val)04X" % {"val" : regs.read_xreg()}
    regs.write_xhreg(0xFF)
    print "%(val)04X" % {"val" : regs.read_xreg()}
    regs.write_reg(26, 0xCD)
    regs.write_reg(27, 0xAB)
    print "%(val)04X" % {"val" : regs.read_xreg()}

    print "Testing Y register"
    regs.write_yreg(0xDEAD)
    print "%(val)04X" % {"val" : regs.read_yreg()}
    regs.write_ylreg(0x32)
    print "%(val)04X" % {"val" : regs.read_yreg()}
    regs.write_yhreg(0xFF)
    print "%(val)04X" % {"val" : regs.read_yreg()}
    regs.write_reg(28, 0xCD)
    regs.write_reg(29, 0xAB)
    print "%(val)04X" % {"val" : regs.read_yreg()}

    print "Testing Z register"
    regs.write_zreg(0xDEAD)
    print "%(val)04X" % {"val" : regs.read_zreg()}
    regs.write_zlreg(0x32)
    print "%(val)04X" % {"val" : regs.read_zreg()}
    regs.write_zhreg(0xFF)
    print "%(val)04X" % {"val" : regs.read_zreg()}
    regs.write_reg(30, 0xCD)
    regs.write_reg(31, 0xAB)
    print "%(val)04X" % {"val" : regs.read_zreg()}

    regs.incr_reg(30)
    regs.decr_reg(31)
    print "%(val)04X" % {"val" : regs.read_zreg()}

    print regs

    print "Testing Stack Pointer Register"
    sp = AVRStackPointerRegister(32768)
    print sp
    sp.write_sp(0xDEAD)
    print "%(val)04X" % { "val" : sp.read_sp() }
    print "%(val)02X" % { "val" : sp.read_spl() }
    print "%(val)02X" % { "val" : sp.read_sph() }
    sp.write_spl(0xAA)
    sp.write_sph(0x55)
    print "%(val)04X" % { "val" : sp.read_sp() }

    sp.incr_sp(1)
    print "%(val)04X" % { "val" : sp.read_sp() }
    sp.incr_sp(2)
    print "%(val)04X" % { "val" : sp.read_sp() }
    sp.decr_sp(1)
    print "%(val)04X" % { "val" : sp.read_sp() }
    sp.decr_sp(2)
    print "%(val)04X" % { "val" : sp.read_sp() }
    
    print "Testing Status Register"
    sreg = AVRSreg()
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

