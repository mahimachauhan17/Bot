from rest_framework import serializers
from .models import JobDescription

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = '__all__'
        read_only_fields = ('_id', 'created_at', 'updated_at', 'created_by')

class JobDescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        exclude = ('_id', 'created_at', 'updated_at', 'created_by')
