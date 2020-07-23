import random
import string
from unittest.mock import patch 
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from .models import *
from .serializers import *
from .views import *
SEED = 42

TEST_BUCKET_NAME = 'test-rsftzmqvua'
TEST_FILE_NAME = 'test.pdf'

random.seed(SEED)

class TestLiveBucket(StaticLiveServerTestCase):
    #fixtures = ['user-data.json']
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver('data/drivers/macos/chromedriver')
        cls.selenium.implicitly_wait(10)

    def setUp(self):
        User.objects.all().delete()
        self.test_user = User.objects.create(username='test')


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test(self):
        pass

#    @patch('project.storage_backends.MediaStorage.custom_domain', new_callable = PropertyMock)
#    @patch('django.contrib.auth.models.AnonymousUser')
#    @patch('jobs.views.JobViewSet.STAGING_SIZE',new_callable = PropertyMock,return_value = 1)
#    def test_perform(self, MockSize, MockAnonymousUser,MockDomain):
#    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.staticfiles_storage')

#    @override_settings(ROOT_URLCONF='project.tests')
#    @override_settings(AWS_DEFAULT_ACL='public-read')
#    @patch('buckets.views.BucketViewSet.list')
    def test_pdf_list(self):
#        import ipdb; ipdb.set_trace()
#        import ipdb; ipdb.set_trace()
#        MockDomain.return_value = self.live_server_url.replace('http://','')
#        urlpatterns = [
#            static(TEST_MEDIA_URL, TEST_MEDIA_ROOT),
#        ] + project.urls.urlpatterns
#        test_file_path = os.path.join(TEST_DATA_DIR,TEST_FILE_NAME)
#        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
#        job = Classification.objects.create(owner=self.test_user.profile,bucket=bucket)
        #file = File.objects.create(name=TEST_FILE_NAME)
        #file.copy()
        bucket = Bucket.objects.create(name='test-vvhgiscyyf')
        #job = Classification.objects.create(owner=self.test_user.profile,bucket=bucket)
        file = File.objects.create(name='multi_page.pdf', parent=bucket)
        file.copy()
        file.s3_client.put_object_acl(
            ACL='public-read',
#            Bucket=file.root.name,
            Bucket=file._instance.storage.bucket.name,
            #Key=file._instance.name,
            Key=os.path.join(file._instance.storage.location,file._instance.name),
        )
#        file._instance.save(TEST_FILE_NAME, io.BytesIO())
        uri = reverse('file-list') + '?' + 'format=pdf' 
        #patcher = patch('buckets.views.BucketViewSet.list')
        #self.addCleanup(patcher.stop)
        #MockView = patcher.start()
#        [ job.queue.put(file.tag.hex) for _ in range(3) ] 
        #FIXME TODO SHOULD NOT NEED MULTIPLE CALLS
        #patcher = patch('django.contrib.auth.models.AnonymousUser', spec=True)
        #AnonymousUser = patcher.start()
#        MockAnonymousUser.return_value = self.test_user
#        stage_size_patch = patch(
#            'jobs.views.JobViewSet.STAGING_SIZE', 
#             new_callable = PropertyMock,
#        )
#        mockSize = stage_size_patch.start()
#        mockSize.return_value = 1
        test_endpoint = '%s%s' % (self.live_server_url, uri)
        #media_url = self.live_server_url + '/media/test.pdf'
        #media_url = file._instance.url
#        self.client.force_login(self.test_user)
#        file._instance.name = 'test.pdf'
        #factory = APIRequestFactory()
        #request = factory.get(uri)
        #serializer = FileSerializer(file,context={'request': request})
#        serializer.is_valid()
	#view = FileViewSet.as_view({'get','render'})
        
        #MockView.return_value = Response(serializer.data)
        self.selenium.get(test_endpoint)

        import ipdb; ipdb.set_trace()
#        stage_size_patch.stop()
        #patcher.stop()
        pass


class TestModels(TestCase): 
    def test_relations(self):
        bucket = Bucket.objects.create()
        folder = Folder.objects.create(parent=bucket)
        file = File.objects.create(parent=folder)
        self.assertEqual(file.root,bucket)

    def test_load(self):
        bucket = Bucket.objects.create(name=TEST_BUCKET_NAME)
        file = File.objects.create(parent=bucket,name=TEST_FILE_NAME)
        file.load()
        self.assertIsNotNone(file.raw)
