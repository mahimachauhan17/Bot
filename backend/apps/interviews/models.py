from djongo import models
from django.contrib.auth.models import User
import uuid
from apps.jobs.models import JobDescription
from apps.candidates.models import Candidate

class Interview(models.Model):
    """
    Interview model - stores interview sessions
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='interviews')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interviews')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='interviews_created')
    
    # Interview Type
    interview_type = models.CharField(
        max_length=20,
        choices=[
            ('chat', 'Chat Interview'),
            ('video', 'Video Interview (AI Voice)')
        ],
        default='chat'
    )
    
    # Difficulty
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
            ('auto', 'Auto (from CV)')
        ],
        default='auto'
    )
    calculated_difficulty = models.CharField(max_length=20, blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('invited', 'Invited'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show')
        ],
        default='scheduled'
    )
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=60)
    
    # Interview Link
    interview_link = models.CharField(max_length=500, blank=True, null=True)
    invite_token = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Settings
    enable_video_analysis = models.BooleanField(default=True)
    video_analysis_consent = models.BooleanField(default=False)
    enable_recording = models.BooleanField(default=True)
    enable_captions = models.BooleanField(default=True)
    
    # Recording
    video_recording_url = models.CharField(max_length=500, blank=True, null=True)
    audio_recording_url = models.CharField(max_length=500, blank=True, null=True)
    
    # Transcript
    full_transcript = models.JSONField(default=list, blank=True, null=True)
    # Each item: {timestamp, speaker, text, question_id}
    
    # Non-verbal Analysis (Video only)
    body_language_analysis = models.JSONField(default=dict, blank=True, null=True)
    # {overall_summary, confidence_score, key_moments: [{timestamp, observation, score}]}
    
    facial_expression_analysis = models.JSONField(default=dict, blank=True, null=True)
    # {dominant_emotions, engagement_score, key_moments: [{timestamp, emotion, intensity}]}
    
    # Connection quality
    connection_log = models.JSONField(default=list, blank=True, null=True)
    # [{timestamp, event_type, details}]
    
    fallback_mode_used = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notes
    interviewer_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'interviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Interview: {self.candidate.full_name} for {self.job.title}"


class InterviewMessage(models.Model):
    """
    Individual messages/interactions during an interview
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='messages')
    
    # Message details
    sender = models.CharField(
        max_length=20,
        choices=[
            ('ai', 'AI Interviewer'),
            ('candidate', 'Candidate')
        ]
    )
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('question', 'Question'),
            ('answer', 'Answer'),
            ('followup', 'Follow-up'),
            ('system', 'System Message')
        ]
    )
    
    content = models.TextField()
    question_id = models.UUIDField(null=True, blank=True)  # Reference to Question model
    
    # Timing
    timestamp = models.DateTimeField(auto_now_add=True)
    audio_duration_seconds = models.FloatField(null=True, blank=True)
    
    # For voice interviews
    audio_url = models.CharField(max_length=500, blank=True, null=True)
    transcription_confidence = models.FloatField(null=True, blank=True)
    
    # Scoring (if applicable)
    score = models.FloatField(null=True, blank=True)
    score_breakdown = models.JSONField(default=dict, blank=True, null=True)
    
    class Meta:
        db_table = 'interview_messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."
