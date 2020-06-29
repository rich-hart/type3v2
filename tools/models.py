from enum import Enum
from django.db import models
from project.storage_backends import StaticStorage



#https://docs.celeryproject.org/en/stable/userguide/configuration.html#conf-cache-result-backend
# PREPROSESSING TOOLS
class Tool(models.Model):
    # COMPUTER VISION
    # NLP
   
    pass

class NLP(Tool):
    pass

class TfIDF(Tool):
    _vectorizer = models.FileField(storage=StaticStorage())
    _labels = None
    NAMESPACE_ROOT = 'TFIDF_' #FIXME: TODO: Not implemented  
    class Namespace(Enum):
        LABELS = 'LABELS'

    @property
    def namespaces(self):
        return [value for _,value in enumerate( self.Namespace)]

    @property
    def vectorizer(self):
        return self._vectorizer

    @property
    def corpus(self):
        raise NotImplementedError()
#
#class Vector(MONGODB):
#    pass
    # CLASSIFIERING? 
    # MACHINE LEARNING?
