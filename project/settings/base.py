from .core import *

INSTALLED_APPS += depends.build(
    'users',
    'buckets',
    'classifiers',
    'tools',
    'jobs',
    'procedures',
    'clients',
)

INSTALLED_APPS = list(set(INSTALLED_APPS))

STATIC_URL = '/static/'
STATIC_ROOT =  os.path.join(BASE_DIR, 'static') 

DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'

AWS_STORAGE_BUCKET_NAME = 'project-dev-claxotionf'

AWS_REGION = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = 's3.%s.amazonaws.com/%s' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'project.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

MEMCACHED_HOST = '0.0.0.0' #localhost
MEMCACHED_PORT = 11211

MONGO_PORT = 27017
MONGO_HOST = '0.0.0.0' #localhost
MONGO_DATABASE = os.environ.get('MONGO_INITDB_DATABASE','test-project')
MONGO_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME','guest')
MONGO_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD','guest')

NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:test@localhost:7687')
NEOMODEL_ENCRYPTED_CONNECTION = False
NEOMODEL_SIGNALS = True
NEOMODEL_MAX_POOL_SIZE = 50
#NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:neo4j@neo4j:7687')

DEFAULT_MESSAGE_QUEUE='amqp://guest:guest@localhost:5672'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', DEFAULT_MESSAGE_QUEUE)
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND','amqp://guest:guest@localhost:5672//')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "NAME": os.environ.get("SQL_DATABASE","project"),
        "USER": os.environ.get("SQL_USER", "root"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

MESSAGE_QUEUE_HOST = os.environ.get('MESSAGE_QUEUE_HOST',DEFAULT_MESSAGE_QUEUE)


from .local import *
