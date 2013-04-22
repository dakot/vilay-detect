import cv2
import numpy as np
import os

from vilay.core.Descriptor import MediaTime, Shape
from vilay.detectors.IDetector import IDetector
from vilay.core.DescriptionScheme import DescriptionScheme

class FaceDetector(IDetector):
    
    def getName(self):
        return "Face Detector"
    
    def initialize(self):
        # define haar-detector file
        print os.getcwd() + '/vilay/detectors/FaceDetector/haarcascade_frontalface_default.xml'
        self.cascade = cv2.CascadeClassifier(os.getcwd() + '/vilay/detectors/FaceDetector/haarcascade_frontalface_default.xml')
    
    def detect(self, mediaTimes, tgtDS, film, rootDS, mainGUI):
        for mediaTime in mediaTimes:
            for frameIdx in range(mediaTime.startTime, mediaTime.startTime + mediaTime.duration):
                actFrame = film.getFrame(frameIdx)
                
                # preprocessing
                actFrame = cv2.cvtColor(actFrame, cv2.cv.CV_BGR2GRAY)
                actFrame = cv2.equalizeHist(actFrame)
                
                # detect faces
                faces = self.cascade.detectMultiScale(actFrame, 1.2, 3, 0, (5,5))
                
                # create ds and add time and shape descriptor 
                for faceIdx in range(len(faces)):
                    [x,y,width,height] = faces[faceIdx,:]
                    
                    ds = DescriptionScheme('RTI', 'Face Detector')
                    region = Shape('Face Detector','rect', np.array([[x, y], [x + width, y + height]]))
                    mediaTime = MediaTime('Face Detector', frameIdx, 1)
                    
                    tgtDS.addDescriptionScheme(ds)
                    ds.addDescriptor(region)
                    ds.addDescriptor(mediaTime)
            
        
    