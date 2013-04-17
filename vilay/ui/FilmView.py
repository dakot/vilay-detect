from PyQt4 import QtGui, QtCore

import numpy as np
import cv2

class FilmView(QtGui.QGraphicsView):

    def __init__(self, *args):
        QtGui.QGraphicsView.__init__(self,*args)
#         self.sendClickPosition = None   #set by mainWindow in init
#         self.sendPoints = None    #set by mainWindow in init
#         self.drawType = None    #set by mainWindow
        self.zoom = 1;
        
        self.pic = None
    
    def mouseReleaseEvent(self, event):
        scenePoint = self.mapToScene(QtCore.QPoint(event.x(),event.y()))
        x = int(scenePoint.x())
        y = int(scenePoint.y())
        self.emit(QtCore.SIGNAL('filmViewClicked(int,int)'), x, y)
        
#     def mouseReleaseEvent(self, event):
#         if self.drawType is None:
#             self.sendClickPosition(event.x(),event.y())
#         elif self.drawType == 1 or self.drawType == 2: #rect. circ
#             self.drawSmallTmpPoint(event.x(),event.y())
#             self.points.append(np.array([event.x(), event.y()]))
#             if len(self.points) == 2:
#                 self.sendPoints(np.array(self.points).copy())
#                 self.points = []
#         elif self.drawType == 3: #poly
#             self.drawSmallTmpPoint(event.x(),event.y())
#             self.points.append(np.array([event.x(), event.y()]))
#             if len(self.points) > 2:
#                 if np.linalg.norm(self.points[0] - self.points[len(self.points)-1]) <= 5:
#                     self.sendPoints(np.array(self.points).copy())
#                     self.points = []
#         elif self.drawType == 4: #elip
#             self.drawSmallTmpPoint(event.x(),event.y())
#             self.points.append(np.array([event.x(), event.y()]))
#             if len(self.points) == 4:
#                 self.sendPoints(np.array(self.points).copy())
#                 self.points = []
#     
#     def drawSmallTmpPoint(self,x,y):
#         pic = cv2.cvtColor(self.pic, cv2.COLOR_BGRA2BGR)
#         cv2.circle(pic, (x,y), 1, [100,100,255], 2)
#         self.showImg(pic)
        
    def mouseMoveEvent(self, event):
        pass
        
    def setZoom(self, zoom):
        self.zoom = zoom
        self.readjust()
    
    def readjust(self):
        if not self.pic is None:
            scaleCoeff = min(float(self.width())/(self.pic.shape[1]+4), float(self.height())/(self.pic.shape[0]+4))
            self.resetTransform()
            self.scale(self.zoom*scaleCoeff, self.zoom*scaleCoeff)
    
    def showImg(self, pic):
        self.pic = pic
        
        h, w, channels = self.pic.shape
        self.pic = cv2.cvtColor(self.pic, cv2.COLOR_BGR2BGRA)

        # Qt expects 32bit BGRA data for color images:    
        qimg = QtGui.QImage(self.pic.data, w, h, QtGui.QImage.Format_RGB32)
        qimg.ndarray = self.pic
        
        scene = QtGui.QGraphicsScene()
        scene.addPixmap(QtGui.QPixmap(qimg))
        
        self.setScene(scene)
    