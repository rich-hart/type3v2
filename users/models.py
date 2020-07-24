from django.db import models
from django.db.models import signals


from django.contrib.auth.models import User

from project.models import Base



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


def update_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


signals.post_save.connect(receiver=update_or_create_profile, sender=User)

Account.register_tags()
Profile.register_tags()
