import os
import time
import serial

samples = 100

class MyFiles:
    # Functions concerning input/output files
    def __init__(self, fileTemp):
        self.fileTemp = fileTemp
        self.fileOpen = False
        self.fileSize = 0
        self.fileOpen = object
        self.fileSize = 0

    def File_Size(self):
        self.fileSize = os.path.getsize(self.fileTemp)
        return self.fileSize

    def File_Remove(self):
        try:
            os.remove(self.fileTemp)
        except OSError:
                pass

    def File_Open(self):
        self.fileOpen = open(self.fileTemp)

    def File_Read(self, size = 1024):
        while True:
            data = self.fileOpen.read(size)
            if not data:
                break
            yield data

    def File_Push(self, data):
        with open(self.fileTemp, "a") as outfile:
            outfile.write(data + '\n')

class MySerial:
    buffer = 1024
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.isOpen = False
        self.ser = object

    def Serial_Open(self):
        if self.isOpen == False:
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baud, 
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 1)
            self.isOpen = True
            print "Serial port ", self.port, " open"
        else:
            print self.port, " is already open"

    #def Serial_Send(self):
    def Serial_SendFile(self, tempFile):
        tempFile.File_Open()
        for piece in tempFile.File_Read(MySerial.buffer):
            self.ser.write(piece)
        self.ser.close()
        self.isOpen = False

    def Serial_ReadFile(self, tempFile):
        global ts
        while self.ser.inWaiting() < 1:
            pass
        ts = time.time()
        while self.ser.inWaiting() > 0:
            data = self.ser.read(MySerial.buffer)
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.ser.close()
        print "output.txt created"
        self.isOpen = False

xbee = MySerial("/dev/ttyUSB0", 115200)
print "Create file object"
outputFile = MyFiles("output.txt")
serialFile = MyFiles("serial_timestamp_log.txt")
print "Remove old files"
outputFile.File_Remove()
serialFile.File_Remove()
totalTime = 0
for x in range(0, samples):
    xbee.Serial_Open()
    xbee.Serial_ReadFile(outputFile)
    transferTime = time.time() - ts
    totalTime += transferTime
    serialFile.File_Push(str(transferTime))
print "Transfer Time: ", transferTime
print "Average Time: ", totalTime / 100
fileSize = outputFile.File_Size()
print "File Size: ", fileSize
print "Bytes per second: ", fileSize/transferTime
