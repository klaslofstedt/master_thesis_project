import threading
import time

class serialThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print "start serial"
        serialWrite()
        print "finished serial"

class tcpThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print "start tcp"
        tcpWrite()
        print "finished tcp"

def serialWrite():
    for x in range(0, 5):
        print "sent serial"
        time.sleep(1)

def tcpWrite():
    for x in range(0, 10):
        print "sent tcp"
        time.sleep(0.5)

thread1 = serialThread()
thread2 = tcpThread()

thread1.start()
thread2.start()

print "do main stuff"
for x in range(0, 20):
    print "main"
    time.sleep(0.25)
