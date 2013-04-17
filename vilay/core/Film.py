from vilay.core.Cache import Cache

import cv2
import numpy as np

class Film:
    def __init__(self, path):
        self.path = path
        self.capture = cv2.VideoCapture(self.path)
        
        self.width   = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
        self.height  = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        
        # not using open cv functions due to wrong values
        #self.fps = self.capture.get(cv2.cv.CV_CAP_PROP_FPS )
        #self.nFrames = int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT ))
        #self.nSeconds = self.nFrames / self.fps
        
        self.frameTimes = self.getFrameIndizes()
        self.nFrames = self.frameTimes.size
        self.fps = self.nFrames *1000./ (int(self.frameTimes[-1]-self.frameTimes[0]))
        self.nSeconds = self.frameTimes[-1]*1./1000
        
        self.fourcc = int(self.capture.get(cv2.cv.CV_CAP_PROP_FOURCC ))
        
        self.cacheSize = 100
        self.cache = Cache(self.cacheSize)
        
        self.actFrame = 0
    
    def getFrameIndizes(self):
        frameTimes = []
        while self.capture.grab():
            msec = int(self.capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
            frameTimes.append(msec)
        frameTimes = np.array(frameTimes)
        return frameTimes
    
    def getFrame(self, frameIdx):
        frameIdx = int(frameIdx)
        if frameIdx < 0:
            frameIdx = 0
        if frameIdx >= self.nFrames:
            frameIdx = self.nFrames-1
        
        
        # frame is already cached, so read from cache
        i = self.cache.getCacheIdx(frameIdx)
        if i != None:
            #print ["got from cache", i]
            pass
        
        # frame is next frame in capture pipeline
        elif frameIdx == self.frameTimes.searchsorted(int(self.capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC))) + 1:
            i = self.cache.add(frameIdx, self.capture.read()[1])
            #print ["frame was next in pipeline", i]
        
        # frame must be searched
        else:
            msecInp = self.frameTimes[frameIdx]
            msecOut = msecInp +1
            msecReq = msecInp
            #print ["frame newly requested", i]
            
            while msecInp < msecOut:
                msecReq -= 1000
                if msecReq < 0:
                    self.capture = cv2.VideoCapture(self.path)
                else:
                    self.capture.set(cv2.cv.CV_CAP_PROP_POS_MSEC, msecReq)
                pic = self.capture.read()[1]
                msecOut = int(self.capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
            
            if msecInp != msecOut:
                captureFrameIdx = self.frameTimes.searchsorted(int(self.capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)))
                while captureFrameIdx < frameIdx:
                    pic = self.capture.read()[1]
                    captureFrameIdx = self.frameTimes.searchsorted(int(self.capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)))
                    i = self.cache.add(captureFrameIdx, pic)
                    
                i = self.cache.add(frameIdx,pic)
            else:
                i = self.cache.add(frameIdx,pic)
        
        self.actFrame = frameIdx
        return self.cache.getFromCacheIdx(i)
        