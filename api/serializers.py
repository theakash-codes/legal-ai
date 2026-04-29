from rest_framework import serializers
from .models import Document, History, GeneratedClause

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'owner', 'original_filename', 'uploaded_at', 'content', 'doc_type',
                  'risk_score', 'fraud_score', 'compliance_score', 'summary']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['action', 'timestamp']

class GeneratedClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedClause
        fields = ['id', 'template_type', 'title', 'content', 'created_at']