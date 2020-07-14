import os
import yaml



current_file_dir = os.path.dirname(os.path.abspath(__file__))
private_yml = os.path.join(current_file_dir, 'private.yml')

if os.path.exists(private_yml):
    with open(private_yml) as fp:
        private_settings = yaml.load(fp,Loader=yaml.BaseLoader)
    for key, value in private_settings.items():
        exec(f"{key} = '{value}'")
else:
    from .private import *
#https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

AWS_STORAGE_BUCKET_NAME = 'test-vvhgiscyyf'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#AWS_ACCESS_KEY_ID = os.environ.get('THECINEMASOURCE_AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = os.environ.get('THECINEMASOURCE_AWS_SECRET_ACCESS_KEY')
#AWS_STORAGE_BUCKET_NAME = os.environ.get('THECINEMASOURCE_AWS_STORAGE_BUCKET_NAME')

AWS_REGION = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'project.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
