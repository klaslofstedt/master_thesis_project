# MySerial.py
import time
import serial
import MyFiles

class MySerial:
    buffer = 1000
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
        wait = 0
        tempSize = int(math.ceil(tempFile.File_GetSize()/float(1000)))
        
        print "tempSize", tempSize
        tempFile.File_Open()

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
        wait = 0.1
        ############################### SET FILE SIZE STATICALLY ###
        Size = 40
        print "loop times: ", Size
        data = 0
        for x in range(0, Size):
            data = self.ser.read(1000)
            self.ser.write("1")
            #put the data in a file
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        print "finished"
