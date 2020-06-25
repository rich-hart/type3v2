from django.db import models

from tagging.registry import register

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#FIXME: register tags
#register(Base)
