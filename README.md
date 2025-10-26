# Interviewer AI Agent

A comprehensive AI-powered interview platform that automates the entire interview process from job description generation to candidate evaluation.

## 🚀 Features

- **AI Job Descriptions**: Generate complete JDs from job titles using GPT-4
- **Smart CV Parsing**: Extract structured data from PDF, DOCX, and TXT resumes
- **Intelligent Question Generation**: Create role-specific technical, behavioral, and scenario-based questions
- **Live Video Interviews**: AI speaks and listens in real-time using TTS and STT
- **Chat Interviews**: Text-based alternative with contextual follow-ups
- **Body Language Analysis**: Analyze facial expressions and posture during video interviews
- **Comprehensive Scoring**: 0-10 scores across multiple parameters with hiring recommendations
- **Detailed Reports**: Export and share interview reports with insights
- **Scheduling**: Calendar integration with reminders

## 🏗️ Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: MongoDB (via Djongo)
- **WebSockets**: Django Channels + Redis
- **AI**: OpenAI GPT-4.5
- **Speech**: Google Cloud Speech-to-Text, Azure TTS
- **Vision**: OpenCV + MediaPipe
- **Task Queue**: Celery + Redis

### Frontend
- **Framework**: Next.js 14 + React 18
- **Styling**: TailwindCSS
- **State**: Zustand + React Query
- **Real-time**: WebSocket (socket.io-client)
- **Video**: WebRTC + react-webcam

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB 5.0+
- Redis 6.0+
- Docker & Docker Compose (optional)

## 🛠️ Installation & Setup

### Backend Setup

1. **Clone the repository**
```bash
cd Bot/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Required API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here
GOOGLE_CLOUD_CREDENTIALS_PATH=/path/to/google-credentials.json
AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=your-region

# Database
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=interviewer_ai_db

# Redis
REDIS_URL=redis://localhost:6379/0
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
# Start Django
python manage.py runserver

# In another terminal, start Celery worker
celery -A config worker -l info

# In another terminal, start Channels (for WebSocket)
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

### Frontend Setup

1. **Navigate to frontend**
```bash
cd Bot/frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.local.example .env.local
```

4. **Start development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🔑 API Keys Setup

### OpenAI API
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Google Cloud Speech-to-Text
1. Go to Google Cloud Console
2. Enable Speech-to-Text API
3. Create service account and download JSON credentials
4. Add path to `.env`: `GOOGLE_CLOUD_CREDENTIALS_PATH=/path/to/credentials.json`

### Azure Speech Services
1. Go to Azure Portal
2. Create Speech resource
3. Get key and region
4. Add to `.env`:
   - `AZURE_SPEECH_KEY=your-key`
   - `AZURE_SPEECH_REGION=your-region`

## 📁 Project Structure

```
Bot/
├── backend/
│   ├── config/              # Django settings
│   ├── apps/
│   │   ├── jobs/           # Job descriptions
│   │   ├── candidates/     # CV parsing & profiles
│   │   ├── interviews/     # Interview sessions
│   │   ├── questions/      # Question generation
│   │   ├── scoring/        # Evaluation engine
│   │   ├── reports/        # Report generation
│   │   ├── scheduling/     # Calendar integration
│   │   └── integrations/   # AI, STT, TTS, Vision services
│   ├── requirements.txt
│   └── manage.py
└── frontend/
    ├── src/
    │   ├── pages/          # Next.js pages
    │   ├── components/     # React components
    │   └── styles/         # Global styles
    ├── package.json
    └── next.config.js
```

## 🎯 Usage

### Recruiter Flow

1. **Create Job**
   - Manual entry or AI generation from title
   - Configure interview settings

2. **Upload CVs**
   - Drag & drop PDF/DOCX files
   - Automatic parsing and skill extraction

3. **Generate Questions**
   - AI creates 12+ tailored questions
   - Edit and customize as needed

4. **Schedule Interview**
   - Choose chat or video mode
   - Set difficulty (auto/manual)
   - Send calendar invite

5. **Review Results**
   - View scores and insights
   - Access transcript and recordings
   - Export PDF report

### Candidate Flow

1. **Receive Invite**
   - Email with join link

2. **Device Check**
   - Mic and camera permissions
   - Consent for video analysis

3. **Join Interview**
   - AI introduces itself
   - Answer questions via voice/text

4. **Complete**
   - Thank you screen
   - Confirmation email

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/register/` - Register

### Jobs
- `GET /api/jobs/` - List jobs
- `POST /api/jobs/` - Create job
- `POST /api/jobs/generate_from_title/` - AI generate JD
- `GET /api/jobs/{id}/` - Job details

### Candidates
- `GET /api/candidates/` - List candidates
- `POST /api/candidates/upload_cv/` - Upload & parse CV
- `GET /api/candidates/{id}/` - Candidate profile

### Interviews
- `GET /api/interviews/` - List interviews
- `POST /api/interviews/` - Create interview
- `WS /ws/interview/{id}/` - Real-time interview session

### Reports
- `GET /api/reports/{id}/` - Get report
- `GET /api/reports/{id}/export/` - Export PDF

## 🧪 Testing

```bash
# Backend tests
python manage.py test

# Frontend tests
npm run test
```

## 🐳 Docker Deployment

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔐 Security Considerations

- All API keys stored in environment variables
- JWT authentication for API access
- CORS configured for frontend domain
- Video analysis requires explicit consent
- Recordings encrypted at rest

## 📊 Performance

- MongoDB for scalable NoSQL storage
- Redis for WebSocket and caching
- Celery for async processing
- WebRTC for peer-to-peer video

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is proprietary software. All rights reserved.

## 🆘 Support

For issues or questions:
- Create an issue on GitHub
- Email: support@interviewerai.com

## 🗺️ Roadmap

### Phase 1 (MVP) - ✅ Completed
- Job description management
- CV parsing
- Question generation
- Chat interviews
- Basic scoring

### Phase 2 - 🚧 In Progress
- Video AI interviews with voice
- Body language analysis
- Advanced scheduling
- Comprehensive reports

### Phase 3 - 📅 Planned
- Multi-language support
- Advanced analytics dashboard
- ATS integrations (Greenhouse, Lever)
- Mobile apps

## 🙏 Acknowledgments

- OpenAI for GPT-4
- Google Cloud for Speech services
- Azure for TTS
- MediaPipe for vision AI
- All open-source contributors

---

**Note**: Remember to configure all API keys before running the application. Check `.env.example` files for required variables.
