# MySerial.py
import time
import serial
import MyFiles

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
