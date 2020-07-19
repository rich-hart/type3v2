from __future__ import absolute_import, unicode_literals
from typing import List
import celery
from celery import shared_task

from bases.models import Object
from .queue import RabbitMQ as Queue
HashObjects = List[str]
ModelObjects = List[Object]


from celery import Task

class Task(Task):
    _qconn = None

    @property
    def qconn(self):
        if self._qconn is None or self._qconn.is_closed:
            self._qconn = Queue().connection
        return self._qconn

@shared_task
def begin(*args,**kwargs):
    return args

@shared_task
def initialize(ids, index=0, format='pdf', **kwargs):
    object = Object.objects.get(id=ids[index])
    job = getattr(object,'job',object)
#    objects[index].mirror(format=format)
#    object.mirror(format=format)
#    object.save()
    return [job.bucket.id]

@shared_task(base=Task)
def mirror(ids, index=0, format='pdf', **kwargs):
    object = Object.objects.get(id=ids[index])
    object = getattr(object,'fsobject',object)
    object = getattr(object,'bucket',object)
#    objects[index].mirror(format=format)
    files = object.mirror(format=format)
    ids = [f.id for f in files]
    return ids

@shared_task
def start(*args, **kwargs):
    return args

@shared_task
def stop(*args, **kwargs):
    return args

#@shared_task
#def mirror_bucket(*buckets,index=0):
#    buckets[index].mirror('pdf')

@shared_task
def copy(ids,index=0, **kwargs):
    object = Object.objects.get(id=ids[index])
    object = getattr(object,'fsobject',object)
    object = getattr(object,'file',object)
    object.copy()
#    object.save() 
    return ids


@shared_task
def double(x):
    return x * 2

@shared_task
def triple(x):
    return x * 3



@shared_task
def end(x):
    return x

@shared_task
def execute(x):
    return x

@shared_task
def terminate(x):
    return x

@shared_task
def walk(buckets: HashObjects, index: int) -> HashObjects:
    raise NotImplementedError
    return files

@shared_task
def convert(index, *files): #PDF --> PNG, TODO: options
    raise NotImplementedError
    for image in images:
        image.cache()        
    return images

@shared_task
def save(index, *images):
    raise NotImplementedError
    return images
@shared_task
def train_svm(index, *vectors):
    raise NotImplementedError
    return {svm}



@shared_task
def nn_encode(index, *texts):
    raise NotImplementedError
    return vectors

@shared_task
def train_nn(index, *vectors):
    raise NotImplementedError
    return {nn}


@shared_task
def svm_classify(index, *vectors): #FIXME TODO How does `classifier` app do this?
    raise NotImplementedError
    return labels

@shared_task
def nn_classify(index, *vectors): #FIXME TODO How does `classifier` app do this?
    raise NotImplementedError
    return labels


