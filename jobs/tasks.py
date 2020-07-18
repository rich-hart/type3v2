from __future__ import absolute_import, unicode_literals
from typing import List
import celery
from celery import shared_task
from .models import Job

@shared_task
def initialize(ids, index=0, case='classification', **kwargs):
    job = Job.objects.get(id=ids[index])
    job = getattr(job,case,job)
#    objects[index].mirror(format=format)
#    object.mirror(format=format)
#    object.save()
    return [job.bucket.id]


