# client.py (for PC, but server for Rpi_2):
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
        serialWrite()
        print "Finished serial"

class tcpThread(threading.Thread):
    def __init__(self, tempMyTCP, tempFile):
        threading.Thread.__init__(self)
        self.tempMyTCP = tempMyTCP
        self.tempFile = tempFile

    def run(self):
        print "Start tcp"
        self.tempMyTCP.TCP_SendFile(self.tempFile)
        print "Finished tcp"

def serialWrite():
    for x in range(0, 20):
        print "Sending lots of serial data"
        time.sleep(1)

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

#while True:
# Connect to PC to get the file that should be processed
client = MyTCP("192.168.199.203", 5473)
client.TCP_ConnectToServer()
file1 = MyFiles("file1.txt")
print "Remove old file"
file1.File_Remove()
print "Waiting on data from PC..."
client.TCP_ReceiveToFile(file1)
print "Received file from PC"

# TODO Calculate variables here
# split file1 into file_tcp file_zigbee file_bluetooth
file_tcp = MyFiles("file_tcp.txt")
file_zigbee = MyFiles("file_zigbee.txt")
file_tcp.File_Remove()
file_zigbee.File_Remove()

# Open serial port for Zigbee
xbee = MySerial("/dev/ttyUSB0", 115200)
xbee.Serial_Open()
#xbee.Serial_SendFile(file1)

# Connect to RPI2
client = MyTCP("192.168.199.118", 5519)
client.TCP_ConnectToServer()

# Multi-thread the transmissions
thread1 = tcpThread(client, file1)
thread2 = serialThread(xbee, file_zigbee)

# Start the threads
thread1.start()
thread2.start()
print "threads started"

# Connect to PC again to transmit results
while (thread1.isAlive() or thread2.isAlive()):
    time.sleep(0.5)

print "threads are finished"
client.TCP_ConnectToServer()
transferTime = client.TCP_ReceivePiece()
# Transfer time is fucky. Starts when the program starts rather
# than when the transmission starts
print "Transfer time: ", transferTime
client = MyTCP("192.168.199.203", 5473)
client.TCP_ConnectToServer()
client.TCP_SendPiece(transferTime)
# Main loop does nothing
#for x in range(0, 1):
#    print "Waiting for transmission to finish."
