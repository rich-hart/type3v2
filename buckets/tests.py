from django.test import TestCase

from .models import *

class TestModels(TestCase):       
    def test_relations(self):
        bucket = Bucket.objects.create()
        folder = Folder.objects.create(parent=bucket)
        file = File.objects.create(parent=folder)
        self.assertEqual(file.root,bucket)
