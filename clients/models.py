from django.db import models



# Create your models here.
# NOTE: TEST THIS WITH QA CREDENTIALS AND CONSERNS
# TODO: fixture: Type3, GIS, Capco, WF
class Client(models.Models):
    name = models.CharField(max_length=127)
    # NOTE: add name to user group on instance init
