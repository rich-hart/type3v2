from django.test import TestCase

from .models import *

class TestModels(TestCase):       
    def test_bucket(self):
        Bucket.objects.create()
