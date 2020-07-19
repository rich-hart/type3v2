from time import sleep
import os
import unittest
import unittest
import unittest.mock
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.core.management import call_command
from buckets.models import File, Bucket
from procedures.utils import RabbitMQ as Queue

from .models import *
from .views import *

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'

#NOTE TEST INSTANCE
class TestSignals(TestCase):
    def setUp(self):
        Job.objects.all().delete()
        User.objects.all().delete()
        Object.objects.all().delete()
#        File.objects.all().delete()
        self.test_user = User.objects.create(username='test')

    def test_file_signal(self):
        bucket = Bucket.objects.create(name='test')
        job = Classification.objects.create(owner=self.test_user.profile,bucket=bucket)
        queue = Queue(job.queue_name) 
        self.assertFalse(queue.qsize())
        file = File.objects.create(name='test',parent=bucket)
        self.assertIn(job.tag.hex, [t.name for t in file.tags])
        self.assertTrue(queue.qsize())

    def test_job_signal(self):
        bucket = Bucket.objects.create(name='test')
#        job = Classification.objects.create(owner=self.test_user.profile,bucket=bucket)
        job = Job.objects.create(owner=self.test_user.profile)
        self.assertTrue(Queue.exists(job.queue_name))
#        self.assertTrue0(manager.channel.queue_declare(job.queue_name,passive=True))

class TestWorker(TestCase):
    def setUp(self):
        User.objects.all().delete()
#        self.patcher = unittest.mock.patch('procedures.utils.RabbitMQ')
#        self.mockQueue = self.patcher.start()

#    def target(self, messages):
#        instance = self.mockQueue.return_value
#        instance.__iter__.return_value = iter(messages)
#        main()
#        self.assertGreater(len(instance.put.call_args_list),0)
#        return instance.put.call_args_list[0][0][0]['mappedData']

#    def tearDown(self):
#        self.patcher.stop()

    def test(self):
        pass


class TestBinaryClassificationJob(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.test_user = User.objects.create(username='test')

    def test_perform(self):
        import ipdb; ipdb.set_trace()
        user = User.objects.create(username='assignee')

        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        job = Classification.objects.create(owner=self.test_user.profile,bucket=bucket)
        file = File.objects.create(name=TEST_FILE_NAME, parent=bucket)
        file.copy()
#        file.save()
        perform_url = reverse('job-perform',args=[1])    + '?format=json' 
        self.client.force_login(self.test_user)
        response = self.client.get(perform_url, format='json', follow=True, content_type='application/json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {}
        response = self.client.post(perform_url, data,format='json', follow=True, content_type='application/json')
        import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_job_owner_human(self):

        user = User.objects.create(username='assignee')

#        Profile.objects.create(user=self.test_user)
#        Profile.objects.create(user=user)
       
        job_url = reverse('job-list')  + '?format=json' 

        data = {
            'profile_set': [user.profile.id],
            'classification':{'bucket': 'test-rsftzmqvua'},
        }

        self.client.force_login(self.test_user)
#        manager = Queue()
        response = self.client.post(job_url, data,format='json', follow=True, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        job = Job.objects.get(id=response.data['id'])
        self.assertTrue(Queue.exists(job.queue_name))

    @unittest.skip("NotImplemented")
    def test_job_owner_random_bot(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_owner_smart_bot(self):
        self.fail("NotImplementedError")


class TestDemo(TestBinaryClassificationJob):
    def setUp(self):
        User.objects.all().delete()

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


from rest_framework.test import APIRequestFactory

#NOTE: TEST ABSTRACTION
class TestJob(TestCase):
    def setUp(self):
        User.objects.all().delete()

    @unittest.skip("NotImplemented")
    def test_create_job(self):
        self.fail("NotImplementedError")

    @unittest.skip("Patch test view broken, dev works") 
    def test_start_job(self):
        factory = APIRequestFactory()
        view = JobViewSet.as_view({'get':'start'})

        self.test_user = User.objects.create(username='test')
        Profile.objects.create(user=self.test_user)
#        job = Classification.objects.create(owner=self.test_user.profile)
        job_url = reverse('job-list')
        job_url = os.path.join(job_url,str(job.id),'start') + '/?format=json' 
        data = {
            'owner': self.test_user.profile,
            'bucket': 'test-pitypincio',
#            'status': Job.Status.
        }
        #FIXME: TODO
        request = factory.patch(job_url,data=data)
        response = view(request,pk = job.pk)                    
#        self.client.force_login(self.test_user)
#        response = self.client.patch(job_url, data,format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    @unittest.skip("Patch test view broken, dev works") 
    def test_start_command(self):
        #factory = APIRequestFactory()
        #view = JobViewSet.as_view({'get':'start'})

        self.test_user = User.objects.create(username='test')
        Profile.objects.create(user=self.test_user)
        job = Classification.objects.create(owner=self.test_user.profile)
        call_command('start', job.id)
        sleep(.3)
        job = Job.objects.get(pk=job.id)
        #job_url = reverse('job-list')
        #job_url = os.path.join(job_url,str(job.id),'start') + '/?format=json' 
        #data = {
        #    'owner': self.test_user.profile,
#            'status': Job.Status.
        #}
        #FIXME: TODO
        #request = factory.patch(job_url,data=data)
        #response = view(request,pk = job.pk)                    
#        self.client.force_login(self.test_user)
#        response = self.client.patch(job_url, data,format='json', follow=True)
        expected = Job.Status.STARTED.value
        returned = job.status 
        self.assertEqual(expected, returned)

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

  
