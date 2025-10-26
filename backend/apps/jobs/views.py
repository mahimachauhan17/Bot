from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import JobDescription
from .serializers import JobDescriptionSerializer, JobDescriptionCreateSerializer
from apps.integrations.services.ai_service import AIService

class JobDescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Job Descriptions
    """
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return JobDescriptionCreateSerializer
        return JobDescriptionSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_from_title(self, request):
        """
        Generate a complete JD from just a job title using AI
        POST /api/jobs/generate_from_title/
        Body: {"title": "Java Developer", "company": "Tech Corp"}
        """
        job_title = request.data.get('title')
        company = request.data.get('company', '')
        
        if not job_title:
            return Response(
                {'error': 'Job title is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ai_service = AIService()
            jd_data = ai_service.generate_job_description(job_title, company)
            
            # Create the JD
            jd_data['created_by'] = request.user
            jd_data['ai_generated'] = True
            jd = JobDescription.objects.create(**jd_data)
            
            serializer = JobDescriptionSerializer(jd)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Duplicate an existing JD
        POST /api/jobs/{id}/duplicate/
        """
        jd = self.get_object()
        jd.pk = None
        jd._id = None
        jd.title = f"{jd.title} (Copy)"
        jd.created_by = request.user
        jd.save()
        
        serializer = JobDescriptionSerializer(jd)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get only active job descriptions
        GET /api/jobs/active/
        """
        active_jobs = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_jobs)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_jobs, many=True)
        return Response(serializer.data)
