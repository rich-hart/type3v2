import os
from enum import Enum
import uuid
import pandas as pd
import numpy as np
from django.conf import  settings
from django.db import models
from project.storage_backends import StaticStorage, MediaStorage
from bases.models import Memory, ROOT_NAMESPACE
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


#class Label(Memory):
#    pass
from django.core.files.uploadedfile import SimpleUploadedFile
import pickle
import io


class TfIDF(Tool):
    _vectorizer = models.FileField(storage=MediaStorage())
    _vectors = None
    _labels = None
    _memory = None

    address = models.UUIDField(
        unique = True,
        default = uuid.uuid4,
        editable = False,
    )
    @property
    def vectors(self):
        if not self._vectors:
            self._vectors = self.collection[self.address]
        return self._vectors

    #@classmethod
    def store(self, tool, labels, vectors):
        stream = io.BytesIO()
        pickle.dump( tool, stream )
        stream.flush()
        stream.seek(0)
        key = os.path.join(self.class_name, self.address.hex)
        self.s3_client.upload_fileobj(stream, settings.AWS_STORAGE_BUCKET_NAME, key)        
        self.save()
        array = vectors.toarray()
        frame = pd.DataFrame(array)
        #frame.to_json(stream)
        records = frame.rename(columns=dict(enumerate(labels))).to_dict('records')
#        self.collection[self.address]  
        self.vectors.insert_many(records)
        #self.collection.insert(???)

    # NOTE: Need to move to Base Object class
    class Namespace(Enum):
    #    ROOT = 'PROJECT_' #FIXME cant get superclass of root to work
        LABELS = 'LABELS'
    
        @property
        def uuid(self):
            value = ROOT_NAMESPACE + self.value
            return uuid.uuid3(uuid.NAMESPACE_DNS, value)

#        @property
#        def hash(self):
#            return self.uuid

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

#    @property
#    def vectors(self):
#        raise NotImplementedError()

    @property
    def labels(self):
        raise NotImplementedError()

#    def create(self,*args, **kwargs):
#        super(self, TfIDF).create(address_id=uuid.uuid4().hex,*args, **kwargs)
#    @property 
#    def memory(self):
#        if not self._memory:
#            self._memory = Memory.objects.update_or_create(id=self.address)
#        return self._memory

#    def store(self, data):
##      Memory.objects.update_or_create(id=self.address.hex)
#        if isinstance(data, csr_matrix):
#            raise NotImplementedError(f'save {data} to mongodb')
#        elif isinstance(data, list):
#            #self.memory.data
#            for i in range(len(data)):
#                encoded_data = Memory.encode(data[i])
#                Memory.store(self.Namespace.LABELS.uuid, self.address,encoded_data)    
##                memory.store(self.Namespace.LABELS.hash, encoded_data) 
#            #memory = Memory.objects.update_or_create(id=self.address)
#            #raise NotImplementedError(f'save {data} to general memory')
#        else:
#            raise NotImplementedError()
#
#class Vector(MONGODB):
#    pass
    # CLASSIFIERING? 
    # MACHINE LEARNING?
