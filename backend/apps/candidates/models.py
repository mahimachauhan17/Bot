from djongo import models
from django.contrib.auth.models import User
import uuid

class Candidate(models.Model):
    """
    Candidate model - stores candidate profiles parsed from CVs
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    
    # Professional Summary
    summary = models.TextField(blank=True, null=True)
    current_title = models.CharField(max_length=200, blank=True, null=True)
    total_experience_years = models.FloatField(default=0)
    
    # Skills
    technical_skills = models.JSONField(default=list)  # List of technical skills
    soft_skills = models.JSONField(default=list)  # List of soft skills
    languages = models.JSONField(default=list)  # List of languages with proficiency
    certifications = models.JSONField(default=list)  # List of certifications
    
    # Experience
    work_experience = models.JSONField(default=list)  # List of work experiences
    # Each item: {company, title, start_date, end_date, description, achievements}
    
    # Education
    education = models.JSONField(default=list)  # List of education records
    # Each item: {institution, degree, field, start_date, end_date, gpa}
    
    # Projects
    projects = models.JSONField(default=list, blank=True, null=True)
    # Each item: {name, description, technologies, url}
    
    # CV File
    cv_file = models.FileField(upload_to='cvs/', null=True, blank=True)
    cv_file_name = models.CharField(max_length=255, blank=True, null=True)
    cv_parsed_data = models.JSONField(default=dict, blank=True, null=True)  # Raw parsed data
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='candidates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parsing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    parsing_error = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'candidates'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.email}"


class CandidateNote(models.Model):
    """
    Notes about candidates added by recruiters
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'candidate_notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.candidate.full_name} by {self.author}"
