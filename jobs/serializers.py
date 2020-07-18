from rest_framework import serializers

from bases.models import Object, Memory 

from buckets.models import Bucket, File, Image 
from users.models import Profile


from .models import *

class ClassificationSerializer(serializers.ModelSerializer):
#    profile_set = ProfileSerializer(many=True, write_only=True)
#    assignee_set = AssigneeSerializer(many=True)
    bucket = serializers.CharField(max_length=127)
    class Meta:
        model = Classification
        fields = (
            'id',
            'bucket',
        )
        write_only_fields = ('bucket',)
        read_only_fields = ('status',)


class JobSerializer(serializers.ModelSerializer):
    classification = ClassificationSerializer()
    class Meta:
        model = Job
        fields = (
            'id',
            'description',
            'status',
            'assignee_set',
            'classification',
            'owner',
        )
        read_only_fields=('status','owner','assignee_set')
        write_only_fields=('users',)
    def create(self, validated_data):
        classification_data = validated_data.pop("classification")
        assignee_set = validated_data.pop('assignee_set')

        classification_serializer = ClassificationSerializer(data=classification_data)
        classification_serializer.is_valid()
        validated_data.update(classification_serializer.data)
        bucket = validated_data.pop('bucket')
        bucket,_ = Bucket.objects.get_or_create(name=bucket)
        validated_data['bucket']=bucket
        instance = Classification.objects.create(**validated_data)
        return instance

class AssigneeSerializer(serializers.ModelSerializer):
     class Meta:
        model = Assignee
        fields = (
            'profile',
        )  

class ProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = Profile
        fields = (
            'id',
        )  







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
     
     value = serializers.ChoiceField(['Unknown','True','False'], default ='Unknown')
#     object_set = ObjectSerializer(read_only=True,many=True)
     class Meta:
        model = Classifier
        fields = (
            'id',
#            'object_set', # Base Model Serializer 
#            'label',
            'value',
        )

#     def to_representation(self, instance):
#         """Convert `username` to lowercase."""
#         import ipdb; ipdb.set_trace()
#         memory = Memory.objects.get(id=self.instance.Namespace.LABEL.uuid)
#         label = Memory.decord(memory._data)
#         instance.label =  
#         instance.human.object_set
         #ret = super().to_representation(instance)
#        ret['username'] = ret['username'].lower()
#         ret = super(BinaryClassifierSerializer,self).to_representation(instance)         
#         return ret
     
#     def to_internal_value(self, data):
#         return data
 
