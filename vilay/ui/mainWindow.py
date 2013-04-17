import os, glob

from PyQt4 import QtCore, QtGui
from datetime import datetime

from vilay.ui.main_ui import Ui_vilaydetect
from vilay.core.Descriptor import MediaTime
from vilay.detectors import IDetector
from vilay.detectors.DetectorMainWrapper import DetectorMainWrapper 


class MainWindow(QtGui.QWidget):
    def __init__(self, vd, parent=None):
        # setting up GUI
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_vilaydetect()
        self.ui.setupUi(self)
        
        # main annotation data structure
        self.vd = vd
        # referencing actual shown frame
        self.actFrameIdx = 0
        
        # scheduler
        self.qscheduler = QtCore.QTimer()
        QtCore.QObject.connect(self.qscheduler, QtCore.SIGNAL("timeout()"), self.nextFrame)
        
        # main buttons
        self.ui.menuNew.clicked.connect(self.menuNew)
        self.ui.menuLoad.clicked.connect(self.menuLoad)
        self.ui.menuSave.clicked.connect(self.menuSave)
        self.ui.menuImport.clicked.connect(self.menuImport)
        self.ui.menuExport.clicked.connect(self.menuExport)
        self.ui.menuUndo.clicked.connect(self.menuUndo)
        self.ui.menuRedo.clicked.connect(self.menuRedo)
        self.connect(self.ui.menuDecSelect, QtCore.SIGNAL('activated(QString)'), self.changeMenuDetectorSelect)
        self.ui.menuDecStart.clicked.connect(self.startDetector)
        self.ui.menuSettings.clicked.connect(self.menuSettings)
        self.ui.menuQuit.clicked.connect(self.menuQuit)
        
        # film control buttons
        self.ui.filmPlayButton.clicked.connect(self.play)
        self.ui.filmPauseButton.clicked.connect(self.pause)
        self.ui.filmStopButton.clicked.connect(self.stop)
        self.ui.filmPrevFrameButton.clicked.connect(self.prevFrame)
        self.ui.filmNextFrameButton.clicked.connect(self.nextFrame)
        self.ui.filmPrevElementButton.clicked.connect(self.prevTimeElement)
        self.ui.filmNextElementButton.clicked.connect(self.nextTimeElement)
        self.ui.filmPrevTimeButton.clicked.connect(self.prevTime)
        self.ui.filmNextTimeButton.clicked.connect(self.nextTime)
        
        # zooming
        self.ui.filmZoom1x.clicked.connect(self.zoom1x)
        self.ui.filmZoom2x.clicked.connect(self.zoom2x)
        self.ui.filmZoom4x.clicked.connect(self.zoom4x)
        
        # splitter movements
        self.ui.splitter.splitterMoved.connect(self.repaint)
        self.ui.splitter_2.splitterMoved.connect(self.repaint)
        
        # film click events
        self.connect(self.ui.filmView, QtCore.SIGNAL('filmViewClicked(int,int)'), self.filmViewClicked)
        
        # setting root to concept tree for object getting
        self.ui.annotationTree.vd = self.vd
       
        # frame selected from navigation bar
        self.connect(self.ui.navigationBar, QtCore.SIGNAL('frameChanged(int)'), self.vd.showFrame)
        
        # when selection in tree changed, repaint small overview of MediaTimes in navigation bar
        self.connect(self.ui.annotationTree, QtCore.SIGNAL('dSelectionChanged()'), self.repaintNavigationMediaTimes)
        
        # detector list
        self.refreshDetectorList()
        
