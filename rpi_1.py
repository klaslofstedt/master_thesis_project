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

    def TCP_SendFile(self, tempFile):
        tempFile.OpenFile()
        for piece in temp.ReadFile(1024):
            self.conn.send(piece)
        self.conn.close()

    def TCP_ReceiveByte(self):
        # buffer = 1
        data = self.conn.recv(1024)
        print "Received: ", data
        self.conn.close()
        return data

    def TCP_ReceiveToFile(self, tempFile):
        buffer = 1024
        while True:
            data = self.conn.recv(buffer)
            with open(tempFile.fileOutput, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.conn.close()
        print "output.txt created"

class MyFiles:
    # Functions concerning input/output files
    def __init__(self, fileOutput, fileInput = None):
        self.fileInput = fileInput
        self.fileOutput = fileOutput
        self.fileOpen = False
        self.fileSize = 0
        self.fileOpen = object

    def RemoveFile(self):
        try:
            os.remove(self.fileOutput)
        except OSError:
                pass

    def OpenFile(self):
        self.fileOpen = open(self.fileInput)

    def ReadFile(self, size = 1024):
        while True:
            data = self.fileOpen.read(size)
            if not data:
                break
            yield data

# SERVER (connect to client, RPi_2)
# initialize the TCP/IP connection for eth0 (pi_1 & pi_2)
server = MyTCP("169.254.0.2", 5006)
server.TCP_ConnectToClient()
# CLIENT (connect to server, PC)
# initialize the TCP/IP connection for eth1 (pi_1 & PC)
client = MyTCP("192.168.199.203", 5472)
client.TCP_ConnectToServer()
print "Create file object"
outputFile = MyFiles("output.txt")
print "Remove old file"
outputFile.RemoveFile()
print "Waiting on data from PC..."
client.TCP_ReceiveToFile(outputFile)
print "Program finished!"
