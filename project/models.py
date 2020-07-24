from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings
from tagging.registry import register
from enum import IntEnum, Enum
from django.db.models import signals
import boto3
from pymongo import MongoClient
from pymemcache.client.base import Client as CacheClient
import uuid 

def get_namespace(name):
    namespace = uuid.uuid3(uuid.NAMESPACE_DNS, name)
    return namespace

class Choice(Enum): #NOTE: Link with Object class choice
     @classmethod
     def get_choices(cls):
         return [ (name,value) for (name,value) in enumerate(cls) ]


class Client:
    name = None
    _connection = None
    _cursor = None
    _instance = None
    _db = None
    _collection = None


    def __call__(self):
        """
        Change project client to service client
        with function call e.g. project_client = Client()
        service_client = project_client()
        """
        return self.instance

 #    @property
#    def cache_client(self):
#        if not self._cache_client:
#            self._cache_client = Client((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
#        return self._cache_client

class S3(Client):
    name = 's3'
    region_name=settings.AWS_REGION
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    
    @property
    def instance(self):
        if not self._instance:
            self._instance = boto3.client(
                self.name,
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
        return self._instance
#    @property
#    def s3_client(self):
#        if not self._s3_client:
#            self._s3_client = boto3.client(
#                's3',
#                region_name=settings.AWS_REGION,
#                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#            )
#        return self._s3_client


#    @property
#    def s3_client(self):
#        if not self._s3_client:
#            self._s3_client = boto3.client(
#                's3',
#                region_name=settings.AWS_REGION,
#                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#            )
#        return self._s3_client


class Cache(Client):
    name = 'cache'
    host = settings.MEMCACHED_HOST
    port = settings.MEMCACHED_PORT

    @property
    def instance(self):
        if not self._instance:
            self._instance = CacheClient((self.host,self.port))
        return self._instance



class Mongo(Client):
    name = 'mongo'
    MONGO_URI = f'mongodb://' \
                f'{settings.MONGO_USERNAME}:' \
                f'{settings.MONGO_PASSWORD}@' \
                f'{settings.MONGO_HOST}:' \
                f'{settings.MONGO_PORT}'
#    _db = None
#    _collection = None

    def __init__(self):
        self._instance = MongoClient(self.MONGO_URI)
        self._db = self._instance[settings.MONGO_DATABASE]

    @property
    def instance(self):
        if not self._instance:
            self._instance = MongoClient(self.MONGO_URI)
        return self._instance

    @property
    def db(self):
        if not self._db:
            self._db = self.instance[settings.MONGO_DATABASE]
        return self._db

#    def get_collection(name)

#        self._collection=self.db[collection]
#     @property
#    def mongo_db(self):
#        if not self._mongo_db:
#            self._mongo_db = self.mongo_client[settings.MONGO_DATABASE]
#        return self._mongo_db

#    @property
#    def collection(self):
#        if not self._collection:
#            self._collection=self.mongo_db[self.class_name]
#        return self._collection

#    @property
#    def mongo_client(self):
#        if not self._mongo_client:
#            self._mongo_client = MongoClient(
#                settings.MONGO_HOST,
#                settings.MONGO_PORT,
#                username=settings.MONGO_USERNAME,
#                password=settings.MONGO_PASSWORD,
#                authSource="admin",
#            )
#            self._mongo_client = MongoClient(f"mongodb://{settings.MONGO_USERNAME}:"\
#                "{settings.MONGO_PASSWORD}@"\
#                "{settings.MONGO_HOST}/{MONGO_DATABASE}")
#            self._mongo_client = MongoClient(self.MONGO_URI)
#        return self._mongo_client

#    @property
#    def s3_client(self):
#        if not self._s3_client:
#            self._s3_client = boto3.client(
#                's3',
#                region_name=settings.AWS_REGION,
#                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#            )
#        return self._s3_client
       
#mongo_client = Mongo()

class Base(models.Model):
    class Namespace(IntEnum):
        root = get_namespace('ROOT_NAMESPACE')
 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    _clients = set([
        Mongo(),
        Cache(),
        S3(),
    ])

    @property
    def clients(self):
        return { c.name: c for c in self._clients }

    tag = models.UUIDField(
        primary_key = False,
        unique = True,  
        default = uuid.uuid4, 
        editable = False,
    )

    @property
    def seed(self):
        return self.tag.hex

    #FIXME: TODO: Clean up namespaces
    #FIXME:  Auto run register_tags for global modules on startup
    @classmethod
    def register_tags(cls):
        register(cls)

    @property 
    def module_path(self):
        return self.__module__

    @property 
    def app_name(self):
        return self.__module__.split('.')[0]

    @property
    def class_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True




# Concreat base class / Link class to memory (Depecated Label)? 
class Object(Base):  #NOTE: Replace Base with Object?  Allow either / or?
    name = models.CharField(max_length=2**6)
#    class Meta:
#        abstract = True
class Tag(Base):
    id = models.UUIDField(
        primary_key = True,
        unique = True,
        editable = False,
    )
    _data = JSONField(default=dict)
    
    @property 
    def data(self):
        #FIXME: Overwrite with mongo
        return self._data

Object.register_tags()

def save_to_mongo(sender, instance, *args, **kwargs):
    client = sender.clients['mongo']() 
    collection = client.db[instance.class_name]
    instance._data['_id'] = instance.tag.hex
    collection.insert_one(instance._data)
    instance._data = {}
    instance.save()

signals.pre_save.connect(receiver=save_to_mongo, sender=Tag)

