import sys
import os
import time
import serial

samples = 100
delay = 1

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

    def File_Read(self, size = 1024):
        while True:
            data = self.fileOpen.read(size)
            if not data:
                break
            yield data

    def File_Push(self, data):
        with open(self.fileTemp, "a") as outfile:
            outfile.write(data + '\n')

    def File_List(self, data):
        with open(self.fileTemp, "a") as outfile:
            outfile.write(data + ',')

class MySerial:
    buffer = 1024
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.isOpen = False
        self.ser = object

    def Serial_Open(self):
        global ts1
        if self.isOpen == False:
            ts1 = time.time()
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

    def Serial_SendPiece(self, data):
        global ts2
        ts2 = time.time()
        self.ser.write(data)
        self.ser.close()
        self.isOpen = False

    def Serial_SendFile(self, tempFile):
        tempFile.File_Open()
        for piece in tempFile.File_Read(MySerial.buffer):
            self.ser.write(piece)
        self.ser.close()
        self.isOpen = False

    def Serial_ReadFile(self, tempFile):
        while self.ser.inWaiting() > 0:
            data = self.ser.read(MySerial.buffer)
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.ser.close()
        print "output.txt created"
        self.isOpen = False

    #def Serial_Send(self):
xbee = MySerial("/dev/ttyUSB0", 115200)
#print "Create file object"
#file1 = MyFiles("output.txt")
#file1.File_Open()
#for x in range(0, 100):
#    xbee.Serial_Open()
#    xbee.Serial_SendFile(file1)
#    time.sleep(2)
logFile = MyFiles("../logs/serial_log.txt")
logFile.File_Remove()
#logFile.File_Push("startup times:")
totalTime = 0
print "start"
dataOut = 0
startupAverage = 0
sendtimeAverage = 0
print "Size: ", sys.getsizeof(str(dataOut))
for x in range(0, samples):
    xbee.Serial_Open()
    startup = time.time() - ts1
    startupAverage += startup
    xbee.Serial_SendPiece(str(dataOut))
    sendtime = time.time() - ts2
    logFile.File_List(str(startup))
    sendtimeAverage += sendtime
    time.sleep(delay)
startupAverage = startupAverage / samples
sendtimeAverage = sendtimeAverage / samples
print "startup: ", startupAverage
print "sendtime: ", sendtimeAverage
print "throughput: ", (sys.getsizeof(str(dataOut)) / sendtimeAverage)
#logFile.File_Push("Average startup time: " + str(startupAverage))
#logFile.File_Push("Average send time: " + str(sendtimeAverage))
#logFile.File_Push("Throughput: " + str((sys.getsizeof(str(dataOut)) / sendtimeAverage)))
