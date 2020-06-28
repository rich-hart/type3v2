import random
import string 

from django.test import TestCase

from .models import *

SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'

random.seed(SEED)

class TestModels(TestCase): 
    def test_relations(self):
        bucket = Bucket.objects.create()
        folder = Folder.objects.create(parent=bucket)
        file = File.objects.create(parent=folder)
        self.assertEqual(file.root,bucket)

    def test_load(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        file = File.objects.create(parent=bucket,name=TEST_FILE_NAME)
        file.load()
        self.assertIsNotNone(file.raw)
