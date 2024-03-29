from vilay.detectors.IDetector import IDetector
from vilay.core.Descriptor import MediaTime
from vilay.core.DescriptionScheme import DescriptionScheme

import cv2
import numpy as np

class ShotDetector(IDetector):
    def getName(self):
        return "Shot Detector"
    
    def initialize(self):
        self.threshold = 45 
    
    def detect(self, mediaTimes, tgtDS, film, rootDS, mainGUI):
        for mediaTime in mediaTimes:
            frame1 = None
            frame2 = None
            
            values = []
            times = []
            cuts = []
            
            # go through every frame
            for frameIdx in range(mediaTime.startTime, mediaTime.startTime + mediaTime.duration):
                actFrame = film.getFrame(frameIdx)
                
                frame2 = self.preProcessing(actFrame)
                
                if not frame1 is None:
                    absPic = cv2.absdiff(frame2, frame1)
                    mean = sum(cv2.mean(absPic))
                    values.append(mean)
                    times.append(frameIdx)
                
                frame1 = frame2
            
            # numpy array conversion
            times = np.array(times)
            values = np.array(values)
            
            # calculate second derivation 
            fstDiff = np.gradient(values)
            sndDiff = np.gradient(fstDiff)
            
            cuts.append(mediaTime.startTime)
            
            for i, val in enumerate(sndDiff):
                if val < -1*self.threshold:
                    cuts.append(times[i])
            
            cuts.append(mediaTime.startTime+mediaTime.duration)
            
            cuts = np.array(cuts)
            
            # create DS and add descriptor
            for i in range(len(cuts)-1):
                actDS = DescriptionScheme('Shot '+str(i+1), 'Shot Detector')
                mediaTime = MediaTime('Shot Detector', cuts[i], cuts[i+1]-cuts[i])
                actDS.addDescriptor(mediaTime)
                tgtDS.addDescriptionScheme(actDS)
            
    
    def preProcessing(self, img):
        # make small image and equalize histogram
        img = cv2.resize(img,(10,10))
        img2 = np.zeros((img.shape[0],img.shape[1],1),'uint8')
        for i in range(3):
            img2[:,:,0] = img[:,:,i]
            img[:,:,i] = cv2.equalizeHist(img2)
        
        return img