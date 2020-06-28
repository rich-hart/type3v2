from bases.models import Base

#https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/types.html
#https://www.slsmk.com/use-boto3-to-open-an-aws-s3-file-directly/

class FSObject(Base):
    # path
    # name
    pass


class Bucket(FSObject):
    pass

class Folder(FSObject):
    pass
# TODO: FIXME!!! 
# Use binary stream of from boto3 to pull in data to general file
# data from aws
# FIXME: DO NOT WRITE TO HOST FS!!!!
class File(FSObject):
    format = None
    pass

class Page(Base):
    # image = 1-1 Image

    pass

class Image(File):
    # format = choices: PNG
    pass

class Audio(File):
    # format = choices: MP3
    pass


class Video(File):
    # format = choices: MP4
    pass

