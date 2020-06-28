from enum import Enum
import io
import numpy as np
import pickle
import boto3
from pymemcache.client.base import Client
from django.conf import settings
from django.db import models
from bases.models import Object, Choice
from typing import List
from project.storage_backends import StaticStorage
from pdf2image import convert_from_path, convert_from_bytes
import PIL
#https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/types.html
#https://www.slsmk.com/use-boto3-to-open-an-aws-s3-file-directly/

#class Object(Base):
    # path
    # name
    #path = FileField
#    parent = models.ForeignKey(Base, on_delete=models.CASCADE)


#    class Meta:
#        abstract = True



class FSObject(Object):
    parent = models.ForeignKey('buckets.FSObject', on_delete=models.CASCADE, null=True, related_name='+')
    _s3_client = None
    _cache_client = None

    @property
    def key(self):
        return self.name

    def cache(self):
        raise NotImplementedError


    @staticmethod
    def _root(object):
        parent = getattr(object,'parent',None)
        if parent:
            return object._root(parent)
        else:
            return object

    @property
    def root(self):
        return self._root(self)



    @property
    def s3_client(self):
        if not self._s3_client:
            self._s3_client = boto3.client(
                's3',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        return self._s3_client
    @property
    def cache_client(self):
        if not self._cache_client:
            self._cache_client = Client((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
        return self._cache_client


class Bucket(FSObject):
    def list_objects(self) -> List[str]:
        objects = self.s3_client.list_objects(Bucket=self.name)
        keys = [ o['Key'] for o in objects['Contents'] ]
        return keys

class Folder(FSObject):
     pass
#    parent = models.ForeignKey(FSObject, on_delete=models.CASCADE,null=True,related_name='+')

#    @property
#    def bucket(self):
#        return self.parent
# TODO: FIXME!!! 
# Use binary stream of from boto3 to pull in data to general file
# data from aws
# FIXME: DO NOT WRITE TO HOST FS!!!!
class File(FSObject):
    class Format(Choice):
        undefined = None
        pdf = 'pdf'
        @classmethod
        def get_default(cls):
            return cls.undefined.value
    format = None
    _raw = None
    _array = None
    _pil = None
    format = models.CharField(
        max_length=3,
        null = True,
        #choices=Status, #TODO fix this, make PR to django official cite
        choices=Format.get_choices(),
        default=Format.get_default(),
    )
    _path = models.FileField(storage=StaticStorage())
#    parent = models.ForeignKey(Folder, on_delete=models.CASCADE,null=True)
#    parent = models.ForeignKey(FSObject, on_delete=models.CASCADE,null=True)

#    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

       
    @property
    def raw(self):
        return self._raw

    @property
    def array(self, type):
        return self._array

    def cache(self):
        output = io.BytesIO() 
        self._pil.save(output, format = self.format)
        output.flush()
        output.seek(0)
        self._raw = output.read()
        self.cache_client.set(self.tag.hex, self._raw)

    def convert(self):
        if self.format == File.Format.pdf.value:
            return convert_from_bytes(self._raw)
        else:
            raise NotImplementedError

    def load(self):
        self._raw = self.cache_client.get(self.tag.hex)
        if self._raw:
            input = io.BytesIO(self._raw)
            self._pil = PIL.Image.open(input)
            return
        elif isinstance(self.root, Bucket): 
            fileobj = self.s3_client.get_object(
                Bucket=self.root.name,
                Key=self.name,
            )
            self._raw = fileobj['Body'].read()
        else:
            raise NotImplementedError  
            #self._array = None
     


class Text(File): #TEXT
    # image = 1-1 Image

    pass

#import boto3
# 
#s3client = boto3.client(
#    's3',
#    region_name='us-east-1'
#)
# 
## These define the bucket and object to read
#bucketname = mybucket 
#file_to_read = /dir1/filename 
#
##Create a file object using the bucket and object key. 
#fileobj = s3client.get_object(
#    Bucket=bucketname,
#    Key=file_to_read
#    ) 
## open the file object and read it into the variable filedata. 
#filedata = fileobj['Body'].read()
#
## file data will be a binary stream.  We have to decode it 
#contents = filedata.decode('utf-8')) 
#
## Once decoded, you can treat the file as plain text if appropriate 
#print(contents)


#class Image(File):
#    @property
#    def raw(self):
#        return self._raw
#    def __call__(self):
#        pass
class Image(File):
    class Format(Choice):
        undefined = None
        png = 'png'
        def get_default(self):
            return self.png.value

    @property
    def pil(self):
        return self._pil

#    def save(self):
#        raise NotImplementedError('CHECK ME')
    #FIXME: TODO Does it make sense to put cache here?  or in worker?
#        self.cache()
#        super(self,Image).save()

class Audio(File):
    # format = choices: MP3
    pass


class Video(File):
    # format = choices: MP4
    pass

