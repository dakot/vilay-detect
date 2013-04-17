class Cache:
    #TODO: replace by dict 
    def __init__(self, size):
        self.size = size
        self.writeIdx = 0
        
        self.indexes = [None] * self.size
        self.storage = [None] * self.size

    def add(self, idx, data):
        if self.getCacheIdx(idx) == None:
            self.indexes[self.writeIdx] = idx
            self.storage[self.writeIdx] = data
            
            wroteAtIdx = self.writeIdx
            self.writeIdx = (self.writeIdx + 1) % self.size
            return wroteAtIdx
        else:
            return self.getCacheIdx(idx)
    
    def get(self, idx):
        i = self.getCacheIdx(idx)
        return self.getFromCacheIdx(i)
    
    def getCacheIdx(self, requestIdx):
        for i,idx in enumerate(self.indexes):
            if idx == requestIdx:
                return i
        
        return None
    
    def getFromCacheIdx(self, idx):
        if idx >= 0 and idx < self.size:
            return self.storage[idx]
        else:
            return None 