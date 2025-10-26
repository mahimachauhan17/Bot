from djongo import models
import uuid
from apps.interviews.models import Interview

class InterviewScore(models.Model):
    """
    Comprehensive scoring for an interview
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, related_name='score')
    
    # Overall Score
    overall_score = models.FloatField(default=0.0)  # 0-10
    
    # Parameter Scores (0-10 each)
    technical_skills_score = models.FloatField(default=0.0)
    problem_solving_score = models.FloatField(default=0.0)
    communication_score = models.FloatField(default=0.0)
    cultural_fit_score = models.FloatField(default=0.0)
    experience_relevance_score = models.FloatField(default=0.0)
    
    # Video-specific scores (if applicable)
    confidence_score = models.FloatField(null=True, blank=True)  # From body language
    engagement_score = models.FloatField(null=True, blank=True)  # From facial expressions
    professionalism_score = models.FloatField(null=True, blank=True)
    
    # Weights for overall calculation
    score_weights = models.JSONField(default=dict)
    # {technical_skills: 0.3, problem_solving: 0.25, communication: 0.2, ...}
    
    # Detailed breakdown
    question_scores = models.JSONField(default=list)
    # [{question_id, score, max_score, feedback}]
    
    # AI Analysis
    strengths = models.JSONField(default=list)  # List of identified strengths
    weaknesses = models.JSONField(default=list)  # List of areas for improvement
    key_insights = models.TextField(blank=True, null=True)
    
    # Recommendation
    recommendation = models.CharField(
        max_length=50,
        choices=[
            ('strong_hire', 'Strong Hire'),
            ('hire', 'Hire'),
            ('maybe', 'Maybe'),
            ('no_hire', 'No Hire')
        ],
        blank=True,
        null=True
    )
    recommendation_reasoning = models.TextField(blank=True, null=True)
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    calculated_by_ai = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'interview_scores'
    
    def __str__(self):
        return f"Score for {self.interview.candidate.full_name}: {self.overall_score}/10"
    
    def calculate_overall_score(self):
        """
        Calculate weighted overall score
        """
        if not self.score_weights:
            # Default equal weights
            self.score_weights = {
                'technical_skills': 0.25,
                'problem_solving': 0.20,
                'communication': 0.20,
                'cultural_fit': 0.15,
                'experience_relevance': 0.20
            }
        
        score = 0.0
        score += self.technical_skills_score * self.score_weights.get('technical_skills', 0)
        score += self.problem_solving_score * self.score_weights.get('problem_solving', 0)
        score += self.communication_score * self.score_weights.get('communication', 0)
        score += self.cultural_fit_score * self.score_weights.get('cultural_fit', 0)
        score += self.experience_relevance_score * self.score_weights.get('experience_relevance', 0)
        
        self.overall_score = round(score, 2)
        return self.overall_score
