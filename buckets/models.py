import boto3
from django.db import models
from bases.models import Base, Object

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
#    name = models.CharField(max_length=2**6)
    class Meta:
        abstract = True

class Bucket(FSObject):
    pass

class Folder(FSObject):
    parent = models.ForeignKey(Bucket, on_delete=models.CASCADE,null=True)

    @property
    def bucket(self):
        return self.parent
# TODO: FIXME!!! 
# Use binary stream of from boto3 to pull in data to general file
# data from aws
# FIXME: DO NOT WRITE TO HOST FS!!!!
class File(FSObject):
    format = None
    _raw = None
    _array = None
    _client = None
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE,null=True)

#    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    @property
    def client(self):
        if type=='s3' and not self._client:
            self._client = boto3.client(
                's3',
                region_name='us-east-1'
            )
        return self._client
       
    @property
    def raw(self, type):
        return self._raw

    @property
    def array(self, type):
        return self._array

    def load(self, type):
        fileobj = s3client.get_object(
            Bucket=self.folder.bucket.name,
            Key=self.file,
        )
        self._raw = fileobj['Body'].read() 
        self._array = None
     


class Page(Base): #TEXT
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

