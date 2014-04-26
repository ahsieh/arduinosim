#!/usr/bin/python

# Imports -------------------------------------------------------------------
from avr_flashmem import AVRFlashWord

# Classes -------------------------------------------------------------------
## Generic Register Object
class AVRFlash:
    # Instance variables
    flash_size = 0

    # Override methods
    # Initialization
    def __init__(self, def_filename):
        try:
            # Open file for reading
            f = open(def_filename, "r")

            #
            for line in f:
                if (line[0] != ";"):
                    words = line.split()
                    if (len(words) > 0):
                        if (words[0] == "FLASH" and words[1] == "="):
                            try:
                                print words[2]
                                self.flash_size = int(words[2].strip())
                                break
                            except:
                                print "**Error: FLASH definition has errors"
                                errflag = 1
                                break

            #
            if (errflag == 1):
                self.flash = []
                self.flash_size = 0
            else:
                if self.flash_size == 0:
                    self.flash_size = 2048

                for addr in xrange(0, self.flash_size):
                    self.flash.append(AVRFlashWord(addr))

            f.close()
        except:
            print "**Err: File does not exist!"

    # String Representation
    def __str__(self):
        retstr = ""
        for flash in self.flash:
            retstr = retstr + str(flash) + "\r\n"
        return retstr

    # Object Comparison
    # TODO

    # Instance methods
    # Read memister contents
    def read(self, addr):
        return self.flash[addr].read()

    # Modify memister contents
    def write(self, addr, data):
        self.flash[addr].write(data)

# Main function -------------------------------------------------------------
## Main (for testing purposes)
if __name__=="__main__":
    flash = AVRFlash("arch/atmega328p.def")
    if (flash.flash_size != 0):
        print "Hurray!"


