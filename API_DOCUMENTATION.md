# API Documentation

## Base URL
```
Development: http://localhost:8000/api
Production: https://api.yourdomain.com/api
```

## Authentication

All API endpoints (except public ones) require JWT authentication.

### Get Access Token
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user"
  }
}
```

### Use Token in Requests
```http
GET /api/jobs/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## Job Descriptions

### List All Jobs
```http
GET /api/jobs/

Response:
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "_id": "uuid",
      "title": "Senior Java Developer",
      "company": "Tech Corp",
      "description": "...",
      "required_skills": ["Java", "Spring", "SQL"],
      "experience_level": "senior",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Create Job
```http
POST /api/jobs/
Content-Type: application/json

{
  "title": "Senior Java Developer",
  "company": "Tech Corp",
  "description": "We are looking for...",
  "responsibilities": [
    "Design and develop Java applications",
    "Lead technical discussions"
  ],
  "requirements": [
    "5+ years Java experience",
    "Strong knowledge of Spring Framework"
  ],
  "required_skills": ["Java", "Spring", "SQL", "REST API"],
  "experience_level": "senior",
  "job_type": "full_time",
  "default_difficulty": "auto",
  "enable_video_analysis": true
}

Response: 201 Created
{
  "_id": "uuid",
  "title": "Senior Java Developer",
  ...
}
```

### Generate JD from Title (AI)
```http
POST /api/jobs/generate_from_title/
Content-Type: application/json

{
  "title": "Java Developer",
  "company": "Tech Corp"
}

Response: 201 Created
{
  "_id": "uuid",
  "title": "Java Developer",
  "description": "AI-generated description...",
  "responsibilities": [...],
  "requirements": [...],
  "required_skills": [...],
  "ai_generated": true
}
```

### Get Job Details
```http
GET /api/jobs/{job_id}/

Response:
{
  "_id": "uuid",
  "title": "Senior Java Developer",
  ...
}
```

### Update Job
```http
PUT /api/jobs/{job_id}/
PATCH /api/jobs/{job_id}/  (partial update)

{
  "title": "Lead Java Developer",
  "is_active": false
}
```

### Delete Job
```http
DELETE /api/jobs/{job_id}/

Response: 204 No Content
```

---

## Candidates

### List All Candidates
```http
GET /api/candidates/

