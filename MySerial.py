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

    def Serial_Flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()

    def Serial_Open(self):
        global ts1
        wait = 0.1
        try:
        #if self.isOpen == False:
            ts1 = time.time()
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baud, 
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 100,
                writeTimeout = 2)
            self.isOpen = True
            print "Serial port ", self.port, " open"
        except SerialException:
            print "Error port already in use"
        self.Serial_Flush()

    def Serial_SendFile(self, tempFile):
        global ts2
        wait = 0
        tempSize = int(math.ceil(tempFile.File_GetSize()/float(1000)))
        
        print "tempSize", tempSize
        tempFile.File_Open()
        ts2 = time.time()

        flag = 0
        flag2 = 0
        for piece in tempFile.File_Read(1000):
            self.ser.write(piece)
            time.sleep(wait)
            acc = self.ser.read()
            if acc == "1":
                #print acc
                if flag == 10:
                    print acc, "flag2 :", flag2
                    flag = 0
            else:
                print "fail: ", acc
            flag += 1
            flag2 += 1
        print "finished"
    
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
