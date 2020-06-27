from django.db import models


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

#FIXME:  Auto run register_tags for global modules on startup

Profile.register_tags()
