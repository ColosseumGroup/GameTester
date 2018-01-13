# -*- coding: utf-8 -*-
class Behavior:
    # action==-1为停止flag
    def __init__(self, a="", P1=(0, 0), P2=(0, 0)):
        self.setAction(a)
        self.setActionTag(-1)
        self.setPosition(P1, P2)
        self.description =''

    def setDescription(self, descri):
        self.description = descri
        print ('Action %s with description %s Setted!' % (self.action,self.description))

    def setPosition(self, P1, P2=(0, 0)):
        self.Position1 = P1
        self.Position2 = P2

    def setAction(self, a):
        self.action = a

    def setActionTag(self, tag):
        self.behaviorTag = tag
        print ("Action " + self.action + " behaviorTag %d" % self.behaviorTag + " setted!")

    def getCordinateOne(self):
        return self.Position1

    def getCordinateTwo(self):
        return self.Position2

def main():
    b = Behavior()
    b.setAction("touch")
    b.setPosition((1, 2), (2, 3))
    b.setActionTag(-1)

if __name__ == '__main__':
    main()
