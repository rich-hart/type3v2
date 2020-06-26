from .core import *

INSTALLED_APPS += depends.build(
    'users',
    'buckets',
    'classifiers',
    'tools',
    'jobs',
)

INSTALLED_APPS = list(set(INSTALLED_APPS))
