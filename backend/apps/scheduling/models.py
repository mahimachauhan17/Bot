from djongo import models
import uuid
from apps.interviews.models import Interview
from django.contrib.auth.models import User

class InterviewSchedule(models.Model):
    """
    Interview scheduling model
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, related_name='schedule')
    
    # Scheduling
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Calendar Integration
    google_calendar_event_id = models.CharField(max_length=200, blank=True, null=True)
    outlook_calendar_event_id = models.CharField(max_length=200, blank=True, null=True)
    
    # Reminders
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Attendees
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_interviews')
    attendee_email = models.EmailField()
    
    # Meeting Details
    meeting_link = models.URLField(blank=True, null=True)
    meeting_platform = models.CharField(
        max_length=20,
        choices=[
            ('webrtc', 'In-App WebRTC'),
            ('zoom', 'Zoom'),
            ('teams', 'Microsoft Teams'),
            ('meet', 'Google Meet')
        ],
        default='webrtc'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('reminded', 'Reminder Sent'),
            ('started', 'Started'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('rescheduled', 'Rescheduled')
        ],
        default='scheduled'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'interview_schedules'
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"Schedule for {self.interview.candidate.full_name} on {self.scheduled_date}"
