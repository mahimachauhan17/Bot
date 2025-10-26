import openai
from django.conf import settings
import json

class AIService:
    """
    Service for AI operations using OpenAI GPT-4
    TODO: Add your OpenAI API key in .env file
    """
    
    def __init__(self):
        # TODO: Configure your OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
    
    def generate_job_description(self, job_title, company=''):
        """
        Generate a complete job description from a job title
        
        Args:
            job_title: The job title (e.g., "Senior Java Developer")
            company: Optional company name
            
        Returns:
            dict: Complete JD data structure
        """
        prompt = f"""
        Generate a comprehensive job description for the position: {job_title}
        {f"at {company}" if company else ""}
        
        Return a JSON object with the following structure:
        {{
            "title": "{job_title}",
            "company": "{company}",
            "description": "Detailed job description",
            "responsibilities": ["responsibility 1", "responsibility 2", ...],
            "requirements": ["requirement 1", "requirement 2", ...],
            "preferred_qualifications": ["qualification 1", ...],
            "required_skills": ["skill1", "skill2", ...],
            "nice_to_have_skills": ["skill1", "skill2", ...],
            "experience_level": "mid|senior|entry|lead"
        }}
        
        Be specific and realistic for the role.
        """
        
        try:
            # TODO: Uncomment when API key is configured
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are an expert HR professional who creates detailed job descriptions."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.7
            # )
            # 
            # jd_data = json.loads(response.choices[0].message.content)
            # return jd_data
            
            # Placeholder response until API is configured
            return {
                "title": job_title,
                "company": company or "Tech Company",
                "description": f"We are seeking an experienced {job_title} to join our dynamic team.",
                "responsibilities": [
                    "Design and develop software solutions",
                    "Collaborate with cross-functional teams",
                    "Participate in code reviews",
                    "Mentor junior team members"
                ],
                "requirements": [
                    "Bachelor's degree in Computer Science or related field",
                    "5+ years of professional experience",
                    "Strong problem-solving skills",
                    "Excellent communication abilities"
                ],
                "preferred_qualifications": [
                    "Master's degree",
                    "Experience with agile methodologies",
                    "Open source contributions"
                ],
                "required_skills": ["Python", "Java", "JavaScript", "SQL", "Git"],
                "nice_to_have_skills": ["Docker", "Kubernetes", "AWS", "React"],
                "experience_level": "mid"
            }
        
        except Exception as e:
            raise Exception(f"Failed to generate JD: {str(e)}")
    
    def generate_interview_questions(self, job_description, candidate_profile, difficulty='auto'):
        """
        Generate interview questions based on JD and candidate CV
        
        Args:
            job_description: JobDescription model instance
            candidate_profile: Candidate model instance
            difficulty: 'easy', 'medium', 'hard', or 'auto'
            
        Returns:
            list: List of question dictionaries
        """
        if difficulty == 'auto':
            # Calculate difficulty based on candidate experience
            years_exp = candidate_profile.total_experience_years
            if years_exp < 2:
                difficulty = 'easy'
            elif years_exp < 5:
                difficulty = 'medium'
            else:
                difficulty = 'hard'
        
        prompt = f"""
        Generate 12 interview questions for the following:
        
        Job: {job_description.title}
        Required Skills: {', '.join(job_description.required_skills)}
        
        Candidate:
        - Experience: {candidate_profile.total_experience_years} years
        - Skills: {', '.join(candidate_profile.technical_skills[:10])}
        - Current Role: {candidate_profile.current_title or 'N/A'}
        
        Difficulty: {difficulty}
        
        Create exactly 12 questions:
        - 5 technical questions
        - 4 behavioral questions
        - 3 scenario-based questions
        
        Return as JSON array with structure:
        [
            {{
                "question_text": "Question here?",
                "question_type": "technical|behavioral|scenario",
                "difficulty": "easy|medium|hard",
                "skills_tested": ["skill1", "skill2"],
                "expected_answer_points": ["point1", "point2"],
                "max_score": 10.0
            }},
            ...
        ]
        """
        
        try:
            # TODO: Uncomment when API key is configured
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are an expert interviewer who creates targeted, insightful interview questions."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.8
            # )
            # 
            # questions = json.loads(response.choices[0].message.content)
            # return questions
            
            # Placeholder questions until API is configured
            return [
                {
                    "question_text": f"Can you describe your experience with {job_description.required_skills[0] if job_description.required_skills else 'the required technologies'}?",
                    "question_type": "technical",
                    "difficulty": difficulty,
                    "skills_tested": job_description.required_skills[:2],
                    "expected_answer_points": ["Hands-on experience", "Specific projects", "Best practices"],
                    "max_score": 10.0
                },
                {
                    "question_text": "Tell me about a challenging project you worked on recently.",
                    "question_type": "behavioral",
                    "difficulty": difficulty,
                    "skills_tested": ["problem_solving", "communication"],
                    "expected_answer_points": ["Project context", "Challenges faced", "Solutions implemented", "Outcomes"],
                    "max_score": 10.0
                },
                {
                    "question_text": "How would you approach designing a scalable system for our use case?",
                    "question_type": "scenario",
                    "difficulty": difficulty,
                    "skills_tested": ["system_design", "scalability"],
                    "expected_answer_points": ["Architecture considerations", "Technology choices", "Trade-offs"],
                    "max_score": 10.0
                },
            ] * 4  # Repeat to get 12 questions
        
        except Exception as e:
            raise Exception(f"Failed to generate questions: {str(e)}")
    
    def evaluate_answer(self, question, answer, context=None):
        """
        Evaluate a candidate's answer using AI
        
        Args:
            question: Question object
            answer: Candidate's answer text
            context: Optional interview context
            
        Returns:
            dict: {score, feedback, strengths, improvements}
        """
        prompt = f"""
        Evaluate this interview answer:
        
        Question: {question.question_text}
        Type: {question.question_type}
        Expected points: {question.expected_answer_points}
        
        Candidate's Answer: {answer}
        
        Provide evaluation as JSON:
        {{
            "score": 7.5,  // 0-10
            "feedback": "Detailed feedback on the answer",
            "strengths": ["strength1", "strength2"],
            "improvements": ["area1", "area2"],
            "covered_points": ["point1", "point2"]
        }}
        """
        
        try:
            # TODO: Uncomment when API key is configured
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are an expert interviewer who provides fair, constructive evaluations."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.5
            # )
            # 
            # evaluation = json.loads(response.choices[0].message.content)
            # return evaluation
            
            # Placeholder evaluation
            return {
                "score": 7.5,
                "feedback": "Good answer with relevant experience mentioned.",
                "strengths": ["Clear communication", "Relevant examples"],
                "improvements": ["Could provide more technical depth"],
                "covered_points": ["Experience", "Technologies used"]
            }
        
        except Exception as e:
            raise Exception(f"Failed to evaluate answer: {str(e)}")
    
    def generate_follow_up_question(self, question, answer):
        """
        Generate an intelligent follow-up question based on the answer
        
        Args:
            question: Original question text
            answer: Candidate's answer
            
        Returns:
            str: Follow-up question
        """
        prompt = f"""
        Original Question: {question}
        Candidate's Answer: {answer}
        
        Generate a natural, probing follow-up question to dig deeper into their response.
        Return only the question text, nothing else.
        """
        
        try:
            # TODO: Uncomment when API key is configured
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[
            #         {"role": "system", "content": "You are an expert interviewer asking insightful follow-up questions."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.7,
            #     max_tokens=100
            # )
            # 
            # return response.choices[0].message.content.strip()
            
            # Placeholder
            return "That's interesting. Can you elaborate more on the technical challenges you faced?"
        
        except Exception as e:
            return "Can you tell me more about that?"
