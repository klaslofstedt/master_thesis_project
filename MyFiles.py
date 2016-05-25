# MyFiles.py
import os
import tkFileDialog as fd

class MyFiles:
    # Functions concerning input/output files
    def __init__(self, fileTemp):
        self.fileTemp = fileTemp
        self.isOpen = False
        self.fileSize = 0
        self.fileOpen = object

    def File_Remove(self):
        try:
            os.remove(self.fileTemp)
        except OSError:
            pass

    def File_Open(self):
        self.fileOpen = open(self.fileTemp)

    def File_Browse(self):
        self.fileTemp = fd.askopenfilename()
        print "Using file: ", self.fileTemp
        self.fileSize = os.path.getsize(self.fileTemp)
        if self.fileSize > 1000*1000:
            print "File size: ", self.fileSize / (1000*1000), "MB"
        elif self.fileSize > 1000:
            print "File size: ", self.fileSize / 1000, "kB"
        else:
            print "File size: ", self.fileSize, " bytes"
        self.isOpen = True

    def File_Read(self, size = 1024):
        while True:
            data = self.fileOpen.read(size)
            if not data:
                break
            yield data
