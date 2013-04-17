
class IDetector(object):
    def getName(self):
        return "default"
    
    def initialize(self):
        pass
    
    def detect(self, mediaTimes, tgtDS, film, rootDS, mainGUI):
        raise("detect function must me implemented by a Detector")
    
    def close(self):
        pass