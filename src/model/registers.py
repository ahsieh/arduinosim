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
    def __init__(self):
        self.sp = [0x00] * 2    # 16-bit stack pointer register

    # String Representation
    def __str__(self):
        val_low = self.sp[0] & 0xFF
        val_high = (self.sp[1] << 8) & 0xFF00
        return "SP: %(v)04X" % { "v" : (val_high | val_low) }

    # Instance functions
    # Write to Stack Pointer Register
    def write_sp(self, value):
        self.sp[0] = value & 0xFF
        self.sp[1] = (value >> 8) & 0xFF

    # Write to Stack Pointer Register Low Byte (SPL)
    def write_spl(self, value):
        self.sp[0] = value & 0xFF

    # Write to Stack Pointer Register High Byte (SPH)
    def write_sph(self, value):
        self.sp[1] = value & 0xFF

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

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    regs = AVRGeneralPurposeWorkingRegisters()
    print regs

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

    print regs

    print "Testing Stack Pointer Register"
    sp = AVRStackPointerRegister()
    print sp
    sp.write_sp(0xDEAD)
    print "%(val)04X" % { "val" : sp.read_sp() }
    print "%(val)02X" % { "val" : sp.read_spl() }
    print "%(val)02X" % { "val" : sp.read_sph() }
    sp.write_spl(0xAA)
    sp.write_sph(0x55)
    print "%(val)04X" % { "val" : sp.read_sp() }

