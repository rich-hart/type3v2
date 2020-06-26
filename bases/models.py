import uuid
from django.db import models
from tagging.models import Tag
from tagging.registry import register

from enum import Enum
import base64
#binascii.b2a_hex
#base64.b64encode

class Choice(Enum):
     @classmethod
     def get_choices(cls):
         return [ (name,value) for (name,value) in enumerate(cls) ]

#NOTE: THIS CLASS DOUBLES AS A HASHTAG DATA STORE
#FIXME: TODO Refactor Label --> Map / MemoryCell for extra tagging data 
# TODO: Choose Encoding
# TODO: need clean up function for Label / Map / MemoryCell / hash namepaces 
class Label(models.Model):
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False,
    )
    #FIXME: TODO # MAKE _data HEX BINARY for better querying
    data = models.CharField(max_length=32)

    #FIXME: TODO 
    # def __str__ --> self.data
    # def name --> def __str__           

    @staticmethod
    def encode_string(string):
        encoding = base64.b64encode(string.encode('utf-8'))
        return encoding
 
    @property
    def name(self):
        return str(self.data)

#register(Label)
#TODO: move to utils
def get_namespace(name):
    namespace = uuid.uuid3(uuid.NAMESPACE_DNS, name)
    return namespace

class Base(models.Model):
    OBJECT_NAMESPACE = get_namespace('OBJECT_NAME')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.UUIDField(
        primary_key = False,
        unique = True,  
        default = uuid.uuid4, 
        editable = False,
    )

    #FIXME:  Auto run register_tags for global modules on startup
    @classmethod
    def register_tags(cls):
        register(cls)

    def add_label(self, label):
        self.tags.append(label.id)

    @property
    def classname(self):
        return self.__class__.__name__

    def tag_object(self, object):
        object_label_hex = uuid.uuid3(self.OBJECT_NAMESPACE, self.tag.hex)
        object_label = object.classname
        Tag.objects.add_tag(object, self.tag.hex)
        data = Label.encode_string(object_label)
        Label.objects.update_or_create(id=object_label_hex, data=data)
#?????
#    def add_tag(self, instance):
#        self.tags.append(instance.tag) OR instance.tags.append(self.tag)
#?????


    def create_tag(self, name, description=None):
        label = Label.objects.create(name=name,description=description)
        self.add_label(label)
        return label.id

    class Meta:
        abstract = True


