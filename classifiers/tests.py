from time import sleep
import os
import json
import unittest
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.management import call_command

from tools.models import TfIDF

from bases.models import Object, Memory

from users.models import User, Profile

from buckets.models import *
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
    def setUp(self):
        self.test_user = User.objects.create(username='test')
        Profile.objects.create(user=self.test_user)
        self.human_classifier = Human.objects.create(profile=self.test_user.profile)
        self.bucket = Bucket.objects.create()
        self.folder = Folder.objects.create(parent=self.bucket)
        self.file = File.objects.create(parent=self.folder)

    def tearDown(self):
        User.objects.all().delete()
        Object.objects.all().delete()

    @unittest.skip("NotImplemented")
    def test_job_owner_human(self):
        self.fail("NotImplementedError")


    def test_human_classifier(self):
#        import ipdb; ipdb.set_trace()
#        self.test_user = User.objects.create(username='test')
#        Profile.objects.create(user=self.test_user)

#        human = Human.object.create(profile=self.test_user.profile)
        
        self.human_classifier.tag_object(self.file) 
        data = Memory.encode('libor')
        Memory.objects.create(id=self.human_classifier.Namespace.LABEL.uuid,data_beta=data)
        #self.file.tags.append(self.human_classifier.tag)
        classifier_url = reverse('classifier-list')
        self.client.force_login(self.test_user)
        response = self.client.get(classifier_url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        factory = APIRequestFactory()
#        view = JobViewSet.as_view({'get':'start'})
#
#        self.test_user = User.objects.create(username='test')
#        assignee = User.objects.create(username='assignee')
#
#        Profile.objects.create(user=self.test_user)
#        job = Classification.objects.create(owner=self.test_user.profile)
#        job_url = reverse('job-list')
#        job_url = os.path.join(job_url,str(job.id),'start') + '/?format=json'
#        data = {
#            'owner': self.test_user.profile,
#            'profile_set': [assignee.profile.id],
##            'status': Job.Status.
#        }
#        #FIXME: TODO
#        request = factory.patch(job_url,data=data)
#        response = view(request,pk = job.pk)
##        self.client.force_login(self.test_user)
##        response = self.client.patch(job_url, data,format='json', follow=True)
#        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


class ClassificationUtils(TestCase):
    @unittest.skip("function incomplete")
    def test_classifier(self):
        path = os.path.join(TEST_DATA_DIR,'vectors.json')
        features = TfIDF.objects.create()
        with open(path,'r') as fp:
            vectors = json.load(fp)
        [ v.pop('_id') for v in vectors] 
        features.vectors.insert_many(vectors)
        classifier = SVM.objects.create()
        classifier.samples = features.address 
        train(classifier)
