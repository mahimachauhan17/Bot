from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, CandidateNoteViewSet

router = DefaultRouter()
router.register(r'', CandidateViewSet, basename='candidate')
router.register(r'notes', CandidateNoteViewSet, basename='candidate-note')

urlpatterns = [
    path('', include(router.urls)),
]
