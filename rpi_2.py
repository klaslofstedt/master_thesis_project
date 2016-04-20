# Clean this shit up
# client.py
import socket
import time
import serial

# CLIENT
# initialize the TCP/IP connection for eth0 (pi_1 & pi_2)
host = "169.254.0.2" # use the ip (PC wifi) address of the client (server)
port = 5006
buffer = 1024
data = "hello"
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketOpen = 0
count = 0
print "Waiting for server...", count
while socketOpen == 0:
    try:
        s.connect((host, port))
        socketOpen = 1
    except:
        count += 1
        print "Waiting for server...", count
        socketOpen = 0
        time.sleep(1)
print "Successfully connected to server!"

def receiveTCP():
    print "Receiving data from server..."
    while True:
        data = s.recv(buffer)
        if not data: break
        s.send(data) # echo
        print "Received: ", data
    s.close()

def sendTCP():
    print "Sending data to Rpi_2..."
    counter = 0
    while counter < 10:
        s.send(data)
        answer = s.recv(buffer)
        print "Sent: ", data
        print "Echo: ", answer
        time.sleep(1)
        counter += 1
    s.close()

receiveTCP()
#sendTCP()
print "Program finished!"
