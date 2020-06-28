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

DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'

AWS_STORAGE_BUCKET_NAME = 'project_development'

AWS_REGION = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = 's3.%s.amazonaws.com/%s' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'thecinemasource.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'thecinemasource.storage_backends.MediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)



from .local import *
