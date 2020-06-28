from rest_framework import serializers

from .models import *


#class ObjectSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Object
#        fields = (
#            'id',
#            'url',
#        )
#
#
#class BinaryClassifierSerializer(serializers.ModelSerializer):
#     object = ObjectSerializer()
#     label = serializers.CharField(max_length=32, allow_blank=False, trim_whitespace=True)
#     value = serializers.NullBooleanField()
#     class Meta:
#        model = Classifier
#        fields = (
#            'id',
#            'object', # Base Model Serializer 
#            'label',
#            'value',
#        )
#   
