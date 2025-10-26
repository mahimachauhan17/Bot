# Quick Start Guide

## Prerequisites Checklist

Before running the setup, ensure you have:

- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] MongoDB 5.0+ installed and running
- [ ] Redis 6.0+ installed and running
- [ ] Git installed (for version control)

## Quick Setup (Windows)

### 1. Run the Master Setup Script

Open PowerShell in the project root directory and run:

```powershell
.\setup.ps1
```

This will automatically:
- Check prerequisites
- Set up Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Create environment files
- Run database migrations
- Build the frontend

### 2. Configure API Keys

Edit `backend\.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_CLOUD_CREDENTIALS_PATH=C:\path\to\google-credentials.json
AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=eastus
```

### 3. Create Admin User

```powershell
cd backend
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 4. Start the Application

#### Option A: Manual Start (Development)

Open two PowerShell terminals:

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

#### Option B: Using Docker

```powershell
docker-compose up -d
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin

## API Keys Setup Guide

### OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key and add to `.env`

### Google Cloud Speech-to-Text

1. Go to https://console.cloud.google.com
2. Create a new project or select existing
3. Enable "Cloud Speech-to-Text API"
4. Create service account credentials
5. Download JSON key file
6. Add path to `.env`

### Azure Speech Services

1. Go to https://portal.azure.com
2. Create "Speech Services" resource
3. Get keys from "Keys and Endpoint"
4. Add key and region to `.env`

## Troubleshooting

### MongoDB Connection Error

Ensure MongoDB is running:
```powershell
# Check if MongoDB is running
Get-Process mongod

# Start MongoDB (if installed as service)
net start MongoDB
```

### Redis Connection Error

Ensure Redis is running:
```powershell
# Check if Redis is running
Get-Process redis-server

# Start Redis
redis-server
```

### Port Already in Use

If ports 3000 or 8000 are in use:

**Backend (port 8000):**
```powershell
python manage.py runserver 8001
```

**Frontend (port 3000):**
```powershell
# Edit package.json and change port in dev script
npm run dev -- -p 3001
```

### Python Virtual Environment Issues

If activation fails:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Next Steps

1. **Create Your First Job Description**
   - Go to http://localhost:3000/recruiter/dashboard
   - Click "Create Job"
   - Use AI generation or manual entry

2. **Upload a CV**
   - Click "Upload CV"
   - Upload PDF/DOCX file
   - Review parsed data

3. **Schedule an Interview**
   - Select job and candidate
   - Choose interview type (Chat/Video)
   - Set difficulty level
   - Send invitation

4. **Conduct Interview**
   - Candidate opens invite link
   - Complete device check
   - Start interview session

5. **Review Results**
   - View scores and insights
   - Access transcript
   - Export report

## Development Tips

### Running Tests

**Backend:**
```powershell
cd backend
python manage.py test
```

**Frontend:**
```powershell
cd frontend
npm run test
```

### Database Migrations

After modifying models:
```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Clearing Cache

```powershell
# Redis
redis-cli FLUSHALL

# Django cache
cd backend
python manage.py clearcache
```

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review backend/apps/*/models.py for data structures
- Check frontend/src/pages for UI components

## Production Deployment

For production deployment, refer to:
- `docker-compose.yml` for containerized deployment
- `ecosystem.config.js` for PM2 process management
- README.md for full deployment guide
