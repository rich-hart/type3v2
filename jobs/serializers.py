from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'description',
            'status',
            #'progress',
        )

