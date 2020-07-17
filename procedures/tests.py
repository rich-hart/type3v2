import random
import string
from time import sleep
import json
from celery import signature
from unittest import mock
from django.test import TestCase, override_settings
from neomodel import db, clear_neo4j_database

from django.conf import settings
from django.test import TestCase

from pdf2image import convert_from_path, convert_from_bytes
import PIL
from buckets.models import Bucket, File, FSObject

from bases.models import Object
from project.celery import app as celery_app

from .utils import *
from .models import *
SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'
TEST_DATA_DIR = os.path.join(os.getcwd(),'data','tests')
random.seed(SEED)

def gen_rand_str():
    # printing lowercase
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10)) 


from neomodel import db, clear_neo4j_database
from django.core.management import call_command

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'

class TestTasks(TestCase):
    def setUp(self):
        clear_neo4j_database(db)

    def test(self):
        import ipdb; ipdb.set_trace()
        call_command('load')
        sleep(.3)
        self.assertTrue(len(Task.nodes.all()))
        call_command('execute')

    def test_mirror(self):
        import ipdb; ipdb.set_trace()
        bucket,_ = Bucket.objects.get_or_create(name=TEST_BUCKET_NAME)
        files = mirror_bucket(*[bucket])

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

TEST_MONGODB_NAME='test_'+gen_rand_str()

@override_settings(MONGODB_NAME='test_project') 
class TestUtils(TestCase):

#    @classmethod
#    def setUpClass(cls,*args,**kwargs):
#        super(cls, TestUtils).setUpClass(*args,**kwargs)
#        m_client = FSObject().mongo_client
#        cls.mongodb = m_client[TEST_MONGODB_NAME]

#    @classmethod
#    def tearDownClass(cls,*args,**kwargs):
#        super(cls, TestUtils).tearDownClass(*args,**kwargs)
#        m_client = FSObject().mongo_client
#        mongodb = m_client[TEST_MONGODB_NAME]
#        m_client.drop_database(TEST_MONGODB_NAME)

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
        self.assertIn('procedures.utils.debug_task', celery_app.tasks)

    def test_task_add(self):
        signature('procedures.utils.add', args=(2, 2), countdown=10)

    def test_load_task(self):
        self.assertIn('procedures.utils.add', celery_app.tasks)

    def test_task_walk(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        file = File.objects.create(parent=bucket,name=TEST_FILE_NAME)
        expected = set([
                    'folder_0/',
                    'folder_0/folder_1/',
                    'folder_0/folder_1/sample.pdf',
                    'folder_0/folder_2/',
                    'test.pdf',
                    'media/', 
                    'static/',
        ])
        returned = set(self.target('list_objects',0, [bucket.tag]))
        self.assertSetEqual(expected, returned)

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
        sleep(.3)
        self.assertIsNotNone(data)

    def test_ocr_images(self):
        path = os.path.join(TEST_DATA_DIR,'test.png')
        pil = PIL.Image.open(path)
        image = Image.objects.create(name=TEST_FILE_NAME,format='png')
        image._pil = pil
        image.cache()
        tags = ocr(0,*[image])
        self.assertTrue(len(tags))
        sleep(.3)
        cache = FSObject().cache_client
        data = cache.get(tags[0])
        self.assertIsNotNone(data)
    def cleanUpPaths(self):
        for path in self.test_paths:
            os.remove(path)
    def test_tfidf(self):
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
#        with self.settings(MONGODB_NAME='test_'+gen_rand_str()):
        [tag] = tfidf(*tags)

        returned = len([ d  for d in TfIDF.objects.get(tag=tag).vectors.find()])
        expected = 0
        self.assertGreater(returned,expected)
    
    def test_classifier(self):
        path = os.path.join(TEST_DATA_DIR,'vectors.json')
        features = TfIDF.objects.create()
        with open(path,'r') as fp:
            vectors = json.load(fp)
        [ v.pop('_id') for v in vectors] 
        features.vectors.insert_many(vectors)

        #tags = []
        #text = Text.objects.create(name=TEST_FILE_NAME,format='tsv')
        #tags.append(text.tag.hex)
#        with open(path,'rb') as fp:
#            text._raw = fp.read()
#            text.frame
#            text.cache()
#            for r_path in range(10):
#                r_text = Text.objects.create(name=TEST_FILE_NAME,format='tsv')
#                r_text._frame = text._frame.copy()
#                for i in range(len(r_text._frame['text'])):
#                    r_text._frame[i] = gen_rand_str()
#                r_text._raw = r_text._frame.to_csv(sep='\t')
#                r_text.cache()
#                tags.append(r_text.tag.hex)
#        with self.settings(MONGODB_NAME='test_'+gen_rand_str()):
#        [tag] = tfidf(*tags)
#        returned = [ d  for d in TfIDF.objects.get(address=tag)[0].vectors.find()]

