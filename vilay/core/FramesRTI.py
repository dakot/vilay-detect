class FramesRTI:
    """ The class framesRTI is a lookup table, that maps all 'RegionTimeInterval's to its corresponding frameIdx. Furthermore it stores the property 'curated' for every frame. Currated in this setting means, that a frame was seen by a user and its 'RegionTimeInterval's are labeled as correct. """
    
    def __init__(self, nFrames=0):
        self.nFrames = film.nFrames
        self.curated = [False]*self.nFrames
        self.rtis = [[]]*self.nFrames
    
    
    # ***** RegionTimeInterval functions *****
    
    def build(self, rootConcept):
        """ Generates the lookup table for all 'RegionTimeInterval's, that are defined in the 'rootConcept' or its children.
        Goes through every 'RegionTimeInterval' and adds it to 'self.rtis' """
        raise("FramesRTI->build: not implemented yet")
        # TODO: implement
    
    def addRti(self, rti):
        """ Adds a 'RegionTimeInterval' to this FramesRTI. 
        Therefore this rti is inserted for every frame from 'rti.startFrame' to 'rti.startFrame'+'rti.duration'-1 into 'self.rtis' """
        if hasattr(rti, 'getAllValidFrames'):
            for frameIdx in rti.getAllValidFrames():
                self.rtis[frameIdx].append(rti)
            return True
        else:
            return False
    
    def delRti(self, rti):
        """ Deletes a 'RegionTimeInterval' from this FramesRTI. 
        Therefore this rti is deleted for every frame from 'rti.startFrame' to 'rti.startFrame'+'rti.duration'-1 from 'self.rtis' """
        if hasattr(rti, 'getAllValidFrames'):
            res = True
            for frameIdx in rti.getAllValidFrames():
                try:
                    self.rtis[frameIdx].remove(rti)
                except ValueError:
                    res = False
            return res
        else:
            return False
    
    
    # ***** setter functions *****
    
    def setCurated(self, frameIdx, b = True):
        """ Sets the curated variable at 'frameIdx' to the value in 'b'. If no value is given, it is set to 'True'.
            If frameIdx does not exist, nothing is done."""
        if frameIdx >= 0 and frameIdx < self.nFrames and type(b) == bool:
            self.curated[frameIdx] = b
    
    
    # ***** getter functions *****
    
    def getCurated(self, frameIdx):
        """ Returns 'True', if frame at 'frameIdx' is curated by user. 
            Returns 'None', if 'frameIdx' does not exist."""
        if frameIdx >= 0 and frameIdx < self.nFrames:
            return self.curated[frameIdx]
        else:
            return None
    
    def getRtis(self, frameIdx):
        """ Returns a list of all 'RegionTimeInterval's that belong to frame 'frameIdx'.
            Returns an empty list, if 'frameIdx' does not exist."""
        if frameIdx >= 0 and frameIdx < self.nFrames:
            return self.curated[frameIdx]
        else:
            return []
    
