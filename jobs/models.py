import uuid
from django.apps import apps
from django.db import models
from django.contrib.auth.models import User

from tagging.models import Tag, TaggedItem
from bases.models import Base, Choice, Label 

from buckets.models import Bucket
from classifiers.models import Classifier, Human as HumanClassifier
from users.models import Profile
#class Problem(models.Model):
#    pass
# documents in a bucket need to be classified as libor / non-libor

class Job(Base):
    description = None
    owner = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )
    class Status(Choice):
        UNKNOWN = 'UN' 
        CREATED = 'CR'
        PENDING = 'PN' #Might not use
        STARTED = 'ST'
        COMPLETE = 'CP'

    status = models.CharField(
        max_length=2,
        #choices=Status, #TODO fix this, make PR to django official cite
        choices=Status.get_choices(),
        default=Status.UNKNOWN.value,
    )

    def run(self):
        raise NotImplementedError


    @property
    def metric(self):
        raise NotImplementedError

    @property
    def error(self):
        raise NotImplementedError

class ProgressReport(Base):
    #foriegn key to job
    #NOTE: restrict update in view
    # _metric = [0,1]
    metric = models.FloatField()
    error = models.FloatField()

    def save(self, *args, **kwargs):
        self.metric = self.job.metric
        self.error = self.job.error
        super(Progress, self).save(*args, **kwargs)



class Classification(Job):
    description = "classify the instances in an object set"
    #TODO: classifier = #foriegn key Classifier, try to use Model string name for import

    @property
    def metric(self):
        #FIXME: TODO: Return objects % tagged in object_set by classifier
        raise NotImplementedError

    @property
    def error(self):
        if isinstance(self.classifier, HumanClassifier):
            return float('nan')
        raise NotImplementedError

