# 🔑 API Keys Setup Guide

## Overview
This guide will help you get all the API keys needed for your Interviewer AI Agent platform.

---

## 1️⃣ OpenAI API Key (Required for AI Features)

### What it does:
- Generates job descriptions
- Creates interview questions
- Evaluates candidate answers
- Provides intelligent follow-up questions

### How to get it:

**Step 1: Create Account**
- Visit: https://platform.openai.com/
- Sign up with email or Google account
- Verify your email

**Step 2: Add Payment Method**
- Click your profile (top right) → **"Billing"**
- Add credit card (required for API access)
- Add initial credits ($5-10 recommended)

**Step 3: Generate API Key**
- Go to: https://platform.openai.com/api-keys
- Click **"+ Create new secret key"**
- Name it: `interview-bot`
- Copy the key (starts with `sk-proj-...` or `sk-...`)
- ⚠️ **IMPORTANT**: Save it now! You can't see it again

**Step 4: Add to .env**
```bash
# Open backend\.env and add:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Cost**: ~$0.03 per 1K tokens (GPT-4)
- Average interview: ~$0.50-1.00
- First-time users often get free credits

---

## 2️⃣ Google Cloud Speech-to-Text (For Voice Interviews)

### What it does:
- Converts candidate speech to text in real-time
- Enables voice-based interviews
- Transcribes interview audio

### How to get it:

**Step 1: Create Google Cloud Account**
- Visit: https://console.cloud.google.com/
- Sign up (includes $300 free credit for 90 days)
- No credit card required for trial

**Step 2: Create Project**
- Click **"Select a project"** (top left)
- Click **"NEW PROJECT"**
- Name: `interviewer-ai-bot`
- Click **"Create"**

**Step 3: Enable Speech-to-Text API**
- Go to: https://console.cloud.google.com/apis/library
- Search: **"Cloud Speech-to-Text API"**
- Click on it → Click **"ENABLE"**

**Step 4: Create Service Account**
- Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
- Click **"+ CREATE SERVICE ACCOUNT"**
- Name: `speech-service-account`
- Click **"Create and Continue"**
- Role: Select **"Project" → "Owner"** (or "Speech-to-Text Admin")
- Click **"Continue"** → **"Done"**

**Step 5: Generate Credentials JSON**
- Click on the service account you just created
- Go to **"KEYS"** tab
- Click **"ADD KEY"** → **"Create new key"**
- Choose **"JSON"**
- File downloads automatically (e.g., `interviewer-ai-bot-xxxxx.json`)

**Step 6: Save Credentials File**
```powershell
# Create credentials folder
New-Item -ItemType Directory -Path C:\Users\chauh\OneDrive\Desktop\Bot\backend\credentials

# Copy your downloaded JSON file to:
# C:\Users\chauh\OneDrive\Desktop\Bot\backend\credentials\google-credentials.json
```

**Step 7: Add to .env**
```bash
GOOGLE_CLOUD_CREDENTIALS_PATH=C:/Users/chauh/OneDrive/Desktop/Bot/backend/credentials/google-credentials.json
GOOGLE_CLOUD_PROJECT_ID=interviewer-ai-bot
```

**Cost**: $0.006 per 15 seconds
- First 60 minutes per month: **FREE**
- After that: ~$0.024 per minute

---

## 3️⃣ Azure Cognitive Services (For AI Voice/TTS)

### What it does:
- Converts AI interviewer text to speech
- Provides natural-sounding voice
- Powers the AI interviewer's voice

### How to get it:

**Step 1: Create Azure Account**
- Visit: https://portal.azure.com/
- Sign up (includes $200 free credit for 30 days)
- Requires credit card but won't charge without permission

**Step 2: Create Speech Resource**
- Click **"+ Create a resource"** (top left)
- Search: **"Speech"**
- Click **"Speech"** by Microsoft
- Click **"Create"**

**Step 3: Configure Resource**
- **Subscription**: Select your subscription
- **Resource group**: Create new → name it `interviewer-resources`
- **Region**: Choose closest (e.g., `East US`, `West Europe`)
- **Name**: `interview-speech-service`
- **Pricing tier**: 
  - **F0 (Free)**: 5 audio hours/month
  - **S0 (Standard)**: Pay as you go

**Step 4: Get Keys**
- After deployment, click **"Go to resource"**
- On left menu, click **"Keys and Endpoint"**
- Copy **KEY 1**
- Copy **Location/Region** (e.g., `eastus`)

**Step 5: Add to .env**
```bash
AZURE_SPEECH_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
AZURE_SPEECH_REGION=eastus
```

**Cost**: 
- Free tier: 5 audio hours/month
- Standard: ~$1 per 1 million characters (~16 hours of audio)

---

## 🆓 Testing Without API Keys

You can test the application without API keys! The system has **mock responses** built in:

### What works without keys:
✅ User interface
✅ Database operations
✅ Interview scheduling
✅ Candidate management
✅ Basic chat interface

### What needs API keys:
❌ AI-generated job descriptions
❌ AI question generation
❌ Answer evaluation
❌ Voice-to-text
❌ Text-to-speech

### Quick Start Without Keys:

1. **Leave API keys empty in .env**
2. **Run the application** (instructions below)
3. **You'll see placeholder responses** like:
   - "AI Service: This is a mock response. Please add your OpenAI API key."

---

## 📝 Final .env Configuration

Your `backend\.env` should look like this:

```bash
# Django Settings
SECRET_KEY=django-insecure-temp-key-for-development-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=interviewer_ai_db

