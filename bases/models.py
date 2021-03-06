import uuid
from django.conf import settings
from django.db import models
from tagging.models import Tag, TaggedItem
from tagging.registry import register
from django.apps import apps
from pymemcache.client.base import Client as MemcacheClient
from enum import Enum
import base64
#binascii.b2a_hex
#base64.b64encode

#FIXME: TODO Maybe merge bases project app? 

class Choice(Enum): #NOTE: Link with Object class choice
     @classmethod
     def get_choices(cls):
         return [ (name,value) for (name,value) in enumerate(cls) ]
#FIXME: TODO merge Label and Base --> Data
#                                   class Base(model.Model): #abstract
#                                       _hash = model.UUIDField(unique=True)
#                                   class Data(model.Model): #GENERAL DATASTORE FOR TAG MAPPINGS
#                                       id -> is 1-1 with Base._hash
#                                       _data = model.CharFiend(max_length=32)
#FIXME: TODO new object declaration class Object(Base): 
#                                       @property
#                                       def namespaces(self):
#                                           pass
#                                       @property
#                                       def tag(self):
#                                           return self._hash
#                                       @property
#                                       def memory(self)->dict: #load properties here:
#                                           [ setattr(self, k, v) for k,v in self._memory.items()]
#FIXME: TODO  Memcache                      return self._memory #(pulled from Namespace Data store)
#NOTE: THIS CLASS DOUBLES AS A HASHTAG DATA STORE
#FIXME: TODO Refactor Label --> Map / MemoryCell for extra tagging data 
# TODO: Choose Encoding
# TODO: need clean up function for Label / Map / MemoryCell / hash namepaces 



class Label(models.Model): #FIXME: TODO --> make this general `abstract` Data class. 
    #FIXME: Label Depecated Switch with memory
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False,
    )
    #FIXME: TODO # MAKE _data 
    #FIXME: TODO HEX BINARY for better querying
#    data = models.CharField(max_length=32)
    _data = models.CharField(max_length=32)
#    data_beta = models.CharField(max_length=32) #FIXME: TODO reconcile 'data' fields 
    #FIXME: TODO 
    # def __str__ --> self.data
    # def name --> def __str__           
    #FIXME: TODO encode_string --> encode


#    @staticmethod
#    def encode_string(string):
#        encoding = base64.b64encode(string.encode('utf-8'))
#        return encoding



    @staticmethod
    def encode_string(string):
        string = string.encode('utf-8')
        string = base64.b64encode(string)
        string = string.decode('utf-8')
        return string

    @staticmethod
    def encode(string):
        string = string.encode('utf-8')
        string = base64.b64encode(string)
        string = string.decode('utf-8')
        return string

    @staticmethod
    def decode(data):
        decoding = base64.b64decode(data).decode('utf-8')
        return decoding

 
    @property
    def name(self):
        return str(self.data)

# LONG TERM GENERAL MEMORY FOR PROJECT OBJECTS
ROOT_NAMESPACE = ''

class Space(Enum):
#    ROOT = 'PROJECT_' #FIXME cant get superclass of root to work

    @property
    def hash(self):
        value = self.value + ROOT_NAMESPACE
        return uuid.uuid3(uuid.NAMESPACE_DNS, value).hex
#    def __init__(self, value):
        #super(self, Space).__init__(value) #FIXME: Wont work???
#        self = Enum(value)
#        value = self.ROOT + namespace.value
#        setattr(namespace, namespace.name, value)
#        uuid = uuid.uuid3(uuid.NAMESPACE_DNS, value)
#        setattr(namespace, 'uuid', uuid.hex)
        #super(cls, TestUtils).setUpClass(*args,**kwargs)
#        for _, namespace in enumerate(self):
#            value = self.ROOT + namespace.value
#            setattr(namespace, namespace.name, value)
#            uuid = uuid.uuid3(uuid.NAMESPACE_DNS, value)
#            setattr(namespace, 'uuid', uuid.hex)
#__global_memcache_client = MemcacheClient((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
class Memory(Label): #FIXME: Make this concreat memory base class
#    _cache = None

    __global_memcache_client = MemcacheClient((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))
    ROOT_NAMESPACE = ROOT_NAMESPACE

    #@classmethod
    #def cache_client(cls):
        #if not cls._cache_client:
        #    cls._cache_client = __global_memcache_client
        #return cls._cache_client

#    @property
#    def cache_client(self):
#        if not self._cache_client:
#            self._cache_client = Client((settings.MEMCACHED_HOST, settings.MEMCACHED_PORT))i
#        return self._cache_client

#    class Namespace(Space):
#        pass
    #NOTE, check class decorators

