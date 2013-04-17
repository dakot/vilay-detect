from PyQt4 import QtCore, QtGui

from vilay.core.Descriptor import MediaTime

import numpy as np
import cv2

class NavigationBar(QtGui.QGraphicsView):

    def __init__(self, parent = None):
        super(NavigationBar, self).__init__ (parent)
        #QtGui.QGraphicsView.__init__(self,*args)
        
        # input data
        self.nFrames = None
        self.mediaTimes = []
        
        # positions of control elements in frames
        self.selectedItem = None
        self.leftTimeWindow = 0
        self.rightTimeWindow = None
        self.cursor = 0
        
        # temp for images
        self.bgImage = None
        self.intervalImage = None
        self.image = None
    
    def getPlaceTime(self):
        return MediaTime('UI', self.leftTimeWindow, self.rightTimeWindow-self.leftTimeWindow+1)
    
  
    def mousePressEvent (self, event):
        frameIdx = self.getFrameX(event.x())
        
        self.selectedItem = self.getItem(frameIdx)
        
        button = event.button()
        if button == 1: # left
            if self.selectedItem is None:
                self.setCursor(frameIdx)
                self.emit(QtCore.SIGNAL('frameChanged(int)'), self.cursor)
            elif self.selectedItem == "left":
                pass
            elif self.selectedItem == "right":
                pass
        if button == 2: # right
            pass
    
    def mouseMoveEvent(self, event):
        if self.selectedItem is None:
            return
        
        frameIdx = self.getFrameX(event.x())
        
        if self.selectedItem == "left":
            self.setInterval(frameIdx, None)
        elif self.selectedItem == "right":
            self.setInterval(None, frameIdx)
    
    def mouseReleaseEvent(self, event): 
        frameIdx = self.getFrameX(event.x())
        
        button = event.button()
        if button == 1:
            if self.selectedItem == "left":
                self.setInterval(frameIdx, None)
            elif self.selectedItem == "right":
                self.setInterval(None, frameIdx)
            self.selectedItem = None
        if button == 2:
            pass
     
    def getItem(self, frameIdx):
        maxDist = 10
        normLeft = abs(frameIdx - self.leftTimeWindow)
        normRight = abs(frameIdx - self.rightTimeWindow)
        
        if normLeft < maxDist and normLeft < normRight:
            return "left"
        if normRight < maxDist and normRight < normLeft:
            return "right"
        return None
    
    def setCursor(self, frameIdx = None):
        if not frameIdx is None:
            self.cursor = frameIdx
        
        if self.nFrames is None:
            print "nFrames not initialized yet"
            return
        
        if self.intervalImage is None:
            self.repaint()
        
        # draw cursor
        self.image = self.intervalImage.copy();
        xCursor = self.getPaintX(self.cursor)
        # TODO: draw view area
        
        self.image[0:1, xCursor-3:xCursor+4] = [166,26,26]
        self.image[1:2, xCursor-2:xCursor+3] = [166,26,26]
        self.image[2:-3, xCursor-1:xCursor+2] = [166,26,26]
        self.image[-3:-2, xCursor-2:xCursor+3] = [166,26,26]
        self.image[-2:-1, xCursor-3:xCursor+4] = [166,26,26]
        
        self.image[0:-1, xCursor:xCursor+1,:] = 0
        
        self.showImage()
    
    def setInterval(self, leftInt = None, rightInt = None):
        if not leftInt is None:
            self.leftTimeWindow = leftInt
        if not rightInt is None:
            self.rightTimeWindow = rightInt
        
        # draw interval
        self.intervalImage = self.bgImage.copy();
        xLeft = self.getPaintX(self.leftTimeWindow);
        self.intervalImage[0:-1, xLeft:xLeft+2, :] = 0
        self.intervalImage[4:9, xLeft+2, :] = 0
        self.intervalImage[5:8, xLeft+3, :] = 0
        self.intervalImage[6, xLeft+4, :] = 0
        
        xRight = self.getPaintX(self.rightTimeWindow);
        self.intervalImage[0:-1, xRight-2:xRight, :] = 0
        self.intervalImage[4:9, xRight-3, :] = 0
        self.intervalImage[5:8, xRight-4, :] = 0
        self.intervalImage[6, xRight-5, :] = 0
        
        self.setCursor()
    
    def setNFrames(self, nFrames):
        self.nFrames = nFrames
        if self.rightTimeWindow is None:
            self.rightTimeWindow = nFrames-1
    
    def repaint(self, mediaTimes=[]):
        if self.nFrames is None:
            print "nFrames not initialized yet"
            return
        
        if not mediaTimes == []:
            self.mediaTimes = mediaTimes
        
        self.bgImage = np.zeros([self.height(),self.width(),3],'uint8') + 255;
        # draw cuts
        for mediaTime in self.mediaTimes:
            self.bgImage[0:-1, self.getPaintX(mediaTime.startTime):self.getPaintX(mediaTime.startTime+mediaTime.duration), :] = 180
        
        self.setInterval()
        
        self.setCursor()

    def showImage(self):
        h, w, channels = self.image.shape
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)

        # Qt expects 32bit BGRA data for color images:    
        qimg = QtGui.QImage(self.image.data, w, h, QtGui.QImage.Format_RGB32)
        qimg.ndarray = self.image
        
        scene = QtGui.QGraphicsScene()
        scene.addPixmap(QtGui.QPixmap(qimg))
        
        self.setScene(scene)
    
    def getPaintX(self, frame):
        return int(frame*1./self.nFrames * self.width())
    
    def getFrameX(self, x):
        if x < 0:
            return 0
        elif x >= self.width():
            return self.nFrames-1
        else:
            return int(x*1./self.width() * self.nFrames)
        
    