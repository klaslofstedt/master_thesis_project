# client.py (for Rpi_1):
import MyTCP
import MySerial
import MyFiles
import time

xbee = MySerial("/dev/ttyUSB0", 115200)
xbee.Serial_Open()
# SERVER (connect to client, RPi_2)
# initialize the TCP/IP connection for eth0 (pi_1 & pi_2)
#client = MyTCP("169.254.0.2", 5010)
#client.TCP_ConnectToServer()
# CLIENT (connect to server, PC)
# initialize the TCP/IP connection for wlan0 (pi_1 & pi_2)
print "Create file object"
outputFile = MyFiles("output.txt")
print "Remove old file"
outputFile.File_Remove()
print "Waiting on data from RPi_1 on wlan0..."
server = MyTCP("192.168.199.118", 5512)
#ts = time.time()
'''
server.TCP_ConnectToClient()
server.TCP_ReceiveToFile(outputFile)
'''
###################################### max buffer 1024 or 1020?
xbee.Serial_ReadFile(outputFile)
transferTime = time.time() - ts
print "Program finished!"
print "Transfer Time: ", transferTime
server.TCP_ConnectToClient()
server.TCP_SendPiece(transferTime)
