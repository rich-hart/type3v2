import random
from celery import signature
from unittest import mock

from django.test import TestCase



from buckets.models import Bucket, File

from bases.models import Object

from .apps import worker_queue

from .utils import *
SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'

random.seed(SEED)


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
    object = getattr(object,'fsobject')
    return object

# FIXME: TODO Use a LOT of mocking in tests.  I mean A LOT.
# NEED TO EXPLICETLY DECLAIR AND TEST Worker object iteration, / iterable.  
# FIXME: TODO Model celery tests off of groups, chains, chords doc,
# NOTE This will allow for proper syntax unit testing, without needing live workers 
class TestUtils(TestCase):
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
        expected = [file.tag]
        returned = self.target('walk',0, [bucket.tag])
        self.assertListEqual(expected, returned)


