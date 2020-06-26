import unittest
from django.test import TestCase

from .demo import *
#NOTE TEST INSTANCE
class TestDemo(TestCase):
    @unittest.skip("NotImplemented")
    def test_job_owner_human(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_owner_random_bot(self):
        self.fail("NotImplementedError")

    @unittest.skip("NotImplemented")
    def test_job_owner_smart_bot(self):
        self.fail("NotImplementedError")

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

  
