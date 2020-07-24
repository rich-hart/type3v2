import os
from django.test import TestCase

from project.models import Tag, ProjectTag
from .models import *

TEST_CLIENT_FIXTURE_PATH = os.path.join('data','clients','fixtures','default.yaml')

class TestModels(TestCase):
    fixtures = [TEST_CLIENT_FIXTURE_PATH]

    def test_create_client(self):
        client = BusinessClient.objects.create(name='Test Client')
        data ={'info1': 'asdf', 'info2': 'asdf'}
        Tag.objects.update_tags(client, client.tag.hex)
        project_tag = ProjectTag.objects.create(id=client.tag.hex, _data=data)
        project_tag.clients['mongo'].reload()
        collection = project_tag.clients['mongo']().db[project_tag.class_name] 
        tag_data = [ d for d in collection.find({"_id":project_tag.id}) ]
        self.assertTrue(tag_data)
        self.assertFalse(project_tag._data)
