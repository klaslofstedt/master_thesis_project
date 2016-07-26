# client.py (for Rpi_1):
from MyTCP import MyTCP
from MySerial import MySerial
from MyFiles import MyFiles
import time
import threading

class serialThread(threading.Thread):
    def __init__(self, tempMySerial, tempFile):
        threading.Thread.__init__(self)
        self.tempMySerial = tempMySerial
        self.tempFile = tempFile

    def run(self):
        print "Start serial"
        serialRead()
        print "Finished serial"

class tcpThread(threading.Thread):
    def __init__(self, tempMyTCP, tempFile):
        threading.Thread.__init__(self)
        self.tempMyTCP = tempMyTCP
        self.tempFile = tempFile

    def run(self):
        print "Start tcp"
        self.tempMyTCP.TCP_ReceiveToFile(self.tempFile)
        print "Finished tcp"

def serialRead():
    for x in range(0, 20):
        print "Receiving lot of serial data"
        time.sleep(1)

# Connect to RPI1 and create empty files
file1 = MyFiles("file1.txt")
file_tcp = MyFiles("file_tcp.txt")
file_zigbee = MyFiles("file_zigbee.txt")
file1.File_Remove()
file_tcp.File_Remove()
file_zigbee.File_Remove()
print "Waiting on data from RPi_1 on wlan0..."
server = MyTCP("192.168.199.118", 5519)
server.TCP_ConnectToClient()
ts = time.time()

# Open serial port for zigbee
xbee = MySerial("/dev/ttyUSB0", 115200)
xbee.Serial_Open()

# Multi-thread the transmissions
thread1 = tcpThread(server, file1)
thread2 = serialThread(xbee, file_zigbee)

# Start the threads
thread1.start()
thread2.start()

# Wait until both threads are finished until processing of data
while (thread1.isAlive() or thread2.isAlive()):
    time.sleep(0.5)
print "Threads are finished"

# TODO merge the two files into one
#server.TCP_ReceiveToFile(outputFile)
#xbee.Serial_ReadFile(outputFile)


transferTime = str(time.time() - ts)
print "Transfer Time: ", transferTime
server.TCP_ConnectToClient()
server.TCP_SendPiece(transferTime)
