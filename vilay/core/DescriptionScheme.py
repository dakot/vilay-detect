from vilay.core.Descriptor import MediaTime

class DescriptionScheme:
    def __init__(self, name, origin="unknown"):
        self.name = name
        self.parent = None
        self.origin = None
        self.descriptionSchemes = set()
        self.descriptors = set()
    
    # ### adding functions ###
    def addDescriptionScheme(self, descriptionScheme):
        descriptionScheme.parent = self
        self.descriptionSchemes.add(descriptionScheme)
    
    def addDescriptor(self, descriptor):
        descriptor.parent = self
        self.descriptors.add(descriptor)
    
    # ### object manipulation ###
    def rename(self, name):
        if len(name) > 0:
            self.name = name
            return True
        else:
            return False
    
    def move(self, dest):
        if self.parent is None:
            return False
        elif self.parent == dest:
            return True
        else:
            parent = self.parent
            dest.addDescriptionScheme(self)
            parent.descriptionSchemes.remove(self)
            return True
    
    def delete(self):
        if not (self.parent is None):
            self.parent.descriptionSchemes.remove(self)
        del self
    

    # ### getter functions ###
    def getDescriptionSchemes(self):
        return self.descriptionSchemes
    
    def getDescriptors(self):
        return self.descriptors
    
    def getAllPaths(self):
        dictionary = dict()
        strList = [str(self.name)]
        dictionary[str(self.name)] = self
        for child in self.getDescriptionSchemes():
            appendStrList = child.getAllPaths()
            for appendStr in appendStrList:
                strList.append(str(self.name) + " > " + str(appendStr))
#             strList.sort()
        return strList
    
#     def getDescriptionSchemesRecursicely(self, objPath):
#         semObj = self;
#         for objName in objPath:
#             if not semObj.getDescriptionScheme(objName) is None:
#                 semObj = semObj.getDescriptionScheme(objName)
#             else:
#                 semObj = semObj.getDescriptor(objName)
#                 break
#             
#         return semObj
    
    def collectAll(self, classObj):
        s = list()
        for descriptor in self.descriptors:
            s.extend(descriptor.collectAll(classObj))
        for descriptionScheme in self.descriptionSchemes:
            s.extend(descriptionScheme.collectAll(classObj))
        return s
    
    # returns True, if this DesciptionScheme has no MediaTime Descriptor or a MediaTime Descriptor containing this frameId
    def containsFrameId(self, frameId):
        iDescriptors = 0; 
        for descr in self.descriptors:
            if isinstance(descr, MediaTime):
                if descr.startTime <= frameId and frameId < descr.startTime+descr.duration:
                    return True
                iDescriptors += 1
        
        if iDescriptors == 0:
            return True
        else:
            return False