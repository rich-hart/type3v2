from django.db import models

from bases import Base
#class Problem(models.Model):
#    pass
# documents in a bucket need to be classified as libor / non-libor

class Job(Base):
    description = None
    #TODO: owner

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
    metric = models.DecimalField(max_digits=1, decimal_places=5)
    error = models.DecimalField(max_digits=1, decimal_places=5)

    def save(self, *args, **kwargs):
        self.metric = self.job.metric
        self.error = self.job.error
        super(Progress, self).__init__(*args, **kwargs)


class DocumentBinaryClassification(Job):
    description = "classify documents in a bucket"
    #TODO: foriegn key to bucket
