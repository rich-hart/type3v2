import random
from django.db import models
from django.contrib.auth.models import User
from bases.models import Label
from tools.models import Tool
import uuid
#MONGO DB
#class Vector(MONGODB):
#     pass

#class TFIDF(Vector)
#     pass

#class NN(Vector):
#    pass

#FIXME: TODO 
#class Label(Map):
#  @property
#  def name(self):
#  return __str__
import random

class Classifier(Tool):
    LABEL_NAMESPACE = 'CLASSIFIER_LABELS'
    LABEL_INDEXSPACE = 'LABEL_INDEXS'
    SAMPLE_NAMESPACE = 'SAMPLE_SPACE'
    TEST_NAMESPACE = 'TEST_SPACE'
    TRAIN_NAMESPACE = 'TRAIN_SPACE'
    samples = models.UUIDField(
        primary_key = False,
        unique = True,
        editable = False,
    )
    seed = models.UUIDField(
        primary_key = False,
        unique = True,
        default = uuid.uuid4,
        editable = False,
    )
#    _labels = None

#    def train(self, *args, **kwargs):
#        raise NotImplementedError

#    @property
#    def labels(self):
#        if not self._labels:
            # TODO: use `object.tag` and uuid namespace 
            # to query classifier labels from Labels class
            # set the returned array of names equal to _labels      
#            raise NotImplementedError
#        return self._labels

    #NOTE: make a chioce and save it
#    def _classify(self, object):
#        if self.tag not in object.tags:
#            label = self.classify(object)
#            object.tags.append(label.id)

    #NOTE: Just return choice       
#    def classify(self, object):
#        raise NotImplementedError

#    class Meta:
#        abstract = True

        
class Random(Classifier):
    #TODO: random seed 
    def classify(self, *args): 
        label = random.choice(self.labels)
        return label

class Human(Classifier):
    profile = models.OneToOneField(
        'users.Profile',
        on_delete=models.CASCADE,
    )

    @property
    def seed(self):
        return self.profile.tag.hex

class SVM(Classifier):
    pass
#    @location.setter
#    def location(self, val):
#        pass
#    @property
#    def location(self):
#         return self.test.location if self.test else None

class ML(Classifier):
    #TODO: random seed 
    def train(self, *args, **kwargs):
        raise NotImplementedError

