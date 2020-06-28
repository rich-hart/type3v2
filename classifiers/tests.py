from time import sleep
import os
import unittest
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.core.management import call_command

from .models import *
from .views import *
#NOTE TEST INSTANCE
class ClassificationView(TestCase):
    @unittest.skip("NotImplemented")
    def test_job_owner_human(self):
        self.fail("NotImplementedError")


    @unittest.skip("Patch test view broken, dev works")
    def test_start_job(self):
        import ipdb; ipdb.set_trace()
        factory = APIRequestFactory()
        view = JobViewSet.as_view({'get':'start'})

        self.test_user = User.objects.create(username='test')
        Profile.objects.create(user=self.test_user)
        job = Classification.objects.create(owner=self.test_user.profile)
        job_url = reverse('job-list')
        job_url = os.path.join(job_url,str(job.id),'start') + '/?format=json'
        data = {
            'owner': self.test_user.profile,
#            'status': Job.Status.
        }
        #FIXME: TODO
        request = factory.patch(job_url,data=data)
        response = view(request,pk = job.pk)
#        self.client.force_login(self.test_user)
#        response = self.client.patch(job_url, data,format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

