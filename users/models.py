from django.db import models
from django.contrib.auth.models import User

from bases.models import Base

class Profile(Base):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

#FIXME:  Auto run register_tags for global modules on startup

Profile.register_tags()
