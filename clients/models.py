from django.db import models
from project.models import Base


# Create your models here.
# NOTE: TEST THIS WITH QA CREDENTIALS AND CONSERNS
# TODO: fixture: Type3, GIS, Capco, WF
class Client(Base):
    name = models.CharField(max_length=127, unique=True)
    # NOTE: add name to user group on instance init


Client.register_tags()