#         self.repaint()
#         self.replot()

    """ MAIN MENU BUTTON FUNCTIONS """
    def menuNew(self):
        if not self.vd.data is None:
            ret = QtGui.QMessageBox.question(self, 'New file', 'This will create a new file. All unsaved changes will be lost.', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
            if ret != QtGui.QMessageBox.Ok:
                return
            
        path = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        path = str(path)
        
        if not path == '':
            self.vd.newFile(path)

    
    def menuLoad(self):
        # TODO: implement
        pass
    
    def menuSave(self):
        # TODO: implement
        pass
    
    def menuImport(self):
        # TODO: implement
        pass
    
    def menuExport(self):
        # TODO: implement
        pass
    
    def menuUndo(self):
        # TODO: implement
        pass
    
    def menuRedo(self):
        # TODO: implement
        pass    

    def menuSettings(self):
        # TODO: implement
        pass
    
    def menuQuit(self):
        self.vd.close()
        pass
    
    """ FILM CONTROL VIEW BUTTON FUNCTIONS """ 
    def play(self):
        self.qscheduler.start(1000./self.vd.data.film.fps)
    
    def pause(self):
        self.qscheduler.stop()
    
    def stop(self):
        self.qscheduler.stop()
        self.vd.showFrame(0)
    
    def prevFrame(self):
        self.vd.showFrame(self.actFrameIdx-1)

    def nextFrame(self):
        self.vd.showFrame(self.actFrameIdx+1)
    
    def prevTimeElement(self):
        # TODO: implement
        print "Warning: mainWindow.py->prevTimeElement() not implemented correctly"
#         self.vd.showFrame(self.actFrameIdx-20)

    def nextTimeElement(self):
        # TODO: implement
        print "Warning: mainWindow.py->nextTimeElement() not implemented correctly"
#         self.vd.showFrame(self.actFrameIdx+20)
    
    def prevTime(self):
        fr = int(self.ui.filmTimeSpinBox.value()*self.vd.data.film.fps)
        self.vd.showFrame(self.actFrameIdx-fr)

    def nextTime(self):
        fr = int(self.ui.filmTimeSpinBox.value()*self.vd.data.film.fps)
        self.vd.showFrame(self.actFrameIdx+fr)
    
    def zoom1x(self):
        self.ui.filmView.setZoom(1)
    
    def zoom2x(self):
        self.ui.filmView.setZoom(2)
    
    def zoom4x(self):
        self.ui.filmView.setZoom(4)
    
    """ OTHER """
    def repaintNavigationMediaTimes(self):
        mediaTimes = list()
        for dItem in self.ui.annotationTree.getDSelection():
            mediaTimes.extend(dItem.collectAll(MediaTime))
        self.ui.navigationBar.repaint(mediaTimes)
    
    def repaint(self, evt=None):
        self.ui.filmView.readjust()
        self.ui.navigationBar.repaint()
    
    def replot(self):
        self.ui.annotationTree.createObjectTree()
    
    def resizeEvent(self, QResizeEvent):
        self.repaint()
    
    def refreshDetectorList(self):
        # import detector classes     
        for l in glob.glob(self.vd.rootPath + "/detectors/*.py"):
            moduleName = os.path.basename(l)[0:-3]
            if moduleName == '__init__' or moduleName == 'IDetector':
                continue
            __import__('vilay.detectors.'+moduleName)
        
        # search through detector classes
        self.vd.actDetector = None   
        self.detectors = []
        self.ui.menuDecSelect.addItem("None")
        for oneClass in IDetector.IDetector.__subclasses__():
            actDetectorInstance = oneClass()
            self.detectors.append(actDetectorInstance)
            self.ui.menuDecSelect.addItem(actDetectorInstance.getName())
        
    def updateFilmString(self):
        outp = "Frame " + str(self.actFrameIdx+1) + "/" + str(self.vd.data.film.nFrames) + "<br>"
        outp += "Time " + self.sec2time(self.vd.data.film.frameTimes[self.actFrameIdx]) + "/" + self.sec2time(self.vd.data.film.frameTimes[-1])
        self.ui.filmTimeFrame.setText(outp)
    
    def changeMenuDetectorSelect(self):
        decIdx = self.ui.menuDecSelect.currentIndex() -1
        if decIdx < 0:
            self.vd.actDetector = None
        else:
            self.vd.actDetector = DetectorMainWrapper(self.vd, self.detectors[decIdx].__class__())
    
    def startDetector(self):
        if not self.vd.actDetector is None:
            self.vd.actDetector.startDetector()
        else:
            print "Warning: no Detector selected"
    
    def filmViewClicked(self, x, y):
        #self.vd.selectItemAt(self.actFrameIdx, x, y)
        # TODO: fix
        print 'output: ' + str(x) + ', ' + str(y)
    
    def showImg(self, pic):
        self.actFrameIdx = self.vd.data.film.actFrame
        self.ui.filmView.showImg(pic)
    
    def closeEvent(self, event):
        self.vd.close()

    def sec2time(self, secs):
        secs = secs*1./1000
        int_t = int(secs)
        ms = secs - int_t
        tstr = datetime.fromtimestamp(-3600 + int_t).strftime('%H:%M:%S')
        return tstr + '.%.3i' % (ms * 1000)
        
    def time2seconds(self,h,m,s,ms):
        return h*3600+m*60+s+ms*1./1000
    
    
    