#    def memory_id(self, space):
#        return uuid.uuid3(space.hash,self.id)

    def retrieve(self, space):
        hash = self.memory_id(space)
        data = Memory.__global_memcache_client.get(hash)
        if not data:
            data = Memory.objects.get(id=hash).data
        return data
    @staticmethod
    def get_address(space, hash):
        return uuid.uuid3(space,hash.hex)

#    @c
#    def cache(self, hash, space, data):
        #hash = address.memory_id(space)
#        address = uuid.uuid3(space,hash.hex)
#        cls.__global_memcache_client.set(address.hex, data)
#        cls.objects.update_or_create(id=address, data=data)
 






#    def save(self):
#        super(self, Space).__init__(value)

#    def store(self, name, data):
#        raise Warning('store in  memcache first')
#        space = self.Namespace(name)
#        Memory.obects.update_or_create(tag = space.hash, data = self.encode(data))


#                setattr(self, namespace.name, namespace.value)

#        def get(self):
#            namespace = uuid.uuid3(uuid.NAMESPACE_DNS,
#        @classmethod
#        def get(cls):
#            namespace = uuid.uuid3(uuid.NAMESPACE_DNS, name)
#            return namespace



        

#register(Label)
#TODO: move to utils
def get_namespace(name):
    namespace = uuid.uuid3(uuid.NAMESPACE_DNS, name)
    return namespace

class Base(models.Model):
    OBJECT_NAMESPACE = get_namespace('OBJECT_NAME')
    APP_NAMESPACE = get_namespace('APP_NAME')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.UUIDField(
        primary_key = False,
        unique = True,  
        default = uuid.uuid4, 
        editable = False,
    )
    namespaces = set()
    # Move to objects
    _object_set = None

    #class Namespace(Enum):
        #FIXME: TODO: Use namespace to load custom properties
        # at runtime
    #    pass
    # namespaces = set()    
    @property
    def seed(self):
        return self.tag.hex

    #FIXME: TODO: Clean up namespaces

    #FIXME:  Auto run register_tags for global modules on startup
    @classmethod
    def register_tags(cls):
        register(cls)

    def add_label(self, label):
        self.tags.append(label.id)

    @property 
    def module_path(self):
        return self.__module__

    @property 
    def app_name(self):
        return self.__module__.split('.')[0]

    @property
    def class_name(self):
        return self.__class__.__name__

    def tag_object(self, object):
        Tag.objects.add_tag(object, self.tag.hex)

        object_label_hex = uuid.uuid3(self.OBJECT_NAMESPACE, self.tag.hex)
        object_label = object.class_name
        data = Label.encode_string(object_label) 
        Label.objects.update_or_create(id=object_label_hex, _data=data)

        app_label_hex = uuid.uuid3(self.APP_NAMESPACE, self.tag.hex)
        app_label = object.app_name
        data = Label.encode_string(app_label)
        Label.objects.update_or_create(id=app_label_hex, _data=data)

#?????
#    def add_tag(self, instance):
#        self.tags.append(instance.tag) OR instance.tags.append(self.tag)
#?????

    @property
    def data(self):
        data = {}
        for _, space in self.namespaces:
                value = self.retrieve(space.hash)
                value = self.decode(value)
                name = space.value.lower()
                data[name] = value
        return data

    def create_tag(self, name, description=None):
        label = Label.objects.create(name=name,description=description)
        self.add_label(label)
        return label.id

    @property
    def object_set(self):
        if self._object_set:
            return self._object_set
        # TODO: use hashing to look up object type. 
        tags = Tag.objects.filter(name=self.tag.hex)
        objects = []
        for tag in tags:
            object_tag = tag
            #FIXME: TODO Move hash memory retieval into Base class
            object_label_hex = uuid.uuid3(self.OBJECT_NAMESPACE, object_tag.name)
            memory_block = Label.objects.get(id=object_label_hex) 
            model_name = Label.decode(memory_block.data)


            app_label_hex = uuid.uuid3(self.APP_NAMESPACE, object_tag.name)
            memory_block = Label.objects.get(id=app_label_hex)
            app_label =  Label.decode(memory_block.data)

            Model = apps.get_model(app_label=app_label, model_name=model_name)

            instances = TaggedItem.objects.get_by_model(Model, object_tag)
            for instance in instances:
                objects.append(instance)

        self._object_set = objects

        return self._object_set


    class Meta:
        abstract = True

# Concreat base class / Link class to memory (Depecated Label)? 
class Object(Base):  #NOTE: Replace Base with Object?  Allow either / or?
    name = models.CharField(max_length=2**6)
#    class Meta:
#        abstract = True

class Algorithm(Base):
    input = None
    output = None
    # def init
    # def mantain
    # def terminate

    class Meta:
        abstract = True

register(Object)
