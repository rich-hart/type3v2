import uuid
from django.db import models

from tagging.registry import register

#NOTE: THIS CLASS DOUBLES AS A HASHTAG DATA STORE
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

 
    @property
    def name(self):
        return str(self.data)

register(Label)

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.UUIDField(
        primary_key = False, 
        default = uuid.uuid4, 
        editable = False,
    )

    #FIXME:  Auto run register_tags for global modules on startup
    @classmethod
    def register_tags(cls):
        register(cls)

    def add_label(self, label):
        self.tags.append(label.id)


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


