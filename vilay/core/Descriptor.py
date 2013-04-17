"""
abstract class
"""
from PyQt4 import QtGui, QtCore

class Descriptor(object):
    def __init__(self, origin, *data):
        self.parent = None
        self.origin = origin
        self.init()
        if len(data) > 0:
            self.setData(*data)
    
    def init(self):
        pass
    
    def move(self, dest):
        if self.parent is None:
            return False
        elif self.parent == dest:
            return True
        else:
            parent = self.parent
            dest.addDescriptor(self)
            parent.descriptors.remove(self)
            return True
    
    def delete(self):
        if not (self.parent is None):
            self.parent.descriptors.remove(self)
        del self
    
    def setData(self, *data):
        raise("implementation missing")
    
    def getTypeString(self):
        raise("implementation missing")
    
    def getValueString(self):
        raise("implementation missing")
    
    def getOverlayImage(self, width, height):
        return None
    
#    def getExportString(self):
#        raise("implementation missing")

    def collectAll(self, classObj):
        if isinstance(self, classObj):
            return [self]
        else:
            return []
    
class MediaTime(Descriptor):   
    def setData(self, startTime = None, duration=None):
        if type(int(startTime)) == int: 
            self.startTime = startTime
            
            if type(int(duration)) == int:
                self.duration = duration
            else:
                self.duration = 1
        else:
            self.startTime = None
            self.duration = None
        
        
    def contains(self, obj):
        if isinstance(obj, MediaTime):
            return obj.startTime >= self.startTime and obj.startTime + obj.duration <= self.startTime + self.duration
    
    def getTypeString(self):
        return "MediaTime"
    
    def getValueString(self):
        if self.duration > 1:
            return "F=" + str(self.startTime+1) + ", L=" + str(self.duration)
        else:
            return "F=" + str(self.startTime+1)
    
    def initViaGui(self, filmView=None):
        self.__init__('User')
        text, qInpReturn = QtGui.QInputDialog.getText(None, 'Input', 'Fill in StartTime, Duration', text='0,1')
        if qInpReturn:
            vec = list(text.split(","))
            self.setData(int(vec[0]), int(vec[1]))
        

import numpy as np
import cv2

class Shape(Descriptor):
    def init(self):
        self.dictionary = dict(none=0, rect=1 ,circ=2 ,poly=3 ,elip=4)
    
    def setData(self, typ='none', pts=[]):
        self.typ = self.dictionary.get(typ)
        if not self.dictionary.values().count(self.typ) > 0:
            self.typ = self.dictionary.get('none')
        
        self.points = pts
        self.poly = self.getPoly(self.typ, self.points)
    
    def getPoly(self, typ, pts):
        if typ == 0:
            return []
        elif typ == 1:
            x = pts[:,0]
            y = pts[:,1]
            
            x.sort()
            y.sort()
            return np.array([[x[0],y[0]],[x[0],y[1]],[x[1],y[1]],[x[1],y[0]]])
        elif typ == 2:
            r = int(np.linalg.norm(pts[0,:] - pts[1,:]))
            return cv2.ellipse2Poly((pts[0,0],pts[0,1]), (r,r), 0, 0, 360, 10)
        elif typ == 3:
            return pts[0:-2,:]
        elif typ == 4:
            print "Warning: Place->getPoly(): typ=4 (ellipse) not implemented yet"
            return None
    
    def getTypeString(self):
        return "Shape"
    
    def getValueString(self):
        return 'type ' + str(self.typ)
    
    def getOverlayImage(self, width, height, color=[0,255,0]):
        pic = np.zeros([height,width,3],'uint8')
        cv2.polylines(pic, [self.poly], True, color)
                
        return pic
    
    def initViaGui(self, filmView=None):
        self.__init__('User')
        self.pts = []
        self.filmView = filmView
        items = self.dictionary.keys()
        item, ok = QtGui.QInputDialog.getItem (None, "Select drawType", "Select drawType, then draw in filmView", items, current = 0, editable = False)
        if ok:
            QtCore.QObject.connect(filmView, QtCore.SIGNAL('filmViewClicked(int,int)'), self.addPoint)
            while not len(self.pts) == 2:
                cv2.waitKey(200)
            QtCore.QObject.disconnect(self.filmView, QtCore.SIGNAL('filmViewClicked(int,int)'), self.addPoint)
            print np.array(self.pts)
            self.setData(str(item), np.array(self.pts))
        else:
            del(self)

    def addPoint(self, x, y):
        self.pts.append([x,y])
        