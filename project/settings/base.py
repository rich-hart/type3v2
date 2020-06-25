from .core import *

INSTALLED_APPS += depends.build('users','buckets')

INSTALLED_APPS = list(set(INSTALLED_APPS))
