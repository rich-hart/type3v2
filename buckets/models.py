import os
from enum import Enum
import io
import numpy as np
import pandas as pd
import pickle
import boto3
#from pymongo import MongoClient

from pymemcache.client.base import Client
from django.conf import settings
from django.db import models
from project.models import Object, Choice
from typing import List
from project.storage_backends import StaticStorage, MediaStorage
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
    MONGO_URI = f'mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}' #TODO: FIXME: Move to settings
    _s3_client = None
    _cache_client = None
    _mongo_client = None
    _mongo_db = None
    _collection = None




    parent = models.ForeignKey('buckets.FSObject', on_delete=models.CASCADE, null=True, related_name='+')
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

#    @property
#    def mongo_db(self):
#        if not self._mongo_db:
#            self._mongo_db = self.mongo_client[settings.MONGO_DATABASE]
#        return self._mongo_db
#
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
#    @property
#    def cache_client(self):
#        if not self._cache_client:
#            self._cache_client = Client((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
#        return self._cache_client



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

    _raw = None
    format = models.CharField(
        max_length=3,
        null = True,
        #choices=Status, #TODO fix this, make PR to django official cite
        choices=Format.get_choices(),
        default=Format.get_default(),
    )
    _path = models.FileField(storage=StaticStorage()) #FIXME: DEPRICATE
    _instance = models.FileField(storage=MediaStorage(),null=True)

#    @property
#    def instance(self):
#        return self._instance
#    parent = models.ForeignKey(Folder, on_delete=models.CASCADE,null=True)
#    parent = models.ForeignKey(FSObject, on_delete=models.CASCADE,null=True)

#    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def copy(self,lazy=True):
        #TODO!!!!: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy_object
        if isinstance(self.root, Bucket):
             if isinstance(self.parent, Folder):
                 path = os.path.join(self.parent.name, self.name)
             else:
                 path = self.name
             #https://stackoverflow.com/questions/5315603/how-do-i-get-the-file-key-size-in-boto-s3
             src_bucket = self.root.name
             src_key = path
             dest_bucket = self._instance.storage.bucket.name

             copy_source = {
                 'Bucket': src_bucket,
                 'Key': src_key,
             }            



            

             if self._instance.name:
                 dest_key = os.path.join(self._instance.storage.location, self._instance.name)
                 if lazy:
                     copy_dest = {
                         'Bucket': dest_bucket,
                         'Key': dest_key,
                     }
                     dest_head_object=self.clients['s3']().head_object(**copy_dest)
                     dest_size = dest_head_object.get('ContentLength',0)
                     src_head_object=self.clients['s3']().head_object(**copy_source)
                     src_size = src_head_object.get('ContentLength',0)
                     if src_size == dest_size:
                         return
             else:    
                 self._instance.save(self.name, io.BytesIO()) #TouchFile to load urls
                 dest_key = os.path.join(self._instance.storage.location, self._instance.name)
               


             self.clients['s3']().copy(copy_source, dest_bucket, dest_key)      
#            path = os.path.join(folder_key, file_key)
#            copy_source = {
#                'Bucket': self.name,
#                'Key': path
#            }
#            pdf._instance.save(pdf_key, io.BytesIO()) #TouchFile to load urls
#            pdf._instance.close()
#            dest_bucket = pdf._instance.storage.bucket.name
#            dest_key = os.path.join(pdf._instance.storage.location, pdf._instance.name)
#            self.s3_client.copy(copy_source, dest_bucket, dest_key)

       
    @property
    def raw(self):
        return self._raw

    def cache(self):
        output = io.BytesIO() 
        self._pil.save(output, format = self.format)
        output.flush()
        output.seek(0)
        self._raw = output.read()
        self.clients['cache']().set(self.tag.hex, self._raw)


    def load(self):
        self._raw = self.clients['cache']().get(self.tag.hex)
        if self._raw:
            return
        elif isinstance(self.root, Bucket): 
            fileobj = self.clients['s3']().get_object(
                Bucket=self.root.name,
                Key=self.name,
            )
            self._raw = fileobj['Body'].read()
        else:
            raise NotImplementedError  
            #self._array = None

#class PDF(File):

#    def cache(self):
#        output = io.BytesIO() 
#        self._pil.save(output, format = self.format)
#        output.flush()
#        output.seek(0)
#        self._raw = output.read()
#        self.cache_client.set(self.tag.hex, self._raw)

#    def convert(self):
#        if self.format == File.Format.pdf.value:
#            return convert_from_bytes(self._raw)
#        else:
#            raise NotImplementedError
#
#    def load(self):
#        self._raw = self.cache_client.get(self.tag.hex)
#        if self._raw:
#            input = io.BytesIO(self._raw)
#            self._pil = PIL.Image.open(input)
#            return
#        elif isinstance(self.root, Bucket): 
#            fileobj = self.s3_client.get_object(
#                Bucket=self.root.name,
#                Key=self.name,
#            )
#            self._raw = fileobj['Body'].read()
#        else:
#            raise NotImplementedError  
#            #self._array = None


