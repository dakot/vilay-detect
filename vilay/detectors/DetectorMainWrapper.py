from PyQt4 import QtGui

from vilay.core.DescriptionScheme import DescriptionScheme

class DetectorMainWrapper:
    
    def __init__(self, vd, detectorClass):
        self.vd = vd
        self.detector = detectorClass
        self.tgtRoot = self.vd.data.dsRoot
        self.mediaTimes = []
        
        self.detector.initialize()
    
    def startDetector(self):
        self.tgtRoot = self.vd.data.dsRoot
        self.mediaTimes = [self.vd.mainWin.ui.navigationBar.getPlaceTime()]
        items = ["Add new Description Scheme to root"]
#         items.extend( self.vd.data.dsRoot.getAllPaths())
#         item, ok = QtGui.QInputDialog.getItem (self.vd.mainWin, "Select root Description Scheme", "Select root for newly detected objects.", items, current = 0, editable = False)
        ok = QtGui.QInputDialog.getItem (self.vd.mainWin, "Select root Description Scheme", "Select root for newly detected objects.", items, current = 0, editable = False)
        
        # TODO: merge mediaTime 
        
        if ok:
            newSemObj = DescriptionScheme("New "+self.detector.getName()+" DS")
            self.vd.data.dsRoot.addDescriptionScheme(newSemObj)
            self.tgtRoot = newSemObj
            #TODO: fix selection of DS
#             path = list(item.split(" > "))
#             if len(path) == 1:
#                 if not item == self.vd.data.dsRoot.name:
#                     newSemObj = DescriptionScheme("New "+self.detector.getName()+" DS")
#                     self.vd.data.dsRoot.addDescriptionScheme(newSemObj)
#                     self.tgtRoot = newSemObj
#             else:
#                 path.pop(0)
#                 print path
#                 newRoot = self.treeRoot.getDescriptionSchemesRecursicely(path)
#                 self.tgtRoot = newRoot
            
            self.detector.detect(self.mediaTimes, self.tgtRoot, self.vd.data.film, self.vd.data.dsRoot, self.vd.mainWin)
            self.vd.mainWin.replot()
            self.vd.mainWin.repaint()
    