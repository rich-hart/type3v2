from rest_framework import serializers

from bases.models import Object, Memory 
from .models import *


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = (
            'id',
#            'url',
        )


class BinaryClassifierSerializer(serializers.ModelSerializer):
#     object = ObjectSerializer(read_only=True)
#     label = serializers.CharField(read_only=True)
#     value = serializers.MultipleChoiceField(['True','False','Unknown'])
     object_set = ObjectSerializer(read_only=True,many=True)
     class Meta:
        model = Classifier
        fields = (
            'id',
            'object_set', # Base Model Serializer 
#            'label',
#            'value',
        )

#     def to_representation(self, instance):
#        """Convert `username` to lowercase."""
#         import ipdb; ipdb.set_trace()
#         instance.human.object_set
         #ret = super().to_representation(instance)
#        ret['username'] = ret['username'].lower()
#         ret = super(BinaryClassifierSerializer,self).to_representation(instance)         
#         return ret
     
#     def to_internal_value(self, data):
#         import ipdb; ipdb.set_trace()
#         return data
 
