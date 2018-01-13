# -*- coding: utf-8 -*-
import time
import sys
import threading

#**********************************************************
sys.path.append('C:\\Users\\bowei\\Desktop\\PokerGame\\')
#**************************************must edit here first
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from CommonFile.Client import Client
from CommonFile.Behavior import Behavior
from CommonFile.PreSetter import PreSetter 
# monkeyrunner is for monkeyrunner (Jython)

class MonkeyController:
    def __init__(self, ip, port, behaviorQ, rawpath):
        self.device = MonkeyRunner.waitForConnection()
        self.device.wake()
        self.tClient = Client(ip, int(port))
        self.behaviorQueue = behaviorQ
        self.RawPath = rawpath
        self.tClient.connect()
        self.imageNum = 0
        self.controlTag = False

    def touch(self, beh):
        P = beh.getCordinateOne()
        self.device.touch(P[0],P[1], "DOWN_AND_UP")

    def drag(self, beh):
        self.device.drag(beh.getCordinateOne(),
                         beh.getCordinateTwo(), 0.1)

    def snapShot(self, beh):
        im = self.device.takeSnapshot()
        #filename = "demo%d.png" % self.imageNum
        filename = "demo.png"
        #self.imageNum = self.imageNum + 1
        im.writeToFile(self.RawPath + filename)
        print ('write to file %s' % filename)

    def actionWarpper(self,action,behavior):
        print ('Perform: %s' % behavior.description)
        action(behavior)
        self.tClient.onSend('finished')#return finish flag

    def execute(self, beh):
        # define more action here later
        switcher = {
            'touch': self.touch,
            'drag': self.drag,
            'snapshot': self.snapShot
        }
        func = switcher.get(beh.action, "behavior unexcepted!")
        return self.actionWarpper(func,beh)

    def handleInstrct(self, instruct):
        if instruct == -1:  # Read exitFlag from tcp
            self.controlTag = True
        else:
            if instruct>len(self.behaviorQueue):
                return
            else:
                self.execute(self.behaviorQueue[instruct])  # slightly faster

    def runner(self):  # receive instruc
        while True:
            instruct = self.tClient.onReceive()
            print ('\nreceive instruct %d'% instruct)
            self.handleInstrct(instruct)
            
            if self.controlTag == True:
                return

def main():
    # receive argv from cmdline
    ip = sys.argv[1]
    port = sys.argv[2]
    xmlPath = sys.argv[3]
    rawPath = sys.argv[4]  # maybe no need later
    Psetter = PreSetter(xmlPath)
    bq = Psetter.runXmlInit()

    # start the controller and snapshot thread
    MkCtrl = MonkeyController(ip, port, bq, rawPath)
    td1 = threading.Thread(target=MkCtrl.runner, args=())

    td1.start()

    # Exit cleaning
    while True:#here is to change
        time.sleep(10)
        if MkCtrl.controlTag == True:
            td1.join()
            MkCtrl.tClient.close()
            break


if __name__ == '__main__':
    main()
