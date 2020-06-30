from time import sleep
import os
import json
import unittest
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.core.management import call_command

from tools.models import TfIDF

from .models import *
from .utils import *
from .views import *
SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'
TEST_DATA_DIR = os.path.join(os.getcwd(),'data','tests')
random.seed(SEED)

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


class ClassificationUtils(TestCase):

    def test_classifier(self):
        import ipdb; ipdb.set_trace()
        path = os.path.join(TEST_DATA_DIR,'vectors.json')
        features = TfIDF.objects.create()
        with open(path,'r') as fp:
            vectors = json.load(fp)
        [ v.pop('_id') for v in vectors] 
        features.vectors.insert_many(vectors)
        classifier = SVM.objects.create()
        classifier.samples = features.address 
        train(classifier)
