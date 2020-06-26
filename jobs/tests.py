import unittest
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
#NOTE TEST INSTANCE
class TestBinaryClassificationJob(TestCase):
    @unittest.skip("NotImplemented")
    def test_job_owner_human(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_owner_random_bot(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_owner_smart_bot(self):
        self.fail("NotImplementedError")


class TestDemo(TestBinaryClassificationJob):
    def test_create_job(self):
        Classification.objects.create()

    def test_post_job(self):
        job_url = reverse('job-list')
        data = {
        }
        response = self.client.post(job_url, data,format='json') #follow=True
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#    @classmethod
#    def setUpClass(cls):
#        pass

#    def setUp(self):
#        pass


    def test(self):
        pass

#    def tearDown(self):
#        pass

#    @classmethod
#    def tearDownClass(cls):
#        pass


#NOTE: TEST ABSTRACTION
class TestJob(TestCase):
    @unittest.skip("NotImplemented")
    def test_create_job(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_start_job(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_status(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_metric(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_error(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_complete(self):
        self.fail("NotImplementedError")

  
