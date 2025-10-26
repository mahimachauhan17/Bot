from djongo import models
from django.contrib.auth.models import User
import uuid

class JobDescription(models.Model):
    """
    Job Description model - stores job postings and requirements
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, default='')
    department = models.CharField(max_length=100, blank=True, null=True)
    
    # Job details
    description = models.TextField()
    responsibilities = models.JSONField(default=list)  # List of responsibilities
    requirements = models.JSONField(default=list)  # List of requirements
    preferred_qualifications = models.JSONField(default=list)
    
    # Job specifics
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
            ('lead', 'Lead/Principal')
        ],
        default='mid'
    )
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('contract', 'Contract'),
            ('internship', 'Internship')
        ],
        default='full_time'
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    salary_range = models.JSONField(default=dict, blank=True, null=True)  # {min, max, currency}
    
    # Technical skills
    required_skills = models.JSONField(default=list)
    nice_to_have_skills = models.JSONField(default=list)
    
    # Interview settings
    default_difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
            ('auto', 'Auto (based on CV)')
        ],
        default='auto'
    )
    enable_video_analysis = models.BooleanField(default=True)
    interview_duration_minutes = models.IntegerField(default=60)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='job_descriptions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    ai_generated = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'job_descriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company}"
