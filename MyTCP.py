# MyTCP.py 
import time
import socket
import MyFiles

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

    def TCP_SendFile(self, tempFile, buffer = 1024):
        tempFile.File_Open()
        for piece in tempFile.File_Read(buffer):
            self.conn.send(piece)
        self.conn.close()
        self.isOpen = False

    # is really a TCP_ReceiveString()
    def TCP_ReceivePiece(self, buffer = 1024):
        data = self.conn.recv(buffer)
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
