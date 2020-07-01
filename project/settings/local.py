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

