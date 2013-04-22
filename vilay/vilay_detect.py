import os
import sys

from PyQt4 import QtCore, QtGui

from vilay.ui.MainWindow import MainWindow
from vilay.core.VDData import VDData
from vilay.core.Film import Film
#from core import detection, detect_object, detect_time, position
from vilay.detectors.DetectorWrapper import DetectorWrapper 

import cv2

class VilayDetect:
    def __init__(self, eventloop=True):
        self.rootPath = os.path.dirname(os.path.abspath(__file__))
        
        # load data
        self.data = None #VDData()
        
        # create window
        self.app = QtGui.QApplication(sys.argv)
        self.mainWin = MainWindow(self)
        self.mainWin.show()
        
        # init detector
        self.detector = None
        
        if eventloop:
            self.wait()
    
    def wait(self):
        sys.exit(self.app.exec_())
    
    def newFile(self, filmpath = None):
        try:
            tmp = VDData(filmpath)
        except:
            raise("filmpath not valid")
        self.data = tmp
        
        self.mainWin.ui.navigationBar.setNFrames(self.data.film.nFrames)
        self.showFrame(0)
        self.mainWin.replot()
        self.mainWin.repaint()
        self.mainWin.repaintNavigationMediaTimes()
        
    def showFrame(self, frameIdx):
        pic = self.data.film.getFrame(frameIdx)
        
        dSlist = [self.data.dsRoot]
        for descrSchemes in dSlist: 
            if descrSchemes.containsFrameId(frameIdx):
                dSlist.extend(descrSchemes.descriptionSchemes)
                for descriptor in descrSchemes.descriptors:
                    overlayPic = descriptor.getOverlayImage(self.data.film.width,self.data.film.height)
                    if not overlayPic is None:
                        try:
                            pic = cv2.add(pic, overlayPic) 
                        except:
                            pass #TODO: replace by better
        
        self.mainWin.showImg(pic)
        self.mainWin.ui.navigationBar.setCursor(frameIdx)
        self.mainWin.updateFilmString()
    
    def initDetector(self, detector):
        self.detector = detector
        if not self.detector is None:
            self.detector = DetectorWrapper(self, detector)
    
    def startDetector(self):
        if not self.detector is None:
            self.detector.startDetector()
        else:
            print "Warning: no Detector selected"
    
    def selectItemAt(self, frameIdx, xPos = None, yPos = None):
        pass
        print ["select Item from Frame", str(frameIdx), "at [", str(xPos), ", ", str(yPos),"] "]
    
    def close(self):
        #self.qscheduler.stop()
        self.mainWin.deleteLater()
        self.app.quit()
