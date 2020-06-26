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

    def setUp(self):
        self.test_user = User.objects.create(username='test')
        Profile.objects.create(user=self.test_user)

    def test_create_job(self):
        owner  = self.test_user
        Classification.objects.create(owner=owner.profile)

    def test_object_set(self):
        owner = self.test_user 
        job = Classification.objects.create(owner=owner.profile)

        test_objects = [User.objects.create(username=str(i)) for i in range(5)]

        for user in test_objects:
            Profile.objects.create(user=user)

        for test_object in test_objects:
            job.tag_object(test_object.profile)
            test_object.save()
        
        job = Classification.objects.get(id=job.id)
        expected = sorted(list([ u.profile.id for u in test_objects ]))
        returned = sorted(list([ p.id for p in  job.object_set]))
        self.assertListEqual(expected, returned)

    def test_get_jobs(self):
        job_url = reverse('job-list')
        response = self.client.get(job_url, format='json') #follow=True
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_job(self):
        job_url = reverse('job-list')
        data = {
            'owner': self.test_user.profile,
        }
        self.client.force_login(self.test_user)
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

  
