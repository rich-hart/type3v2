import os
from typing import List


from bases.models import Object
from buckets.models import *
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

def get_ext(path):
    tokens = os.path.basename(path).split(os.extsep)
    if len(tokens) ==2:
        return tokens[1]

def get_prefix(path):
    tokens = os.path.basename(path).split(os.extsep)
    return tokens[0]

def mirror_pdfs(keys):
#    for key in keys:
    folder_keys = [os.path.dirname(p) for p in keys if get_ext(p)=='pdf']     
    pdf_keys = [os.path.basename(p) for p in keys if get_ext(p)=='pdf']     
    files = []
    for folder_key, pdf_key in zip(folder_keys, pdf_keys):
        if folder_key:
            parent = Folder.objects.create(name=folder_key)
        else:
            parent = None #FIXME: NEED TO LINK TO BUCKET
        file = File.objects.create(name=pdf_key,format='pdf',parent=parent)
        files.append(file)
    return files

def load_file(index, *files):
    file[index].load()
    return files

def convert_to_images(index, *files):
    import ipdb; ipdb.set_trace()
    files[index].load()
    images = files[index].convert()
    for i in range(len(images)):
        name = get_prefix(files[i].name) + '.png'
        image = Image.objects.create(name = name, parent=files[index])
        image._array = np.array(images[index])
        image._raw = image._array.tostring()
        image.cache()
    return images

def save_image(index, *images):
    file[index].save()
    return images



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

