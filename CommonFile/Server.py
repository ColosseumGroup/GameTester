# -*- coding: UTF-8 -*-
import socket
class Server:
    def __init__(self, ip, port):
        self.state = False
        self.accepted = False
        self.maxReceiver = 1
        self.exitFlag = False
        self.ip = ip
        self.port = port
        try:
            self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print ("Server Init")
        except socket.error :
            print ("Server Init Failed")

    def onSending(self, instruct):  # instruct should be int
        if self.state == False:
            print ("connect First!")
            return
        if self.accepted == False:
            print ("still Waiting For Receiver")
            return
        ins = b'%d' % instruct
        self.recSock.send(ins)
        print ('Send Instruct %d' % instruct)

    def onSendExitFlag(self):
        self.exitFlag = True
        self.onSending(-1)
        self.close()

    def onReceive(self):
        if not self.state:
            print ("connect First!")
            return
        buffer = []
        while True:
            d = self.recSock.recv(1024).decode('utf-8')
            if d:
                print (d)
                return d

    def bind(self):
        print ("Start binding")
        self.state = True
        try:
            print (self.ip)
            self.sk.bind((self.ip, self.port))
            print (self.getPort())
        except Exception :
            self.state = False
            print ("Error:Binding")

        if self.state == True:
            print ("Binding Succeeded:")
        print (self.ip, self.port)

    def Listening(self):
        try:
            self.sk.listen(self.maxReceiver)
        except socket.error:
            self.sk.close()
            print ("tcp Sender listen error:")

    def acceptConnection(self):
        print ("Sender Waiting For Receiver")
        self.recSock, addr = self.sk.accept()
        print ("Accepted connection address:")
        print (self.recSock)
        print (addr)
        self.accepted = True

    def getPort(self):
        addr , self.port = self.sk.getsockname()
        return self.port

    def close(self):
        self.sk.close()


def main():
    ts = Server('127.0.0.1', 0)
    ts.bind()
    ts.Listening()
    ts.acceptConnection()
    ts.onSending(22)
    ts.onReceive()
    ts.close()


if __name__ == '__main__':
    main()
