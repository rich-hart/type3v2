import boto3
from django.conf import settings
from django.db import models
from bases.models import Object

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
    parent = models.ForeignKey('buckets.FSObject', on_delete=models.CASCADE, related_name='+')

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
        

class Bucket(FSObject):
    pass

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
    format = None
    _raw = None
    _array = None
    _client = None
#    parent = models.ForeignKey(Folder, on_delete=models.CASCADE,null=True)
#    parent = models.ForeignKey(FSObject, on_delete=models.CASCADE,null=True)

#    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    @property
    def client(self):
        if not self._client:
            self._client = boto3.client(
                's3',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        return self._client
       
    @property
    def raw(self):
        return self._raw

    @property
    def array(self, type):
        return self._array

    def load(self):
        if isinstance(self.root, Bucket): 
            fileobj = self.client.get_object(
                Bucket=self.root.name,
                Key=self.name,
            )
            self._raw = fileobj['Body'].read() 
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
    pass 

class Audio(File):
    # format = choices: MP3
    pass


class Video(File):
    # format = choices: MP4
    pass

