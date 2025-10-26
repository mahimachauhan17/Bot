from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from .models import Candidate, CandidateNote
from .serializers import CandidateSerializer, CandidateCreateSerializer, CandidateNoteSerializer
from apps.integrations.services.cv_parser_service import CVParserService

class CandidateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Candidates
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CandidateCreateSerializer
        return CandidateSerializer
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upload_cv(self, request):
        """
        Upload and parse a CV file
        POST /api/candidates/upload_cv/
        Body: multipart/form-data with 'cv_file' field
        """
        if 'cv_file' not in request.FILES:
            return Response(
                {'error': 'CV file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cv_file = request.FILES['cv_file']
        
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_ext = cv_file.name.lower()[cv_file.name.rfind('.'):]
        
        if file_ext not in allowed_extensions:
            return Response(
                {'error': f'File type not supported. Allowed: {", ".join(allowed_extensions)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create candidate record
            candidate = Candidate.objects.create(
                full_name='Pending',
                email='pending@parse.com',
                cv_file=cv_file,
                cv_file_name=cv_file.name,
                uploaded_by=request.user,
                parsing_status='processing'
            )
            
            # Parse CV asynchronously (in production, use Celery)
            try:
                cv_parser = CVParserService()
                parsed_data = cv_parser.parse_cv(cv_file)
                
                # Update candidate with parsed data
                candidate.full_name = parsed_data.get('full_name', 'Unknown')
                candidate.email = parsed_data.get('email', f'candidate_{candidate._id}@temp.com')
                candidate.phone = parsed_data.get('phone')
                candidate.location = parsed_data.get('location')
                candidate.linkedin_url = parsed_data.get('linkedin_url')
                candidate.summary = parsed_data.get('summary')
                candidate.current_title = parsed_data.get('current_title')
                candidate.total_experience_years = parsed_data.get('total_experience_years', 0)
                candidate.technical_skills = parsed_data.get('technical_skills', [])
                candidate.soft_skills = parsed_data.get('soft_skills', [])
                candidate.languages = parsed_data.get('languages', [])
                candidate.certifications = parsed_data.get('certifications', [])
                candidate.work_experience = parsed_data.get('work_experience', [])
                candidate.education = parsed_data.get('education', [])
                candidate.projects = parsed_data.get('projects', [])
                candidate.cv_parsed_data = parsed_data
                candidate.parsing_status = 'completed'
                candidate.save()
                
                serializer = CandidateSerializer(candidate)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as parse_error:
                candidate.parsing_status = 'failed'
                candidate.parsing_error = str(parse_error)
                candidate.save()
                
                return Response(
                    {
                        'error': 'CV parsing failed',
                        'details': str(parse_error),
                        'candidate_id': str(candidate._id)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        """
        Get all notes for a candidate
        GET /api/candidates/{id}/notes/
        """
        candidate = self.get_object()
        notes = candidate.notes.all()
        serializer = CandidateNoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """
        Add a note to a candidate
        POST /api/candidates/{id}/add_note/
        Body: {"content": "Note content"}
        """
        candidate = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response(
                {'error': 'Note content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        note = CandidateNote.objects.create(
            candidate=candidate,
            author=request.user,
            content=content
        )
        
        serializer = CandidateNoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CandidateNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Candidate Notes
    """
    queryset = CandidateNote.objects.all()
    serializer_class = CandidateNoteSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
