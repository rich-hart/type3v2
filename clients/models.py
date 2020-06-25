from django.db import models

# Create your models here.
class Client(models.Models):
    name = models.CharField(max_length=127)
    # NOTE: add name to user group on instance init
