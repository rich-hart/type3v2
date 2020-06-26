import random
from django.db import models
from django.contrib.auth.models import User
from bases.models import Label
from tools.models import Tool

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

class Classifier(Tool):
    LABEL_NAMESPACE = 'CLASSIFIER_LABELS'
    LABEL_INDEXSPACE = 'LABEL_INDEXS'
    SAMPLE_NAMESPACE = 'SAMPLE_SPACE'
    TEST_NAMESPACE = 'TEST_SPACE'
    TRAIN_NAMESPACE = 'TRAIN_SPACE'

    seed = None
    _labels = None

    @property
    def labels(self):
        if not self._labels:
            # TODO: use `object.tag` and uuid namespace 
            # to query classifier labels from Labels class
            # set the returned array of names equal to _labels      
            raise NotImplementedError
        return self._labels

    #NOTE: make a chioce and save it
    def _classify(self, object):
        if self.tag not in object.tags:
            label = self.classify(object)
            object.tags.append(label.id)

    #NOTE: Just return choice       
    def classify(self, object):
        raise NotImplementedError

    class Meta:
        abstract = True

        
class Random(Classifier):
    #TODO: random seed 
    def classify(self, *args): 
        label = random.choice(self.labels)
        return label

class Human(Classifier):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    @property
    def seed(self):
        return self.user.id

class ML(Classifier):
    #TODO: random seed 
    def train(self, *args, **kwargs):
        raise NotImplementedError

