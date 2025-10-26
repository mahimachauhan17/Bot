from django.contrib import admin
from .models import Interview, InterviewMessage

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('get_candidate_name', 'get_job_title', 'interview_type', 
                   'status', 'scheduled_at', 'created_at')
    list_filter = ('interview_type', 'status', 'difficulty', 'scheduled_at')
    search_fields = ('candidate__full_name', 'job__title', 'job__company')
    readonly_fields = ('_id', 'created_at', 'updated_at', 'started_at', 'ended_at', 
                      'interview_link', 'invite_token')
    
    fieldsets = (
        ('Interview Details', {
            'fields': ('job', 'candidate', 'interview_type', 'difficulty')
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'duration_minutes', 'started_at', 'ended_at')
        }),
        ('Status & Links', {
            'fields': ('status', 'interview_link', 'invite_token')
        }),
        ('Recording & Analysis', {
            'fields': ('enable_video_analysis', 'enable_recording', 
                      'video_recording_url', 'full_transcript')
        }),
        ('Video Analysis Results', {
            'fields': ('body_language_analysis', 'facial_expression_analysis'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('_id', 'created_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_candidate_name(self, obj):
        return obj.candidate.full_name if obj.candidate else 'N/A'
    get_candidate_name.short_description = 'Candidate'
    
    def get_job_title(self, obj):
        return f"{obj.job.title} - {obj.job.company}" if obj.job else 'N/A'
    get_job_title.short_description = 'Job'

@admin.register(InterviewMessage)
class InterviewMessageAdmin(admin.ModelAdmin):
    list_display = ('get_interview', 'sender', 'get_content_preview', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('interview__candidate__full_name', 'content')
    readonly_fields = ('_id', 'timestamp')
    
    def get_interview(self, obj):
        return f"{obj.interview.candidate.full_name} - {obj.interview.job.title}"
    get_interview.short_description = 'Interview'
    
    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = 'Content'