def get_ext(path):
    tokens = os.path.basename(path).split(os.extsep)
    if len(tokens) ==2:
        return tokens[1]

def get_prefix(path):
    tokens = os.path.basename(path).split(os.extsep)
    return tokens[0]

from django.core.files.storage import default_storage
 
class Bucket(FSObject):
    def list_objects(self) -> List[str]:
        objects = self.s3_client.list_objects(Bucket=self.name)
        keys = [ o['Key'] for o in objects['Contents'] ]
        return keys

    def mirror(self, format = None):
        keys = self.list_objects()
        format = format.lower()
        if format:
            folder_keys = [os.path.dirname(p) for p in keys if get_ext(p)==format]     
            file_keys = [os.path.basename(p) for p in keys if get_ext(p)==format]     
        files = []
        for folder_key, file_key in zip(folder_keys, file_keys):
            if folder_key:
                parent,_ = Folder.objects.get_or_create(name=folder_key,parent=self)
            else:
                parent = self #FIXME: NEED TO LINK TO BUCKET
            file, _ = File.objects.get_or_create(name=file_key, parent=parent, format=format)
#            path = os.path.join(folder_key, file_key)
#            copy_source = {
#                'Bucket': self.name,
#                'Key': path
#            }
#            pdf._instance.save(pdf_key, io.BytesIO()) #TouchFile to load urls
#            pdf._instance.close()
#            dest_bucket = pdf._instance.storage.bucket.name
#            dest_key = os.path.join(pdf._instance.storage.location, pdf._instance.name)
#            self.s3_client.copy(copy_source, dest_bucket, dest_key)
            files.append(file)
        return files



    def mirror_pdfs(self):
        keys = self.list_objects()
        folder_keys = [os.path.dirname(p) for p in keys if get_ext(p)=='pdf']     
        pdf_keys = [os.path.basename(p) for p in keys if get_ext(p)=='pdf']     
        pdfs = []
        for folder_key, pdf_key in zip(folder_keys, pdf_keys):
            if folder_key:
                parent = Folder.objects.create(name=folder_key,parent=self)
            else:
                parent = self #FIXME: NEED TO LINK TO BUCKET
            pdf = PDF.objects.create(name=pdf_key,parent=parent)
            path = os.path.join(folder_key,pdf_key)
            copy_source = {
                'Bucket': self.name,
                'Key': path
            }
            pdf._instance.save(pdf_key,io.BytesIO()) #TouchFile to load urls
            pdf._instance.close()
            dest_bucket = pdf._instance.storage.bucket.name
            dest_key = os.path.join(pdf._instance.storage.location, pdf._instance.name)
            self.s3_client.copy(copy_source, dest_bucket, dest_key)
            pdfs.append(pdf)
        return pdfs


class Text(File): #TEXT
    class Format(Choice):
        undefined = None
        tsv = 'tsv' # ('tsv', 'default') 
        @classmethod
        def get_default(cls):
            return cls.undefined.tsv.value
    _frame = None
    # image = 1-1 Image
    def cache(self):
        self.cache_client.set(self.tag.hex, self._raw)

    @property
    def frame(self):
        if not self._frame and self.format==self.Format.tsv.value:
            self._frame = self.get_frame()
        return self._frame

    def get_frame(self):
        return pd.read_csv(io.StringIO(self._raw.decode()),sep='\t',dtype={'text':str})

    def load(self):
        data = self.cache_client.get(self.tag.hex)
        if not data: 
            fileobj = self.s3_client.get_object(
                Bucket=self.root.name,
                Key=self.name,
            )
            data = fileobj['Body'].read()
        self._raw = data
         

            #self._array = None
     

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
    _pil = None
    _array = None
    class Format(Choice):
        undefined = None
        png = 'png'
        def get_default(self):
            return self.png.value

    def cache(self):
        output = io.BytesIO() 
        self._pil.save(output, format = self.format)
        output.flush()
        output.seek(0)
        self._raw = output.read()
        self.cache_client.set(self.tag.hex, self._raw)


    @property
    def pil(self):
        return self._pil

    @property
    def array(self, type):
        return self._array

    def load(self):
        self._raw = self.cache_client.get(self.tag.hex)
        if self._raw:
            return
        elif isinstance(self.root, Bucket): 
            fileobj = self.s3_client.get_object(
                Bucket=self.root.name,
                Key=self.name,
            )
            self._raw = fileobj['Body'].read()
            input = io.BytesIO(self._raw)
            self._pil = PIL.Image.open(input)
        else:
            raise NotImplementedError  
            #self._array = None


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

