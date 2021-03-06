from rest_framework import serializers

from project.models import Object

from buckets.models import Bucket, File, Image 
from users.models import Profile
from classifiers.serializers import BinaryClassifierSerializer

from .models import *

class ClassificationSerializer(serializers.ModelSerializer):
#    profile_set = ProfileSerializer(many=True, write_only=True)
#    assignee_set = AssigneeSerializer(many=True)
    bucket = serializers.CharField(max_length=127)
#    profile_set = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(),many=True)

    class Meta:
        model = Classification
        fields = (
#            'id',
            'bucket',
#            'profile_set',
        )
        write_only_fields = ('bucket',)
        read_only_fields = (
            'status',
        #    'profile_set'
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
        )


class JobSerializer(serializers.ModelSerializer):
    classification = ClassificationSerializer()
    profile_set = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(),many=True,write_only=True)
    class Meta:
        model = Job
        fields = (
            'id',
            'description',
            'status',
            'profile_set',
            'assignee_set',
            'classification',
            'owner',
        )
        read_only_fields=('status','owner','assignee_set')
        write_only_fields=('profile_set',)
#        depth = 2
    def to_representation(self, instance):
        instance.profile_set = [a.profile for a in instance.assignee_set.all()]
        rep = super(JobSerializer, self).to_representation(instance)
        return rep 

    def create(self, validated_data):
        classification_data = validated_data.pop("classification")
        profile_set = validated_data.pop('profile_set')

        classification_serializer = ClassificationSerializer(data=classification_data)
        classification_serializer.is_valid()
        validated_data.update(classification_serializer.data)
        bucket = validated_data.pop('bucket')
        bucket,_ = Bucket.objects.get_or_create(name=bucket)
        validated_data['bucket']=bucket
        instance = Classification.objects.create(**validated_data)
        instance = instance.job_ptr
        assignee_set = [ Assignee(job=instance, profile=p) for p in profile_set]
        Assignee.objects.bulk_create(assignee_set)
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

#class BinaryClassificationSerializer(serializers.ModelSerializer):
#    value = 

class FileSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    class Meta:
        model = File
        fields = (
            'id',
            'url',
        )
        read_only_field = ('instance',)
    def to_representation(self, instance):
        instance.url = instance._instance.url
        rep = super(FileSerializer, self).to_representation(instance)
        return rep 


class PerformSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)
    classifier = BinaryClassifierSerializer()
    class Meta:
        model = Job
        fields = (
            'id',
            'file',
            'classifier',
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
 
