import uuid
from django.core.management import call_command
from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from tagging.models import Tag, TaggedItem
from bases.models import Choice, Label, Object, Base

from buckets.models import Bucket, File
from classifiers.models import Classifier, Human as HumanClassifier
from users.models import Profile
from procedures.utils import RabbitMQ as Queue
#class Problem(models.Model):
#    pass
# documents in a bucket need to be classified as libor / non-libor

class Job(Base):
    description = None
    owner = models.ForeignKey(
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

    @property
    def queue_name(self):
        return 'job_queue_' + self.tag.hex[:8]

    def run(self):
        raise NotImplementedError


    @property
    def metric(self):
        raise NotImplementedError

    @property
    def error(self):
        raise NotImplementedError

class Assignee(Base):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
#        related_name='assignee_job',
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

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
#    classifier = models.OneToOneField('classifiers.Classifier', on_delete=models.CASCADE)
    #TODO: classifier = #foriegn key Classifier, try to use Model string name for import
    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.CASCADE,
    )
    @property
    def metric(self):
        #FIXME: TODO: Return objects % tagged in object_set by classifier
        raise NotImplementedError

    @property
    def error(self):
        if isinstance(self.classifier, HumanClassifier):
            return float('nan')
        raise NotImplementedError

    def start(self):
        call_command('execute', self.id,'--type=job')    

    def run(self):
        raise NotImplementedError

def create_job_queue(sender, instance, created, **kwargs):
    if created:
        Queue.create(instance.queue_name)

def delete_job_queue(sender, instance, *args, **kwargs):
    Queue.delete(instance.queue_name)

def tag_file_with_job(sender, instance, created, **kwargs):
    root = instance.root
    if isinstance(root, Bucket):
        for job in root.classification_set.all():
            if job.tag not in instance.tags:
                job.tag_object(instance)


signals.post_save.connect(receiver=tag_file_with_job, sender=File)

#FIXME: How to consolidate subclass signals?
signals.pre_delete.connect(receiver=delete_job_queue, sender=Job)
signals.post_save.connect(receiver=create_job_queue, sender=Job)
signals.pre_delete.connect(receiver=delete_job_queue, sender=Classification)
signals.post_save.connect(receiver=create_job_queue, sender=Classification)