# Redis
REDIS_URL=redis://localhost:6379/0

# ====== ADD YOUR API KEYS BELOW ======

# OpenAI API
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
OPENAI_MODEL=gpt-4-turbo-preview

# Google Cloud Speech-to-Text
GOOGLE_CLOUD_CREDENTIALS_PATH=C:/Users/chauh/OneDrive/Desktop/Bot/backend/credentials/google-credentials.json
GOOGLE_CLOUD_PROJECT_ID=interviewer-ai-bot

# Azure Speech Services
AZURE_SPEECH_KEY=YOUR_AZURE_KEY_HERE
AZURE_SPEECH_REGION=eastus

# Frontend
FRONTEND_URL=http://localhost:3000
```

---

## 🚀 Next Steps After Adding Keys

```powershell
# 1. Activate virtual environment
cd C:\Users\chauh\OneDrive\Desktop\Bot\backend
.\venv\Scripts\Activate.ps1

# 2. Run migrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Start backend
python manage.py runserver

# 5. Start frontend (new terminal)
cd C:\Users\chauh\OneDrive\Desktop\Bot\frontend
npm run dev
```

---

## 💰 Cost Summary

| Service | Free Tier | Typical Cost/Month |
|---------|-----------|-------------------|
| **OpenAI GPT-4** | - | $10-30 (light use) |
| **Google Speech-to-Text** | 60 min/month | $2-10 |
| **Azure TTS** | 5 hours/month | $1-5 |
| **MongoDB Atlas** | 512MB | $0 (local) |
| **Redis** | Local | $0 (local) |
| **Total** | | **$13-45/month** |

For **testing**: You can start with **$5-10** and test thoroughly.

---

## ⚠️ Important Security Notes

1. **Never commit .env file to Git** (already in .gitignore)
2. **Never share API keys publicly**
3. **Rotate keys if exposed**
4. **Use environment variables in production**
5. **Set up billing alerts** in each service

---

## 🆘 Troubleshooting

### "Invalid API Key" Error
- Check for extra spaces in .env file
- Ensure no quotes around the key
- Verify key is active in the provider's dashboard

### "Module not found" Error
- Run: `pip install -r requirements.txt`

### "Connection refused" Error
- Ensure MongoDB and Redis are running:
  ```powershell
  Get-Service | Where-Object {$_.DisplayName -like "*MongoDB*" -or $_.DisplayName -like "*Redis*"}
  ```

---

## 📚 Additional Resources

- **OpenAI API Docs**: https://platform.openai.com/docs
- **Google Cloud Speech**: https://cloud.google.com/speech-to-text/docs
- **Azure Speech**: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/

---

**Need help?** Check the main `README.md` or `QUICKSTART.md` files!
