
# from PyQt4 import QtCore, QtGui

from vilay.vilay_detect import VilayDetect

#from core import detection, detect_object, detect_time, position
# from vilay.core.DescriptionScheme import DescriptionScheme

if __name__ == "__main__":
    vd = VilayDetect(False)
    
#     indy = DescriptionScheme("Indy")
#     vd.data.dsRoot.addDescriptionScheme(indy)
#     indy.addDescriptionScheme(DescriptionScheme("Gesicht"))
#     indy.addDescriptionScheme(DescriptionScheme("Hand"))
#     vd.data.dsRoot.addDescriptionScheme(DescriptionScheme("Nazi"))
#     vd.data.dsRoot.addDescriptionScheme(DescriptionScheme("Marion"))
#     vd.mainWin.replot()
#      
#     vd.loadFilm('/home/danielkottke/indi_short.m4v')
    
    vd.wait()
    