import sys
import os
import socket
import time

samples = 100
delay = 1

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
        global ts1
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Waiting for server...", count
        while self.isOpen == False:
            try:
                ts1 = time.time()
                self.conn.connect((self.host, self.port))
                self.isOpen = True
            except:
                count += 1
                print "Waiting for server...", count
                self.isOpen = False
                time.sleep(1)
        print "Successfully connected to server!"

    def TCP_SendPiece(self, data):
        global ts2
        ts2 = time.time()
        self.conn.send(str(data))
        self.conn.close()
        self.isOpen = False

    def TCP_SendFile(self, tempFile):
        global ts2
        tempFile.File_Open()
        ts2 = time.time()
        for piece in tempFile.File_Read(1024):
            self.conn.send(piece)
        self.conn.close()
        # needed?
        self.isOpen = False

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
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.conn.close()
        print "output.txt created"
        self.isOpen = False

    def TCP_RefreshToServer(self):
        count = 0
        global ts
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Waiting for server...", count
        while self.isOpen == False:
            try:
                ts = time.time()
                self.conn.connect((self.host, self.port))
                self.isOpen = True
                if self.isOpen == True:
                    print "open"
                    time.sleep(0.5)
                    self.conn.close()
                    self.isOpen = False
            except:
                count += 1
                print "Waiting for server...", count
                self.isOpen = False
                time.sleep(0.5)

class MyFiles:
    # Functions concerning input/output files
    def __init__(self, fileTemp):
        self.fileTemp = fileTemp
        self.fileOpen = False
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


# SERVER (connect to client, RPi_2)
# initialize the TCP/IP connection for eth0 (pi_1 & pi_2)
#client = MyTCP("169.254.0.2", 5010)
#client.TCP_ConnectToServer()
# CLIENT (connect to server, PC)
# initialize the TCP/IP connection for wlan0 (pi_1 & pi_2)
client = MyTCP("192.168.199.118", 5525)
logFile = MyFiles("../logs/tcp_startup.txt")
logFile.File_Remove()
#logFile.File_Push("startup times:")
totalTime = 0
print "start"
dataOut = 0
startupAverage = 0
sendtimeAverage = 0
outSize = sys.getsizeof(dataOut)
print "File Size: ", outSize
#print "Size: ", sys.getsizeof(dataOut)
for x in range(0, samples):
    time.sleep(1)
    client.TCP_ConnectToServer()
    startup = time.time() - ts1
    startupAverage += startup
    client.TCP_SendPiece(dataOut)
    #client.TCP_SendFile(fileOut)
    sendtime = time.time() - ts2
    logFile.File_List(str(startup))
    sendtimeAverage += sendtime
startupAverage = startupAverage / samples
sendtimeAverage = sendtimeAverage / samples
#logFile.File_Push('\n' + "Average throughput (kB): " + str(outSize / (sendtimeAverage * 1000)))
print "startup: ", startupAverage
#print "sendtime: ", sendtimeAverage
#print "throughput: ", (sys.getsizeof(dataOut) / sendtimeAverage)
print "throughput: ", (os.path.getsize("../input_medium.mp4") / sendtimeAverage)
logFile.File_Push("Average startup time: " + str(startupAverage))
logFile.File_Push("Average send time: " + str(sendtimeAverage))
#logFile.File_Push("Throughput: " + str((sys.getsizeof(str(dataOut)) / sendtimeAverage)))
'''
for x in range(0, samples):
    time.sleep(3)
    client.TCP_RefreshToServer()
    startupTime = ts - time.time()
    totalTime += startupTime
    print "Refreshed"
averageTime = totalTime / samples
print "Average startup time: ", averageTime
'''
'''
print "Create file object"
file1 = MyFiles("100output.txt")
file1.File_Open()
for x in range(0, samples):
    client.TCP_ConnectToServer()
    client.TCP_SendFile(file1)
    time.sleep(delay)

file1 = MyFiles("2output.txt")
file1.File_Open()
for x in range(0, samples):
    client.TCP_ConnectToServer()
    client.TCP_SendFile(file1)
    time.sleep(delay)
'''
