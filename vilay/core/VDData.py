from vilay.core.DescriptionScheme import DescriptionScheme
from vilay.core.Film import Film

class VDData:
    def __init__(self, film=None):
        self.dsRoot = DescriptionScheme("Feature Film")
        self.setFilm(film)
        
    def setFilm(self, film):
        if film is None:
            self.film = None
        elif type(film) == str:
            self.film = Film(film)
        elif isinstance(film, Film):
            self.film = film
        else: 
            raise("unknown type of input")
              
    def addDescriptionScheme(self, newSemanticObject, oldSemanticObject):
        return oldSemanticObject.addDescriptionScheme(newSemanticObject)
    
    def addDescriptor(self, detectObject):
        self.descriptors.append(detectObject)
    
