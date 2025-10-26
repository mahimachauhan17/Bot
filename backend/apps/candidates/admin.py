from django.contrib import admin
from .models import Candidate, CandidateNote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'total_experience_years', 
                   'parsing_status', 'created_at')
    list_filter = ('parsing_status', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'technical_skills', 'location')
    readonly_fields = ('_id', 'created_at', 'updated_at', 'parsing_status', 'parsing_error')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'location', 'linkedin_url', 
                      'portfolio_url')
        }),
        ('Professional Summary', {
            'fields': ('summary', 'total_experience_years')
        }),
        ('Skills', {
            'fields': ('technical_skills', 'soft_skills', 'languages', 'certifications')
        }),
        ('Experience & Education', {
            'fields': ('work_experience', 'education', 'projects')
        }),
        ('CV Information', {
            'fields': ('cv_file', 'cv_parsed_data', 'parsing_status', 'parsing_error')
        }),
        ('Metadata', {
            'fields': ('_id', 'uploaded_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(CandidateNote)
class CandidateNoteAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'author_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'candidate__full_name', 'author__username')
    readonly_fields = ('_id', 'created_at', 'updated_at', 'author')
    
    def author_name(self, obj):
        return obj.author.username if obj.author else 'N/A'
    author_name.short_description = 'Author'
