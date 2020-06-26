from django.db import models
from django.contrib.auth.models import User

from tagging.models import Tag
from bases.models import Base, ChoiceType

from buckets.models import Bucket
from classifiers.models import Classifier, Human as HumanClassifier

#class Problem(models.Model):
#    pass
# documents in a bucket need to be classified as libor / non-libor

class Job(Base):
    description = None
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    class Status(ChoiceType):
        UNKNOWN = 'UN' 
        COMPLETE = 'CP'
        CREATED = 'CR'

    status = models.CharField(
        max_length=2,
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
    #TODO: classifier = #foriegn key Classifier

    @property
    def object_set(self):
        objects = Tag.objects.filter(name=self.tag).value('object')
        return objects

    @property
    def metric(self):
        #FIXME: TODO: Return objects % tagged in object_set by classifier
        raise NotImplementedError

    @property
    def error(self):
        if isinstance(self.classifier, HumanClassifier):
            return float('nan')
        raise NotImplementedError

