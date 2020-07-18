from django.db import models
from django.db.models import signals


from django.contrib.auth.models import User

from bases.models import Base



class Profile(Base):
    """
    A project specific class for user info.
    """
    # NOTE Try not to overwrite User class. 
    # Use Profile instead

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

# NOTE: 3rd party info
class Account(Base):
    """
    A class for 3rd party info
    """
    #FIXME: TODO make one to many
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )


def update_or_create(sender, instance, created, **kwargs):
    if not getattr(instance,'profile',None):
        Profile.objects.update_or_create(user=instance)

signals.post_save.connect(receiver=update_or_create, sender=User)
#FIXME:  Auto run register_tags for global modules on startup

Profile.register_tags()
