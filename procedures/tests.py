import random
from celery import signature

from django.test import TestCase



from buckets.models import Bucket, File


from .apps import worker_queue

from .utils import *
SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'

random.seed(SEED)

# FIXME: TODO Use a LOT of mocking in tests.  I mean A LOT.
# NEED TO EXPLICETLY DECLAIR AND TEST Worker object iteration, / iterable.  
# FIXME: TODO Model celery tests off of groups, chains, chords doc,
# NOTE This will allow for proper syntax unit testing, without needing live workers 
class TestUtils(TestCase):
    def target(self, task_name, objects, index=0):
        import ipdb; ipdb.set_trace()
        task = globals()[task_name]
        objects = task(objects,index)
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
        self.target('walk',[bucket.tag])



