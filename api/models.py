# api/models.py
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    signature = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    simplified_text = models.TextField(blank=True, null=True)
    doc_type = models.CharField(max_length=100, blank=True, null=True)
    risk_score = models.IntegerField(default=0)
    fraud_score = models.IntegerField(default=0)
    compliance_score = models.IntegerField(default=0)
    risk_analysis_json = models.JSONField(blank=True, null=True)
    fraud_analysis_json = models.JSONField(blank=True, null=True)
    compliance_json = models.JSONField(blank=True, null=True)
    key_data_json = models.JSONField(blank=True, null=True)
    clauses_json = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.original_filename

class History(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.document.original_filename} - {self.action}'

    class Meta:
        ordering = ['-timestamp']

class GeneratedClause(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    template_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title