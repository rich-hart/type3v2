from django.test import TestCase

from .models import *

class TestModels(TestCase):
#    def setUp(self):
#        self.user = .objects.create(username='test')
       
#    def test_profile(self):
#        profile = Profile.objects.create(user=self.user)
    def test_object_create(self):
        import ipdb; ipdb.set_trace()
        object = Object.objects.create()

