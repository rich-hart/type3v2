from bases.models import Base

class FSObject(Base):
    # path
    # name
    pass

class Bucket(FSObject):
    pass

class Folder(FSObject):
    pass

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

