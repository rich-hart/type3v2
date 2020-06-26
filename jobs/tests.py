import unittest
from django.test import TestCase
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
        pass
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

  
