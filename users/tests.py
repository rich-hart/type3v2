from django.test import TestCase

from .models import *

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
       
    def test_profile(self):
        profile = Profile.objects.create(user=self.user)
