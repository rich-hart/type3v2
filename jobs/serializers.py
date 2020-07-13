from rest_framework import serializers

from .models import Job, Classification


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


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = (
            'id',
            'description',
            'status',
            'assignee_set',
#            'classifier',
            #'progress',
        )

