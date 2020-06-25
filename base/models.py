from django.db import models

from tagging.registry import register

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #FIXME:  Auto run register_tags for global modules on startup
    @classmethod
    def register_tags(cls):
        register(cls)

    class Meta:
        abstract = True

