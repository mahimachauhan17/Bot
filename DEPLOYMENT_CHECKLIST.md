# Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] All API keys configured in `.env` files
- [ ] MongoDB connection tested and working
- [ ] Redis connection tested and working
- [ ] All required Python packages installed
- [ ] All required Node packages installed

### 2. Backend Configuration
- [ ] `SECRET_KEY` changed from default
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Database migrations completed
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Superuser account created
- [ ] CORS settings configured for production frontend URL

### 3. Frontend Configuration
- [ ] `NEXT_PUBLIC_API_URL` points to production backend
- [ ] `NEXT_PUBLIC_WS_URL` points to production WebSocket
- [ ] Build completed successfully (`npm run build`)
- [ ] Environment variables set in hosting platform

### 4. External Services
- [ ] OpenAI API key is valid and has credits
- [ ] Google Cloud Speech-to-Text credentials configured
- [ ] Azure Speech Services credentials configured
- [ ] STUN/TURN servers configured for WebRTC
- [ ] Email service configured (for notifications)
- [ ] Calendar integration credentials (Google/Outlook)

### 5. Database
- [ ] MongoDB production instance set up
- [ ] Database backups configured
- [ ] Indexes created for performance
- [ ] Connection string secured (using env vars)

### 6. Security
- [ ] SSL/TLS certificates installed
- [ ] HTTPS enforced
- [ ] CSRF protection enabled
- [ ] XSS protection headers configured
- [ ] Rate limiting implemented
- [ ] File upload size limits set
- [ ] Sensitive data encrypted
- [ ] API authentication working

### 7. Performance
- [ ] CDN configured for static files
- [ ] Media files storage configured (S3/Azure Blob)
- [ ] Redis caching enabled
- [ ] Celery workers running
- [ ] Load balancer configured (if needed)
- [ ] Database query optimization done

### 8. Monitoring & Logging
- [ ] Error logging configured (Sentry/similar)
- [ ] Application monitoring set up
- [ ] Database monitoring enabled
- [ ] Server resource monitoring active
- [ ] Uptime monitoring configured
- [ ] Log rotation set up

### 9. Testing
- [ ] All backend tests passing
- [ ] All frontend tests passing
- [ ] End-to-end tests completed
- [ ] Load testing performed
- [ ] Security audit completed
- [ ] API endpoints tested
- [ ] WebSocket connections tested
- [ ] Video/audio functionality tested

### 10. Documentation
- [ ] API documentation updated
- [ ] Deployment runbook created
- [ ] Environment variables documented
- [ ] Backup/restore procedures documented
- [ ] Incident response plan created

---

## Production Environment Variables

### Backend (.env)
```env
# Production Settings
SECRET_KEY=<strong-random-secret-key>
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_NAME=interviewer_ai_production

# Redis
REDIS_URL=redis://production-redis:6379/0

# API Keys
OPENAI_API_KEY=sk-prod-...
GOOGLE_CLOUD_CREDENTIALS_PATH=/etc/secrets/google-credentials.json
AZURE_SPEECH_KEY=prod-key
AZURE_SPEECH_REGION=eastus

# Frontend
FRONTEND_URL=https://yourdomain.com

# Email
EMAIL_HOST=smtp.youremailprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=<secure-password>

# File Storage
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_STORAGE_BUCKET_NAME=interviewer-ai-media

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com/ws
NEXT_PUBLIC_STUN_SERVER=stun:stun.yourdomain.com:19302
NEXT_PUBLIC_TURN_SERVER=turn:turn.yourdomain.com:3478
NEXT_PUBLIC_TURN_USERNAME=<username>
NEXT_PUBLIC_TURN_PASSWORD=<password>
```

---

## Deployment Steps

### Option 1: Docker Deployment

```bash
# 1. Update docker-compose.yml for production
# 2. Build images
docker-compose build

# 3. Start services
docker-compose up -d

# 4. Run migrations
docker-compose exec backend python manage.py migrate

# 5. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 6. Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# 7. Check logs
docker-compose logs -f
```

### Option 2: Manual Deployment

#### Backend Deployment
```bash
# 1. Set up production server (Ubuntu example)
sudo apt update
sudo apt install python3.11 python3-pip nginx

# 2. Clone repository
git clone <your-repo>
cd Bot/backend

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 4. Set environment variables
cp .env.example .env
nano .env  # Edit with production values

# 5. Run migrations
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Start with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# 8. Set up systemd service (recommended)
sudo nano /etc/systemd/system/interviewer-ai.service
sudo systemctl enable interviewer-ai
sudo systemctl start interviewer-ai
```

#### Frontend Deployment
```bash
# 1. Build production bundle
cd Bot/frontend
npm install
npm run build

# 2. Start production server
npm run start

# Or deploy to Vercel/Netlify
vercel deploy --prod
```

### Option 3: Cloud Platform Deployment

#### AWS Deployment
- Backend: AWS Elastic Beanstalk or ECS
- Frontend: AWS Amplify or S3 + CloudFront
- Database: AWS DocumentDB (MongoDB compatible)
- Redis: AWS ElastiCache

#### Azure Deployment
- Backend: Azure App Service
- Frontend: Azure Static Web Apps
- Database: Azure Cosmos DB (MongoDB API)
- Redis: Azure Cache for Redis

#### Google Cloud Deployment
- Backend: Google Cloud Run or App Engine
- Frontend: Firebase Hosting
- Database: Google Cloud Firestore
- Redis: Google Cloud Memorystore

---

## Post-Deployment

### 1. Verification
- [ ] Homepage loads correctly
- [ ] Login/authentication works
- [ ] Dashboard displays data
- [ ] CV upload works
- [ ] Interview creation works
- [ ] WebSocket connections establish
- [ ] Video/audio works
- [ ] Reports generate correctly

### 2. Performance Testing
- [ ] Page load times acceptable
- [ ] API response times good
- [ ] WebSocket latency acceptable
- [ ] Video quality satisfactory
- [ ] No memory leaks

### 3. Monitoring Setup
- [ ] Error tracking active
- [ ] Uptime monitoring configured
- [ ] Performance metrics being collected
- [ ] Alerts configured for critical issues

### 4. Backup Configuration
- [ ] Database backups scheduled
- [ ] Media files backed up
- [ ] Configuration backed up
- [ ] Backup restoration tested

---

## Rollback Plan

If issues occur:

```bash
# 1. Stop current deployment
docker-compose down
# or
systemctl stop interviewer-ai

# 2. Restore previous version
git checkout <previous-tag>
docker-compose up -d
# or rebuild

# 3. Restore database if needed
mongorestore --uri="mongodb://..." <backup-directory>

# 4. Verify rollback
# Test critical functionality
```

---

## Maintenance Schedule

### Daily
- [ ] Check error logs
- [ ] Monitor uptime
- [ ] Review system resources

### Weekly
- [ ] Database backup verification
- [ ] Security updates check
- [ ] Performance review

### Monthly
- [ ] Full system backup
- [ ] Security audit
- [ ] Dependency updates
- [ ] User feedback review

---

## Support Contacts

- DevOps Lead: _______________
- Database Admin: _______________
- Security Team: _______________
- API Keys Owner: _______________
- Hosting Support: _______________

---

## Important URLs

- Production Frontend: https://_______________
- Production Backend: https://_______________
- Admin Panel: https://_______________/admin
- Monitoring Dashboard: https://_______________
- Error Tracking: https://_______________
- Status Page: https://_______________

---

**Note**: Complete this checklist thoroughly before deploying to production!
