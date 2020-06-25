from .core import *

INSTALLED_APPS += depends.build('users')

INSTALLED_APPS = list(set(INSTALLED_APPS))
