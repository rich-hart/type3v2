import os
import celery
from typing import List
import pymongo
from pymongo import MongoClient
import pytesseract
import pandas
from bases.models import Object
from celery import Celery
from celery.utils.log import get_task_logger


from buckets.models import *
from tools.models import *
from .tasks import *
#from .apps import worker_queue, get_task_logger
logger = get_task_logger(__name__)

HashObjects = List[str]
ModelObjects = List[Object]
#def scale(scalar: float, vector: Vector) -> Vector:
#    return [scalar * num for num in vector]


# TODO: Use partical filter for parameter search.
# NOTE: https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#first-steps-with-django
# NOTE: README: https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#using-the-shared-task-decorator

#FIXME TODO Decorate index!!!
# FIXME TODO Make general process factory for scheduling

object_hierarchy = [
    'fsobject',
    'bucket',
    'file',
    'image',
]

DEFAULT_SCHEDULE = {
     'mirror_bucket': [],
#    'double': ['triple']
}

DEFAULT_PROCEDURE = {
    'default': [],
}

#@worker_queue.task(bind=True, base=Task)
#def start(self, *args):
#    logger.info(self.request.id)
#    return args
#
#@worker_queue.task(bind=True, base=Task)
#def stop(self, *args):
#    logger.info(self.request.id)
#    return args

#@worker_queue.task(bind=True, base=Task)
#def begin(self,*args):
#    logger.info(self.request.id)
#    return args




#@worker_queue.task(bind=True, base=Task)
#def end(self,*args):
#    logger.info(self.request.id)
#    return args

#@worker_queue.task(bind=True, base=Task)
#def execute(self,*args):
#    logger.info(self.request.id)
#    return args
#
#@worker_queue.task(bind=True, base=Task)
#def terminate(self,*args):
#    logger.info(self.request.id)
#    return args


def retrieve(cast, index, *objects):
    object = objects[index]
    if not isinstance(object, Object):
        object = Object.objects.get(tag=object)

    for type in object_hierarchy:
        if hasattr(object, type):
            object = getattr(object, type)
        if cast == type:
            break
#    if hasattr(object,:
#        object = getattr(object,cast)
    return object

def process(objects: HashObjects, index: int, method: str, type: str) -> HashObjects: #TODO: options
    import ipdb; ipdb.set_trace()
    object = retrieve(type, index, *objects)
    objects = getattr(object, method)()
    return objects

def get_ext(path):
    tokens = os.path.basename(path).split(os.extsep)
    if len(tokens) ==2:
        return tokens[1]

def get_prefix(path):
    tokens = os.path.basename(path).split(os.extsep)
    return tokens[0]

#FIXME: DEPRICATED
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
    files[index].load()
    return files
from io import BytesIO
import PIL

def convert_to_images(index, *files):
    tags = []
    files[index].load()
    images = files[index].convert()
    for i in range(len(images)):
        name = get_prefix(files[i].name) + '.png'
        image = Image.objects.create(name = name, parent=files[index],format='png')
        images[index]
        image._pil = images[index]
        image.cache() # FIXME: TODO Save in new task
        tags.append(image.tag.hex)
    return tags

def ocr(index, *images):
    texts = [None] * len(images)
    images[index].load()
    name = get_prefix(images[index].name) + '.tsv'
    text = Text.objects.create(name = name, parent = images[index] )
    text._raw = pytesseract.image_to_data(images[index].pil)  
    text.cache() # FIXME: TODO Save in new task
    return [text.tag.hex]


from sklearn.feature_extraction.text import TfidfVectorizer
def tfidf(*tags):
    texts = [Text.objects.get(tag=t) for t in tags ]
    corpus = []
    for text in texts:
        text.load()
        frame = text.frame
        text_data = frame[frame.conf != -1]
        words = ' '.join(text_data.text.to_list())
        corpus.append(words)     
    tool = TfidfVectorizer(
            strip_accents='unicode',
            stop_words='english',
    )
    vectors = tool.fit_transform(corpus)
    labels = tool.get_feature_names()
    model = TfIDF.objects.create()
    model.store(tool, labels, vectors)
    #FIXME TODO save tool labels
    #db = tool.mongo_client[settings.MONGODB_NAME]
    # FIXME: TODO Need to save vectorizer pickle
    #  X_train_vectors = vectorizer.fit_transform(X_train_corpus)
    #  X_test_vectors = vectorizer.transform(X_test_corpus)
    #collection = db[tool.class_name]
    #collection.insert_one({})
#    collection.insert_one(vectors)
#    client = MongoClient(f"mongodb://{settings.MONGO_USERNAME}:"\ 
#                "{settings.MONGO_PASSWORD}@"\ 
#                "{settings.MONGO_HOST}/{MONGO_DATABASE}")
#    db = client['test-database']
#    collection = db['test-collection']
#    collection = tool.mongo_client[tool.class_name]
    #model.store(labels)
    #model.store(vectors)
    #model.store(tool)
    return [model.tag]


# X of shape (n_samples, n_features)
# y of class labels (strings or integers), of shape (n_samples):


def save_image(index, *images):
    file[index].save()
    return images




#@worker_queue.task
#def ocr(index,*images):
#    raise NotImplementedError
#    return texts

#@worker_queue.task
#def tfidf(index, *texts):
#    raise NotImplementedError
#    return vectors

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
#@worker_queue.task
#def convert(file, input='pdf', output='png'):
    # at some point cache image data for later processing
#    raise NotImplementedError


#@worker_queue.task
#def add(x, y):
#    return x + y



#@worker_queue.task(bind=True)
#def debug_task(self):
#    print('Request: {0!r}'.format(self.request))



