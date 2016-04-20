import math
import socket
import Tkinter as tk
import sys
import glob
import os
import serial
import time
import tkFileDialog as fd

class MyGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")

        self.text = tk.Text(self, wrap="word")
        self.text.pack(side="top", fill="both", expand=True) # width?
        self.text.tag_configure("stderr", foreground="#b22222") # error color
        sys.stdout = MyTextRedirector(self.text, "stdout")
        sys.stderr = MyTextRedirector(self.text, "stderr")

        serial1.port = tk.StringVar(self)
        serial1.port.set("Open Port")
        m1 = tk.OptionMenu(self, serial1.port, *serialPorts())
        m1.config(height = 1, width = 10)
        b1 = tk.Button(text = "Open File", command = file1.BrowseFile) #.grid(row = 0, column = 1).config(height=1, width= gridWidth)
        b1.config(height = 1, width = 10)
        b3 = tk.Button(text = "Connect TCP/IP", command = tcpRpi1.ConnectTcp) #.grid(row = 0, column = 1).config(height=1, width= gridWidth)
        b3.config(height = 1, width = 10)
        l1 = tk.Label(self, text="Param#1")
        e1 = tk.Entry(self)
        e1.insert(0,"0")
        l2 = tk.Label(self, text="Param#2")
        e2 = tk.Entry(self)
        e2.insert(0,"0")
        b2 = tk.Button(text = "Run", command = Run)
        m1.pack(in_=toolbar, side="left")
        b1.pack(in_=toolbar, side="left")
        b3.pack(in_=toolbar, side="left")
        l1.pack(in_=toolbar, side="left")
        e1.pack(in_=toolbar, side="left")
        l2.pack(in_=toolbar, side="left")
        e2.pack(in_=toolbar, side="left")
        b2.pack(in_=toolbar, side="left")

class MyTextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

class MyTCP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = object
        self.tcpOpen = False

    def ConnectTcp(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((self.host, self.port))
        # Todo: a timeout to avoid program crash
        tcp.listen(1)
        self.conn, addr = tcp.accept()
        print "Successfully accepted the client!"
        self.tcpOpen = True

class MySerial:
    def __init__(self):
        self.port = None
        self.serialOpen = False

    def OpenSerial(self):
        if self.port.get() != ("Open Port"):
            if self.serialOpen == False:
                usb = serial.Serial(
                    port=self.port.get(),
                    baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)
                self.serialOpen = True
                print "Opened USB"
    
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

    def SendFileTCP(self, tempTCP):
        self.OpenFile()
        for piece in self.ReadFile(1024):
            tempTCP.conn.send(piece)
        tempTCP.conn.close()

    def OpenFile(self):
        self.fileOpen = open(self.fileInput)

    def BrowseFile(self):
        self.fileInput = fd.askopenfilename()
        print "Using file: ", self.fileInput
        self.fileSize = os.path.getsize(self.fileInput)
        if self.fileSize > 1000*1000:
            print "File size: ", self.fileSize / (1000*1000), "MB"
        elif self.fileSize > 1000:
            print "File size: ", self.fileSize / 1000, "kB"
        else:
            print "File size: ", self.fileSize, " bytes"
        self.fileOpen = True

    def ReadFile(self, size = 1024):
        while True:
            data = self.fileOpen.read(size)
            if not data:
                break
            yield data

def serialPorts():
    # Lists serial port names
    # - raises EnvironmentError on unsupported or unknown platforms
    # - returns a list of the serial ports available on the system
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        #ports = glob.glob("/dev/tty[A-Za-z]*")
        ports = glob.glob("/dev/ttyUSB*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    if len(ports) > 0:
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
    else:
        result.append("No ports available")
    return result

def Run():
    if serial1.port.get() == ("Open Port"):
        sys.stderr.write("Error: No serial port open\n")
        if file1.fileOpen == False:
            sys.stderr.write("Error: No file open\n")
        else:
            pass
    else:
        if file1.fileOpen == False:
            sys.stderr.write("Error: No file open\n")
        else:
            # Connect to USB/Serial
            print "Running..."
            '''
            if(usb.isOpen() == False):
                usb.open()
            usb.write(str(os.path.getsize(inputFile))+'\n')
            usb.close()
            time.sleep(0.05)
            if(usb.isOpen() == False):
                usb.open()
            ts = time.time()
            for piece in ReadFile(infile):
                usb.write(piece)
                time.sleep(0.0005)
            usb.close()
            '''
            ts = time.time()
            file1.SendFileTCP(tcpRpi1)
            print "Data sent in: ", time.time() - ts, "sec"
                #with open("output.txt", "a") as outfile:
                #    outfile.write(piece)
            
def mainTask():
    serial1.OpenSerial()
    app.after(1000, mainTask)

#class MyOptionMenu(tk.OptionMenu):
#    def __init__(self, master, status, *options):
#        self.var = tk.StringVar(master)
#        self.var.set(status)
#        tk.OptionMenu.__init__(self, master, self.var, *options)

# Browse a file and save the result in "output.txt"
file1 = MyFiles("output.txt")
# Initialize a TCP/IP connection with RPi 1
# Use the ip address of the client (this PC)
tcpRpi1 = MyTCP("192.168.199.203", 5472)
# Initialize the USB connection
serial1 = MySerial()
# Create the GUI
app = MyGUI()
app.title("IoT Testbedd")
# wait 100 ms for ports and stuff before running mainTask
app.after(100, mainTask) 
app.mainloop()
