from djongo import models
import uuid
from apps.interviews.models import Interview

class InterviewReport(models.Model):
    """
    Comprehensive interview report
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, related_name='report')
    
    # Executive Summary
    executive_summary = models.TextField()
    
    # Detailed Sections
    technical_assessment = models.TextField(blank=True, null=True)
    behavioral_assessment = models.TextField(blank=True, null=True)
    communication_assessment = models.TextField(blank=True, null=True)
    
    # Video Analysis (if applicable)
    non_verbal_summary = models.TextField(blank=True, null=True)
    
    # Scores Reference
    overall_score = models.FloatField()  # Denormalized from InterviewScore
    recommendation = models.CharField(max_length=50)
    
    # Report Metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Sharing
    share_token = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_shared = models.BooleanField(default=False)
    
    # Export
    pdf_url = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        db_table = 'interview_reports'
    
    def __str__(self):
        return f"Report for {self.interview.candidate.full_name}"
