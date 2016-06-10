import sys
import os
import socket
import time

samples = 10

class MyTCP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = object # conn = Connection
        self.isOpen = False

    def TCP_ConnectToClient(self):
        global ts
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((self.host, self.port))
        tcp.listen(1)
        self.conn, addr = tcp.accept()
        ts = time.time()
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
        self.conn.send(str(data))
        self.conn.close()

    def TCP_SendFile(self, tempFile):
        tempFile.File_Open()
        for piece in temp.File_Read(1024):
            self.conn.send(piece)
        self.conn.close()
        # needed?
        self.isOpen = False

    def TCP_ReceiveByte(self, buffer = 1024):
        # buffer = 1
        data = self.conn.recv(buffer)
        print "Received: ", data
        self.conn.close()
        return data

    def TCP_ReceiveToFile(self, tempFile, buffer = 1024):
        while True:
            data = self.conn.recv(buffer)
            with open(tempFile.fileTemp, "a") as outfile:
                outfile.write(data)
            if not data: break
        self.conn.close()
        #print "output.txt created"
        self.isOpen = False

    def TCP_Close(self):
        self.conn.close()
        self.isOpen = False

    def TCP_RefreshToClient(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((self.host, self.port))
        tcp.listen(3)
        self.conn, addr = tcp.accept()
        self.isOpen = True
        print "connected"
        '''
        if self.isOpen == True:
            time.sleep(0.5)
            self.conn.close()
            self.isOpen = False
        print "closed"
        '''

class MyFiles:
    # Functions concerning input/output files
    def __init__(self, fileTemp):
        self.fileTemp = fileTemp
        self.fileOpen = False
        self.fileSize = 0
        self.fileOpen = object

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

# SERVER (connect to client, RPi_2)
# initialize the TCP/IP connection for eth0 (pi_1 & pi_2)
#client = MyTCP("169.254.0.2", 5010)
#client.TCP_ConnectToServer()
# CLIENT (connect to server, PC)
# initialize the TCP/IP connection for wlan0 (pi_1 & pi_2)
server = MyTCP("192.168.199.118", 5525)
#logFile = MyFiles("logs/tcp_log.txt")
#outFile = MyFiles("outFile.mp4")
for x in range(0, samples):
    #outFile.File_Remove()
    server.TCP_ConnectToClient()
    #server.TCP_ReceiveToFile(outFile)
    #print "Size of file: ", os.path.getsize("outFile.mp4")
    #print "Size of file: ", sys.getsizeof(outFile)
    inData = server.TCP_ReceiveByte(1024)
    print "Size of data: ", sys.getsizeof(inData)
'''
for x in range (0, samples):
    server.TCP_RefreshToClient()
    print "refreshed"
    #time.sleep(1)
server.TCP_Close()
'''
'''
print "Create file object"
outputFile = MyFiles("output.txt")
tcpFile = MyFiles("logs/100_tcp_log.txt")
print "Remove old files"
outputFile.File_Remove()
tcpFile.File_Remove()
print "100-------------------------------"
totalTime100 = 0
transferTime100 = 0
transfers100 = []
for x in range(0, samples):
    server.TCP_ConnectToClient()
    server.TCP_ReceiveToFile(outputFile, 100)
    transferTime100 = time.time() - ts
    transfers100.append(transferTime100)
    totalTime100 += transferTime100
    tcpFile.File_Push(str(transferTime100))
transfers100.sort()
totalTime100 = (totalTime100 - transfers100[0] - transfers100[samples - 1])/ (samples -2)
print "Average Time: ", totalTime100
fileSize100 = outputFile.File_Size() / samples
print "File Size: ", fileSize100
logFile.File_Push("Average time (" + str(fileSize100) + " bytes)"+ str(totalTime100))

print "Bytes per second: ", fileSize100/transferTime100


print "2---------------------------------"
outputFile = MyFiles("output.txt")
tcpFile = MyFiles("logs/2_tcp_log.txt")
print "Remove old files"
outputFile.File_Remove()
tcpFile.File_Remove()
totalTime2 = 0
transferTime2 = 0
transfers2 = []
for x in range(0, samples):
    server.TCP_ConnectToClient()
    server.TCP_ReceiveToFile(outputFile, 2)
    transferTime2 = time.time() - ts
    transfers2.append(transferTime2)
    totalTime2 += transferTime2
    tcpFile.File_Push(str(transferTime2))
transfers2.sort()
totalTime2 = (totalTime2 - transfers2[0] - transfers2[samples -1]) / (samples -2)
logFile.File_Push("Average time (100 bytes) " + str(totalTime100))
print "Average Time: ", totalTime2
fileSize2 = outputFile.File_Size() / samples
print "File Size: ", fileSize2
logFile.File_Push("Average time (" + str(fileSize2) + " bytes)"+ str(totalTime2))
print "Bytes per second: ", fileSize2/transferTime2
print "---------------------------------"
#logFile.File_Remove()
one_byte = ((totalTime100) - (totalTime2)) / (fileSize100 - fileSize2)
print "1 byte: ", one_byte
startupTime = (totalTime100) - (fileSize100 * one_byte)
print "startup time: ", startupTime
print "throughput: ", 1 / one_byte, "bytes/s"
logFile.File_Push("1 byte: " + str(one_byte))
logFile.File_Push("Startup Time: " + str(startupTime))
logFile.File_Push("Throughput: " + str(1 / one_byte) + " bytes/s")
'''
