from django.test import TestCase

from project.models import Tag, ProjectTag
from .models import *

class TestModels(TestCase):
#    def setUp(self):
#        self.user = .objects.create(username='test')
       
#    def test_profile(self):
#        profile = Profile.objects.create(user=self.user)
    def test_create_client(self):
        client = Client.objects.create(name='Test Client')
        data ={'info1': 'asdf', 'info2': 'asdf'}
        Tag.objects.update_tags(client, client.tag.hex)
        project_tag = ProjectTag.objects.create(id=client.tag.hex, _data=data)
        project_tag.clients['mongo'].reload()
        collection = project_tag.clients['mongo']().db[project_tag.class_name] 
        tag_data = [ d for d in collection.find({"_id":project_tag.id}) ]
        self.assertTrue(tag_data)
        self.assertFalse(project_tag._data)
