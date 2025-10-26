from django.contrib import admin
from .models import JobDescription

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'experience_level', 'is_active', 'created_at')
    list_filter = ('experience_level', 'job_type', 'is_active', 'ai_generated')
    search_fields = ('title', 'company', 'description')
    readonly_fields = ('_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'department', 'description')
        }),
        ('Job Details', {
            'fields': ('experience_level', 'job_type', 'location', 'salary_range')
        }),
        ('Skills & Requirements', {
            'fields': ('required_skills', 'nice_to_have_skills', 'responsibilities', 
                      'requirements', 'preferred_qualifications')
        }),
        ('Interview Settings', {
            'fields': ('default_difficulty', 'enable_video_analysis', 
                      'interview_duration_minutes')
        }),
        ('Metadata', {
            'fields': ('_id', 'created_by', 'is_active', 'ai_generated', 
                      'created_at', 'updated_at')
        }),
    )
