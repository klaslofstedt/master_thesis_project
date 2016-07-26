from MyFiles import MyFiles
from MyTCP import MyTCP
from MySerial import MySerial
import math
import Tkinter as tk
import sys
import glob
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
        #sys.stderr = MyTextRedirector(self.text, "stderr")

        #serial1.port = tk.StringVar(self)
        #serial1.port.set("Open Port")
        #m1 = tk.OptionMenu(self, serial1.port, *Serial_Ports())
        #m1.config(height = 1, width = 10)
        b1 = tk.Button(text = "Open File", command = file1.File_Browse) #.grid(row = 0, column = 1).config(height=1, width= gridWidth)
        b1.config(height = 1, width = 10)
        #b3 = tk.Button(text = "Connect TCP/IP", command = server.TCP_ConnectToClient) #.grid(row = 0, column = 1).config(height=1, width= gridWidth)
        #b3.config(height = 1, width = 10)
        l1 = tk.Label(self, text="Param#1")
        e1 = tk.Entry(self)
        e1.insert(0,"0")
        l2 = tk.Label(self, text="Param#2")
        e2 = tk.Entry(self)
        e2.insert(0,"0")
        b2 = tk.Button(text = "Run", command = Run)
        #m1.pack(in_=toolbar, side="left")
        b1.pack(in_=toolbar, side="left")
        #b3.pack(in_=toolbar, side="left")
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

'''
def Serial_Ports():
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
'''

def Run():
    '''
    if serial1.port.get() == ("Open Port"):
        sys.stderr.write("Error: No serial port open\n")
        if file1.isOpen == False:
            sys.stderr.write("Error: No file open\n")
        else:
            pass
    else:
    '''
    if file1.isOpen == False:
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
        for piece in File_Read(infile):
            usb.write(piece)
            time.sleep(0.0005)
        usb.close()
        '''
        # Initialize a TCP/IP connection with RPi 1
        # Use the ip address of the client (this PC)
        server = MyTCP("192.168.199.203", 5473)
        server.TCP_ConnectToClient()

        ts = time.time()
        server.TCP_SendFile(file1)
        #file1.SendFileTCP(server)
        print "Data sent in: ", time.time() - ts, "sec"
            #with open("output.txt", "a") as outfile:
            #    outfile.write(piece)
        server.TCP_ConnectToClient()
        transferTime = server.TCP_ReceivePiece()
        print "Transfer Time: ", transferTime
            
def mainTask():
    #serial1.Serial_Open()
    app.after(1000, mainTask)

#class MyOptionMenu(tk.OptionMenu):
#    def __init__(self, master, status, *options):
#        self.var = tk.StringVar(master)
#        self.var.set(status)
#        tk.OptionMenu.__init__(self, master, self.var, *options)

# Browse a file and save the result in "output.txt"
file1 = MyFiles("output.txt")
# Initialize the USB connection
#serial1 = MySerial()
# Create the GUI
app = MyGUI()
app.title("IoT Testbedd")
# wait 100 ms for ports and stuff before running mainTask
app.after(100, mainTask) 
app.mainloop()