Response:
{
  "count": 25,
  "results": [
    {
      "_id": "uuid",
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "technical_skills": ["Python", "Django", "React"],
      "total_experience_years": 5.5,
      "parsing_status": "completed",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Upload CV
```http
POST /api/candidates/upload_cv/
Content-Type: multipart/form-data

cv_file: [file]

Response: 201 Created
{
  "_id": "uuid",
  "full_name": "John Doe",
  "email": "john@example.com",
  "technical_skills": ["Python", "Django", "JavaScript"],
  "work_experience": [...],
  "education": [...],
  "parsing_status": "completed"
}
```

### Get Candidate Details
```http
GET /api/candidates/{candidate_id}/

Response:
{
  "_id": "uuid",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "location": "New York, NY",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "summary": "Experienced software developer...",
  "technical_skills": ["Python", "Django", "React", "PostgreSQL"],
  "soft_skills": ["Leadership", "Communication"],
  "work_experience": [
    {
      "company": "Tech Corp",
      "title": "Senior Developer",
      "start_date": "2020-01",
      "end_date": "2023-12",
      "description": "Led development team..."
    }
  ],
  "education": [
    {
      "degree": "Bachelor of Science",
      "institution": "University",
      "field": "Computer Science",
      "end_date": "2019"
    }
  ],
  "total_experience_years": 5.5
}
```

### Add Note to Candidate
```http
POST /api/candidates/{candidate_id}/add_note/

{
  "content": "Strong technical background, good communication skills."
}

Response: 201 Created
{
  "_id": "note_uuid",
  "candidate": "candidate_uuid",
  "author": "recruiter_user_id",
  "author_name": "Recruiter Name",
  "content": "Strong technical background...",
  "created_at": "2024-01-15T10:00:00Z"
}
```

---

## Interviews

### List All Interviews
```http
GET /api/interviews/

Query Parameters:
- status: scheduled|in_progress|completed|cancelled
- job: job_id
- candidate: candidate_id

Response:
{
  "count": 15,
  "results": [
    {
      "_id": "uuid",
      "job": {...},
      "candidate": {...},
      "interview_type": "video",
      "status": "scheduled",
      "scheduled_at": "2024-01-20T14:00:00Z",
      "difficulty": "auto",
      "enable_video_analysis": true,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Create Interview
```http
POST /api/interviews/

{
  "job": "job_uuid",
  "candidate": "candidate_uuid",
  "interview_type": "video",  // or "chat"
  "difficulty": "auto",  // or "easy", "medium", "hard"
  "scheduled_at": "2024-01-20T14:00:00Z",
  "duration_minutes": 60,
  "enable_video_analysis": true,
  "enable_recording": true
}

Response: 201 Created
{
  "_id": "interview_uuid",
  "job": {...},
  "candidate": {...},
  "interview_link": "https://yourdomain.com/interview/interview_uuid",
  "invite_token": "unique_token",
  "status": "scheduled",
  ...
}
```

### Get Interview Details
```http
GET /api/interviews/{interview_id}/

Response:
{
  "_id": "uuid",
  "job": {
    "_id": "job_uuid",
    "title": "Senior Java Developer"
  },
  "candidate": {
    "_id": "candidate_uuid",
    "full_name": "John Doe",
    "email": "john@example.com"
  },
  "interview_type": "video",
  "status": "completed",
  "scheduled_at": "2024-01-20T14:00:00Z",
  "started_at": "2024-01-20T14:02:00Z",
  "ended_at": "2024-01-20T14:58:00Z",
  "full_transcript": [
    {
      "timestamp": "2024-01-20T14:02:00Z",
      "speaker": "ai",
      "text": "Hello! Let's begin the interview..."
    },
    {
      "timestamp": "2024-01-20T14:02:30Z",
      "speaker": "candidate",
      "text": "Thank you, I'm ready."
    }
  ],
  "video_recording_url": "https://storage.../recording.mp4",
  "body_language_analysis": {
    "overall_summary": "Candidate showed high engagement...",
    "confidence_score": 8.5,
    "key_moments": [...]
  }
}
```

---

## WebSocket - Real-time Interview

### Connect to Interview
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/interview/{interview_id}/');

// Connection established
ws.onopen = () => {
  console.log('Connected to interview');
};

// Receive messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Message:', data);
};
```

### Message Types

#### Start Interview
```javascript
ws.send(JSON.stringify({
  type: 'start_interview'
}));

// Server response:
{
  type: 'interview_started',
  message: "Hello! I'm your AI interviewer...",
  timestamp: "2024-01-20T14:00:00Z"
}
```

#### Send Candidate Message
```javascript
ws.send(JSON.stringify({
  type: 'candidate_message',
  content: 'I have 5 years of experience with Java...'
}));

// Server broadcasts:
{
  type: 'message',
  sender: 'candidate',
  content: 'I have 5 years...',
  message_id: 'uuid',
  timestamp: "2024-01-20T14:02:00Z"
}

// Then AI responds:
{
  type: 'message',
  sender: 'ai',
  content: 'That\'s great! Can you tell me more about...',
  message_id: 'uuid',
  timestamp: "2024-01-20T14:02:05Z"
}
```

#### Send Audio Data (for STT)
```javascript
ws.send(JSON.stringify({
  type: 'audio_data',
  audio: base64_encoded_audio_chunk
}));

// Server response:
{
  type: 'audio_processed',
  status: 'received'
}
```

#### End Interview
```javascript
ws.send(JSON.stringify({
  type: 'end_interview'
}));

// Server response:
{
  type: 'interview_ended',
  message: 'Interview session ended. Thank you!'
}
```

---

## Scoring & Reports

### Get Interview Score
```http
GET /api/interviews/{interview_id}/score/

Response:
{
  "_id": "uuid",
  "interview": "interview_uuid",
  "overall_score": 8.2,
  "technical_skills_score": 8.5,
  "problem_solving_score": 8.0,
  "communication_score": 8.5,
  "cultural_fit_score": 7.8,
  "experience_relevance_score": 8.4,
  "confidence_score": 8.0,  // from body language
  "engagement_score": 8.7,  // from facial analysis
  "question_scores": [
    {
      "question_id": "uuid",
      "score": 8.5,
      "max_score": 10,
      "feedback": "Excellent answer with clear examples."
    }
  ],
  "strengths": [
    "Strong technical knowledge",
    "Good communication skills",
    "Relevant experience"
  ],
  "weaknesses": [
    "Could improve system design approach"
  ],
  "recommendation": "hire",  // strong_hire|hire|maybe|no_hire
  "recommendation_reasoning": "Candidate demonstrates strong...",
  "calculated_at": "2024-01-20T15:00:00Z"
}
```

### Get Interview Report
```http
GET /api/reports/{interview_id}/

Response:
{
  "_id": "uuid",
  "interview": "interview_uuid",
  "executive_summary": "Candidate performed well across...",
  "technical_assessment": "Strong knowledge of Java...",
  "behavioral_assessment": "Demonstrated good leadership...",
  "communication_assessment": "Clear and articulate...",
  "non_verbal_summary": "High engagement throughout...",
  "overall_score": 8.2,
  "recommendation": "hire",
  "share_token": "unique_share_token",
  "pdf_url": "https://storage.../report.pdf",
  "generated_at": "2024-01-20T15:00:00Z"
}
```

### Export Report as PDF
```http
GET /api/reports/{interview_id}/export/

Response: PDF file download
```

---

## Question Generation

### Generate Questions for Interview
```http
POST /api/questions/generate/

{
  "job_id": "job_uuid",
  "candidate_id": "candidate_uuid",
  "difficulty": "auto",  // or "easy", "medium", "hard"
  "count": 12
}

Response:
{
  "questions": [
    {
      "_id": "uuid",
      "question_text": "Can you describe your experience with Java?",
      "question_type": "technical",
      "difficulty": "medium",
      "skills_tested": ["Java", "OOP"],
      "expected_answer_points": [
        "Years of experience",
        "Specific projects",
        "Technologies used"
      ],
      "max_score": 10.0
    },
    ...
  ],
  "total_count": 12
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "details": "Detailed error information (if available)",
  "code": "ERROR_CODE"
}
```

### Common Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success, no response body
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

- **Standard endpoints**: 100 requests per minute
- **Authentication**: 10 requests per minute
- **File uploads**: 10 requests per minute
- **WebSocket connections**: 5 connections per user

Exceeded limits return `429 Too Many Requests`.

---

## Webhooks (Future Feature)

Webhooks can be configured to receive notifications for:
- Interview completed
- Report generated
- Candidate applied
- Interview scheduled

---

For more details, see the main README.md file.
