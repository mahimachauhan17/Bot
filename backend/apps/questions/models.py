from djongo import models
import uuid
from apps.jobs.models import JobDescription
from apps.candidates.models import Candidate

class Question(models.Model):
    """
    Interview question model
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='questions')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    
    # Question details
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('technical', 'Technical'),
            ('behavioral', 'Behavioral'),
            ('scenario', 'Scenario-based'),
            ('cultural_fit', 'Cultural Fit')
        ]
    )
    
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ],
        default='medium'
    )
    
    # Scoring criteria
    expected_answer_points = models.JSONField(default=list, blank=True, null=True)
    # List of key points expected in answer
    
    scoring_rubric = models.JSONField(default=dict, blank=True, null=True)
    # Detailed scoring criteria
    
    max_score = models.FloatField(default=10.0)
    weight = models.FloatField(default=1.0)  # Weight in overall score
    
    # Skills being tested
    skills_tested = models.JSONField(default=list)
    
    # Metadata
    order = models.IntegerField(default=0)  # Order in interview
    is_active = models.BooleanField(default=True)
    ai_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Follow-up
    enable_followup = models.BooleanField(default=True)
    max_followups = models.IntegerField(default=2)
    
    class Meta:
        db_table = 'questions'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.question_type}: {self.question_text[:50]}..."


class QuestionSet(models.Model):
    """
    Pre-defined set of questions for a job role
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    job_role = models.CharField(max_length=200)
    
    questions = models.JSONField(default=list)  # List of question IDs
    
    is_template = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'question_sets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.job_role}"
