from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Candidate, CandidateNote

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ('_id', 'created_at', 'updated_at', 'uploaded_by', 'parsing_status', 'parsing_error')

class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        exclude = ('_id', 'created_at', 'updated_at', 'uploaded_by', 'parsing_status', 'parsing_error', 'cv_parsed_data')

class CandidateNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = CandidateNote
        fields = '__all__'
        read_only_fields = ('_id', 'created_at', 'updated_at', 'author')
