from __future__ import absolute_import, unicode_literals
from typing import List
import celery
from celery import shared_task
from bases.models import Object

HashObjects = List[str]
ModelObjects = List[Object]

class CTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@shared_task
def begin(*args,**kwargs):
    return args, kwargs

@shared_task
def mirror_bucket(*buckets,index=0):
    buckets[index].mirror('pdf')


@shared_task
def mirror_bucket(*buckets,index=0):
    buckets[index].mirror('pdf')

@shared_task
def copy_file(*files,index=0):
    files[index].copy()

@shared_task
def double(x):
    return x * 2

@shared_task
def triple(x):
    return x * 3

@shared_task
def stop(x):
    return x


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


