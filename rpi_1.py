# client.py (for PC, but server for Rpi_2):
import MyTCP
import MySerial
import MyFiles
import time

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
client = MyTCP("192.168.199.118", 5512)
'''
client.TCP_ConnectToServer()
client.TCP_SendFile(file1)
'''
xbee.Serial_SendFile(file1)
print "finished"
client.TCP_ConnectToServer()
transferTime = client.TCP_ReceivePiece()
print "Transfer time: ", transferTime
client = MyTCP("192.168.199.203", 5472)
client.TCP_ConnectToServer()
client.TCP_SendPiece(transferTime)
