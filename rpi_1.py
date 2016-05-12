# client.py (for PC, but server for Rpi_2):
import os
import socket
import time
import serial

class MyTCP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = object # conn = Connection
        self.isOpen = False

    def TCP_ConnectToClient(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((self.host, self.port))
        print "Listening for server..."
        tcp.listen(1)
        self.conn, addr = tcp.accept()
        print "Successfully accepted the client!"
        self.isOpen = True

    def TCP_ConnectToServer(self):
        count = 0
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Waiting for server...", count
        while self.isOpen == False:
            try:
                self.conn.connect((self.host, self.port))
                self.isOpen = True
            except:
                count += 1
                print "Waiting for server...", count
                self.isOpen = False
                time.sleep(1)
        print "Successfully connected to server!"

    def TCP_SendPiece(self, data):
        self.conn.send(data)
        self.conn.close()
        self.isOpen = False

    def TCP_SendFile(self, tempFile):
        tempFile.File_Open()
        for piece in tempFile.File_Read(1024):
            self.conn.send(piece)
        self.conn.close()
        self.isOpen = False

    # is really a TCP_ReceiveString()
    def TCP_ReceiveByte(self):
        # buffer = 1
        data = self.conn.recv(1024)
        #print "Received: ", data
        self.conn.close()
        self.isOpen = False
        return data

    def TCP_ReceiveToFile(self, tempFile):
        buffer = 1024
        while True:
            data = self.conn.recv(buffer)
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.conn.close()
        print "output.txt created"
        self.isOpen = False

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
                port = self.port.get(),
                baudrate = baud, 
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 0)
            self.isOpen = True
            print "Serial port ", self.port, " open"
        else:
            print self.port, " is already open"

    def Serial_SendFile(self, tempFile):
        tempFile.File_Open()
        for piece in tempFile.File_Read(MySerial.buffer):
            self.write(piece)
        self.close()
        self.isOpen = False

    def Serial_ReadFile(self, tempFile):
        while self.inWaiting() > 0:
            data = self.read(MySerial.buffer)
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.close()
        print "output.txt created"
        self.isOpen = False

    #def Serial_Send(self):
xbee = MySerial("/dev/ttyUSB0", 115200)
xbee.Serial_Open()
# SERVER (connect to client, RPi_2)
# initialize the TCP/IP connection for eth0 (pi_1 & pi_2)
# IP of this eth0

# This is probably not needed since we will implement the algorithm
# on pi1 and not pi2
#server = MyTCP("169.254.0.2", 5010)
#server.TCP_ConnectToClient()
# CLIENT (connect to server, PC)
# initialize the TCP/IP connection for wlan0 (pi_1 & PC)
# IP from PC wlan0
client = MyTCP("192.168.199.203", 5472)
client.TCP_ConnectToServer()
print "Create file object"
file1 = MyFiles("output.txt")
print "Remove old file"
file1.File_Remove()
print "Waiting on data from PC..."
client.TCP_ReceiveToFile(file1)
client = MyTCP("192.168.199.118", 5505)
client.TCP_ConnectToServer()
client.TCP_SendFile(file1)
print "finished"
client.TCP_ConnectToServer()
transferTime = client.TCP_ReceiveByte()
print "Transfer time: ", transferTime
client = MyTCP("192.168.199.203", 5472)
client.TCP_ConnectToServer()
client.TCP_SendPiece(transferTime)
