from django.test import TestCase

from .models import *

class TestModels(TestCase):       
    def test_file(self):
        import ipdb; ipdb.set_trace()
        bucket = Bucket.objects.create(name='test')
        folder = Folder.objects.create(parent=bucket)
        file = File.objects.create(parent=folder)


