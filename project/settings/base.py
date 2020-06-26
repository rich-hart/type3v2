from .core import *

INSTALLED_APPS += depends.build(
    'users',
    'buckets',
    'classifiers',
    'tools',
    'jobs',
)

INSTALLED_APPS = list(set(INSTALLED_APPS))

STATIC_URL = '/static/'
STATIC_ROOT =  os.path.join(BASE_DIR, 'static') 
