# -*- coding: utf-8 -*-
import time
import sys
import threading

from CommonFile.Behavior import Behavior

class Actor:
    def __init__(self, behaviorQ, snapshot_path):
        self.behaviorQueue = behaviorQ
        self.snapshot_path = snapshot_path
        self.imageNum = 0
        self.controlTag = False

    def touch(self, beh):
        P = beh.getCordinateOne()
        os.system('adb shell input tap %d %d'%(P[0],P[1]))

    def drag(self, beh):
        pass

    def snapShot(self, beh):
        os.system('adb shell screencap -p /sdcard/ScreenTemp.png')
        os.system('adb shell pull /sdcard/ScreenTemp.png '+self.snapshot_path)
        print('Screen Shot update!')

    def actionWarpper(self,action,behavior):
        print ('Perform: %s' % behavior.description)
        action(behavior)

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

def main():
    # receive argv from cmdline
    ip = sys.argv[1]
    port = sys.argv[2]
    xmlPath = sys.argv[3]
    snapshot_path = sys.argv[4]  # maybe no need later
    Psetter = PreSetter(xmlPath)
    bq = Psetter.runXmlInit()

    # start the controller and snapshot thread
    MkCtrl = MonkeyController(ip, port, bq, snapshot_path)
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
