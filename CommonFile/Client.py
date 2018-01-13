
# -*- coding: UTF-8 -*-
import socket
class Client:
    def __init__(self, ip, port=0):
        self.state = False
        self.ip = ip
        self.port = port
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def onReceive(self):
        if not self.state:
            print ("connect First!")
            return
        buffer = []
        while True:
            d = self.sk.recv(1024).decode('utf-8')
            d = int(d)
            if d:
                print(d)
                return d

    def onSend(self,instruct):
        if self.state == False:
            print ("connect First!")
            return
        self.sk.send(instruct)
        print ('Sending '+instruct)

    def connect(self):
        try:
            self.sk.connect((self.ip, self.port))
        except Exception:
            print ("Error:Connecting")

        self.state = True
        print ('Connection:')
        print (self.ip, self.port)

    def close(self):
        self.sk.close()


def main():
    tr = Client('localhost', 49435)
    tr.connect()
    tr.onReceive()
    tr.onSend(26)
    tr.close()

if __name__ == '__main__':
    main()
