from rest_framework import serializers


from buckets.models import Bucket
from users.models import Profile

from .models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'description',
            'status',
            'assignee_set',
            #'progress',
        )

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


class ClassificationSerializer(serializers.ModelSerializer):
#    profile_set = ProfileSerializer(many=True, write_only=True)
#    assignee_set = AssigneeSerializer(many=True)
    bucket = serializers.CharField(max_length=127)
    class Meta:
        model = Classification
        fields = (
            'id',
            'description',
            'status',
            'bucket',
            'assignee_set',
#            'profile_set',
#            'classifier',
            #'progress',
        )
        write_only_fields = ('bucket',)
        read_only_fields = ('status',)

    def create(self, validated_data):
        bucket = validated_data.pop('bucket')
        bucket,_ = Bucket.objects.get_or_create(name=bucket)
        validated_data['bucket']=bucket
        assignee_set = validated_data.pop('assignee_set')
        instance = Classification.objects.create(**validated_data)
        return instance
