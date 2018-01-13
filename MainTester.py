# -*- coding: utf-8 -*-
import cv2
import time
import os
import sys
import threading
import random
from CommonFile.PreSetter import PreSetter
from CommonFile.Client import Client
#from SnapShotProc import SnapShotProc
from CommonFile.Server import Server
from Vision.match_hand_card import get_hand_card
from Vision.match_public_card import get_public_card
from Vision.is_your_turn import is_your_turn

class MainTester:

    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 0
        self.xmlPath = sys.path[0] + '\\TestSet\\testxml\\test.xml'
        self.rawPath = sys.path[0] + '\\TestSet\\testRawSnapShot\\'
        self.resltPath = sys.path[0] + '\\TestSet\\testResultSnapShot\\'
        self.targetSize = (128, 128)

    def inputData(self):
        print("Input the xml config file path(-1 to use default):")
        tempPath = input()
        if tempPath != -1:
            self.xmlPath = tempPath
        print ("Input the raw snapShot file path(-1 to use default):")
        tempPath = input()
        if tempPath != -1:
            self.rawPath = tempPath
        print( "Input the result snapShot file path(-1 to use default):")
        tempPath = input()
        if tempPath != -1:
            self.resltPath = tempPath
        print ('Input the ip address(-1 to use default:)')
        tempIp = input()
        if tempIp != -1:
            self.ip = tempIp
        print ('Input the ip address(-1 to use default:)')
        tempPort = input()
        if tempPort != -1:
            self.port = tempPort

    def cleaningUp(self):
        print ("start cleaning")
        self.tcpS.onSendExitFlag()
        self.tcpS.close()
        #self.sps.setTerminateFlag()
        #self.td1.join()
        self.td2.join()

    def main(self):

      #  self.inputData()
        os.system('chcp 437')
        presetter = PreSetter(self.xmlPath)
        bqueue = presetter.runXmlInit()

        self.tcpS = Server(self.ip, 0)
        self.tcpS.bind()
        self.tcpS.Listening()


        # start monkeyrunner api part using Jython

        cmd = 'monkeyrunner ' + sys.path[0] + '\\monkeycontrol.py %s %d %s %s' % (
            self.ip, self.tcpS.getPort(), self.xmlPath, self.rawPath)

        #self.sps = SnapShotProc(self.rawPath, self.resltPath,self.targetSize, True)

        #self.td1 = threading.Thread(target=self.sps.runProc, args=())
        self.td2 = threading.Thread(target=os.system, args=(cmd,))

        self.td2.start()
        self.tcpS.acceptConnection()

        #self.td1.start()
        # here to add algorithm thread
        while True:  # random decision
            time.sleep(2)  # send a decision every second
            instruct = random.randint(1, 7)
            self.tcpS.onSending(instruct)
            if self.tcpS.onReceive()=='finished':
                if instruct == 1:
                    img_rgb = cv2.imread(self.rawPath+'\\demo.png')
                    hand_card = get_hand_card(img_rgb)
                    public_card = get_public_card(img_rgb)
                    print (hand_card)
                    print (public_card)

        # Exit Cleaning
        return -1


if __name__ == '__main__':
    mT = MainTester()
    s = mT.main()
    if s == -1:
        print ("Program exit")
