# -*- coding: utf-8 -*-
import sys
print (sys.path)
sys.path.append(sys.path[0]+"//BehaviorUtils")
from Behavior import Behavior

from xml.dom.minidom import parse
import xml.dom.minidom
class PreSetter:
    def __init__(self, pathXml='', pathTP=''):
        self.xmlPath = pathXml
        self.TraningParmeterPath = pathTP
        print('PreSetter construct')

    def setBehaviorXmlPath(self, path):
        self.xmlPath = path

    def setTraningParmeters(self, path):
        self.TraningParmeterPath = path

    def runParmetersInit(self):
        pass

    def runXmlInit(self):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(self.xmlPath)
        collection = DOMTree.documentElement
        if collection.hasAttribute("BehaviorFor"):
            print ("This behavior set is for algorithm : %s" % collection.getAttribute("BehaviorFor"))

        behaviors = collection.getElementsByTagName("Behavior")
        BehaviorQueue = []
        i = 0
        for bh in behaviors:
            be = Behavior()
            print ("Behavior%d init" % i)
            if bh.hasAttribute("actionType"):
                be.setAction(bh.getAttribute("actionType"))
            bhtype = bh.getElementsByTagName('description')[0]
            descrip = bhtype.childNodes[0].data
            be.setDescription(descrip)
            bhtype = bh.getElementsByTagName('x1')[0]
            x1 = int(bhtype.childNodes[0].data)
            bhtype = bh.getElementsByTagName('y1')[0]
            y1 = int(bhtype.childNodes[0].data)
            if be.action == "drag":
                bhtype = bh.getElementsByTagName('x2')[0]
                x2 = int(bhtype.childNodes[0].data)
                bhtype = bh.getElementsByTagName('y2')[0]
                y2 = int(bhtype.childNodes[0].data)
                be.setPosition((x1, y1), (x2, y2))
            else:
                be.setPosition((x1, y1))
            be.setActionTag(i)
            i = i + 1
            BehaviorQueue.append(be)
        print ("BehaviorQueue Size:%d" % len(BehaviorQueue))
        return BehaviorQueue
