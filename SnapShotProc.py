# -*- coding: UTF-8 -*-
import time
import os
import sys
from PIL import Image
from PIL import ImageFile
#ImageFile.LOAD_TRUNCATED_IMAGES = True************************************************************************************remember

#process the image
class SnapShotProc:

    def __init__(self, Raw, Reslt, TarSize=(), saveTag=False):  # maybe modify tarx tary into tuple
        self.RawPath = Raw
        self.ResltPath = Reslt
        self.TargetSize = TarSize
        self.isSave = saveTag
        self.terminateFlag = False
        self.currentImName = ''
        self.currentPos = 0

    def ConvertSnapShot(self, im):
        gray = im.resize(self.TargetSize)
        gray = gray.convert("L")
        print ('%s convert finished' % self.currentImName)
        return gray

    def setTerminateFlag(self):
        self.terminateFlag = True
        print ('SnapShotProc terminate')

    def ConvertSnapShotAndSaveToResltPath(self, im):
        if self.ResltPath != "":
            self.ConvertSnapShot(im).save(
                self.ResltPath + self.currentImName, 'png')
        else:
            print ("Error! Please Set ResltPath")

    def getImageFromRaw(self):  # until get the Image Successfully
        if self.RawPath == "":
            print ("Error!Please Set RawPath")
            return
        while self.terminateFlag != True:
            self.currentImName = "demo%d.png" % self.currentPos
            filePath = self.RawPath + self.currentImName  # may need change
            if os.path.isfile(filePath):
                # though image was found, the image might still be processing by the monkeyrunner
                time.sleep(0.4)
                self.currentPos = self.currentPos + 1
                if self.currentPos == 1000:  # may need change
                    self.currentPos = 0
                try:
                    im = Image.open(filePath)
                    return im
                except IOError, e:
                    print ("Error:", e)
                    continue
                # os.remove(filePath)
        return

    def runProc(self):  # keep proccessing snapshots
        if self.TargetSize[0] == 0:
            print ("Error! Please Set TargetSize")
            return
        while self.terminateFlag != True:
            im = self.getImageFromRaw()
            if im == None:
                continue
            if self.isSave == True:
                self.ConvertSnapShotAndSaveToResltPath(im)
            else:
                self.ConvertSnapShot(im)
        return


def main():
    pt = sys.path[0] + "\\PythonProcTest\\testset\\"
    rpt = sys.path[0] + "\\PythonProcTest\\reslt\\"
    sps = SnapShotProc(pt, rpt, (64, 64), True)
    sps.runProc()


if __name__ == '__main__':
    main()
