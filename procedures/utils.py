from typing import List


from bases.models import Object
from .apps import worker_queue



HashObjects = List[str]
ModelObjects = List[Object]
#def scale(scalar: float, vector: Vector) -> Vector:
#    return [scalar * num for num in vector]


# TODO: Use partical filter for parameter search.
# NOTE: https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#first-steps-with-django
# NOTE: README: https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#using-the-shared-task-decorator

#FIXME TODO Decorate index!!!
# FIXME TODO Make general process factory for scheduling

def retrieve(index, *objects, cast='fsobject'):
    object = objects[index]
    if not isinstance(object, Object):
        raise NotImplementedError('need to figure out object loading')
    if cast:
        object = getattr(object,cast)
    return object

def process(objects: HashObjects, index: int, method: str) -> HashObjects: #TODO: options
    object = retrieve(index, *objects)
    objects = getattr(object, method)()
    return objects

@worker_queue.task
def walk(buckets: HashObjects, index: int) -> HashObjects:
    raise NotImplementedError
    return files

@worker_queue.task
def convert(index, *files): #PDF --> PNG, TODO: options
    raise NotImplementedError
    for image in images:
        image.cache()        
    return images

@worker_queue.task
def save(index, *images):
    raise NotImplementedError
    return images

@worker_queue.task
def ocr(index,*images):
    raise NotImplementedError
    return texts

@worker_queue.task
def tfidf(index, *texts):
    raise NotImplementedError
    return vectors

@worker_queue.task
def train_svm(index, *vectors):
    raise NotImplementedError
    return {svm}



@worker_queue.task
def nn_encode(index, *texts):
    raise NotImplementedError
    return vectors

@worker_queue.task
def train_nn(index, *vectors):
    raise NotImplementedError
    return {nn}


@worker_queue.task
def svm_classify(index, *vectors): #FIXME TODO How does `classifier` app do this?
    raise NotImplementedError
    return labels

@worker_queue.task
def nn_classify(index, *vectors): #FIXME TODO How does `classifier` app do this?
    raise NotImplementedError
    return labels

# TODO Make create (update or create) `Task` models command

#In [3]: def test(*args): print(args)                                                                   
#In [4]: test(*{'a','b','c'})                                                                           
#        ('c', 'b', 'a')
#
#
#In [2]: set(['root_hash'])                                                                             
#Out[2]: {'root_hash'}
#
#
#In [8]: test(*{'root_hash'})                                                                           
#Out[8]: {'doc1,doc2,doc3'}
#
#
#In [10]: test(*{'doc1,doc2,doc3'})                                                                     
#Out[10]: 
#{'img0',
# 'img1',
# 'img2',
# 'img3',
# 'img4',
# 'img5',
# 'img6',
# 'img7',
# 'img8',
# 'img9'}
#
#NOTE FIXME Build out syntax for all tasks linearly 
# use lists not sets for worker indexing 
# need a `decorator to wrap hash list serialziation. 
# (wont need rest framework most likely for serilaization
# a simple list of tags should do the trick


#NOTE FIXME WARNING `convert` might be too general for pratical server
@worker_queue.task
def convert(file, input='pdf', output='png'):
    # at some point cache image data for later processing
    raise NotImplementedError


@worker_queue.task
def add(x, y):
    return x + y



@worker_queue.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

