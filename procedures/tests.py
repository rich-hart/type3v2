import random
import string
from celery import signature
from unittest import mock
from django.test import TestCase, override_settings


from django.conf import settings
from django.test import TestCase

from pdf2image import convert_from_path, convert_from_bytes
import PIL
from buckets.models import Bucket, File, FSObject

from bases.models import Object

from .apps import worker_queue

from .utils import *
SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'
TEST_DATA_DIR = os.path.join(os.getcwd(),'data','tests')
random.seed(SEED)

def gen_rand_str():
    # printing lowercase
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10)) 

#import os
#import mock


#def simple_urandom(length):
#    return 'f' * length


#class TestRandom(unittest.TestCase):
#    @mock.patch('os.urandom', side_effect=simple_urandom)
#    def test_urandom(self, urandom_function):
#        assert os.urandom(5) == 'fffff'
def mock_retrieve(index, *tags):
    tag = tags[index]
    object = Object.objects.get(tag=tag)
    fsobject = getattr(object,'fsobject')
    bucket = getattr(fsobject,'bucket')
    return bucket

# FIXME: TODO Use a LOT of mocking in tests.  I mean A LOT.
# NEED TO EXPLICETLY DECLAIR AND TEST Worker object iteration, / iterable.  
# FIXME: TODO Model celery tests off of groups, chains, chords doc,
# NOTE This will allow for proper syntax unit testing, without needing live workers
import csv


@override_settings(MONGODB_NAME='test_'+gen_rand_str()) 
class TestUtils(TestCase):

    @classmethod
    def setUpClass(cls,*args,**kwargs):
        super(cls, TestUtils).setUpClass(*args,**kwargs)
        m_client = FSObject().mongo_client
        self.mongodb = m_client[self.settings.MONGODB_NAME]

    @classmethod
    def setUpClass(cls,*args,**kwargs):
        super(cls, TestUtils).setUpClass(*args,**kwargs)
        m_client = FSObject().mongo_client
        self.mongodb = m_client[self.settings.MONGODB_NAME]
        mongo_client.drop_database(self.settings.MONGODB_NAME)

    @mock.patch('procedures.utils.retrieve', side_effect=mock_retrieve)
    def target(self, task_name, index, objects, *args):
        objects = process(objects, index, task_name)
        return objects

    def test_pdf_convert(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        file = File.objects.create(parent=bucket,name=TEST_FILE_NAME)
        file.load()
        self.assertIsNotNone(file.raw)
        images = convert_from_bytes(file.raw)
        self.assertTrue(len(images))

    def test_load_task(self):
        self.assertIn('procedures.utils.debug_task', worker_queue.tasks)

    def test_task_add(self):
        signature('procedures.utils.add', args=(2, 2), countdown=10)

    def test_load_task(self):
        self.assertIn('procedures.utils.add', worker_queue.tasks)

    def test_task_walk(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        file = File.objects.create(parent=bucket,name=TEST_FILE_NAME)
        expected = [
                    'folder_0/',
                    'folder_0/folder_1/',
                    'folder_0/folder_1/sample.pdf',
                    'folder_0/folder_2/',
                    'test.pdf',
        ]
        returned = self.target('list_objects',0, [bucket.tag])
        self.assertListEqual(expected, returned)

    def test_mirror_pdfs(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        keys = bucket.list_objects()
        objects = mirror_pdfs(keys)
        self.assertTrue(len(objects))

    def test_convert_to_images(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        file = File.objects.create(parent=bucket,name=TEST_FILE_NAME,format='pdf')
        tags = convert_to_images(0,*[file])
        self.assertTrue(len(tags))
        image = Image.objects.get(tag=tags[0]) 
        data = image.cache_client.get(image.tag.hex) 
        self.assertIsNotNone(data)

    def test_ocr_images(self):
        path = os.path.join(TEST_DATA_DIR,'test.png')
        pil = PIL.Image.open(path)
        image = Image.objects.create(name=TEST_FILE_NAME,format='png')
        image._pil = pil
        image.cache()
        tags = ocr(0,*[image])
        self.assertTrue(len(tags))
        cache = FSObject().cache_client
        data = cache.get(tags[0])
        self.assertIsNotNone(data)
    def cleanUpPaths(self):
        for path in self.test_paths:
            os.remove(path)
    def test_tfidf(self):
        import ipdb; ipdb.set_trace()
        path = os.path.join(TEST_DATA_DIR,'test.tsv')
        tags = []
        text = Text.objects.create(name=TEST_FILE_NAME,format='tsv')
        tags.append(text.tag.hex)
        with open(path,'rb') as fp:
            text._raw = fp.read()
            text.frame
            text.cache()
            for r_path in range(10):
                r_text = Text.objects.create(name=TEST_FILE_NAME,format='tsv')
                r_text._frame = text._frame.copy()
                for i in range(len(r_text._frame['text'])):
                    r_text._frame[i] = gen_rand_str()
                r_text._raw = r_text._frame.to_csv(sep='\t')
                r_text.cache()
                tags.append(r_text.tag.hex)
        with self.settings(MONGODB_NAME='test_'+gen_rand_str()):
            vectors, labels = tfidf(*tags)

