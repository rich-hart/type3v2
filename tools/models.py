from enum import Enum
from django.db import models
from project.storage_backends import StaticStorage
from bases.models import Memory
from buckets.models import FSObject

#https://docs.celeryproject.org/en/stable/userguide/configuration.html#conf-cache-result-backend
# PREPROSESSING TOOLS
from django.conf import settings
class Tool(FSObject):
    # COMPUTER VISION
    # NLP
    pass

class NLP(Tool):
    pass
from scipy.sparse import csr_matrix



class TfIDF(Tool):
    _vectorizer = models.FileField(storage=StaticStorage())
    _vectors = None
    _labels = None
    _memory = None

    memory = models.OneToOneField(
        'bases.Memory',
        #on_delete=models.CASCADE,
        on_delete=models.DO_NOTHING,
        related_name='+',
        #related_name='supervisor_of',
    )

    # NOTE: Need to move to Base Object class
    class Namespace(Enum):
    #    ROOT = 'PROJECT_' #FIXME cant get superclass of root to work
        LABELS = 'LABELS'
    
        @property
        def uuid(self):
            value = self.ROOT + self.value
            return uuid.uuid3(uuid.NAMESPACE_DNS, value).hex

        @property
        def hash(self):
            return self.uuid

#    @property
#    def namespaces(self):
#        return [ _, namespace in enumerate(self.Namespace) ]

#    @property
#    def memory(self):
#        if not self._memory:
#            self._memory = Memory.objects.get(id=self.tag.hex)
#        return self._memory


    @property
    def namespaces(self):
        return [value for _, value in enumerate( self.Namespace)]

    @property
    def vectorizer(self):
        raise NotImplementedError
        return self._vectorizer

    @property
    def corpus(self):
        raise NotImplementedError()

    @property
    def vectors(self):
        raise NotImplementedError()

    @property
    def labels(self):
        raise NotImplementedError()

    def store(self, data):
        if isinstance(data, csr_matrix):
            import ipdb; ipdb.set_trace()
            raise NotImplementedError(f'save {data} to mongodb')
        elif isinstance(data,list):
            import ipdb; ipdb.set_trace()
            #self.memory.data 
            raise NotImplementedError(f'save {data} to general memory')
        else:
            import ipdb; ipdb.set_trace()
            raise NotImplementedError()
#
#class Vector(MONGODB):
#    pass
    # CLASSIFIERING? 
    # MACHINE LEARNING?
