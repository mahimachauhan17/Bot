# Master Setup Script for Interviewer AI Platform
# Run this to set up both backend and frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Interviewer AI - Complete Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
Write-Host "Python: " -NoNewline -ForegroundColor White
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Node.js: " -NoNewline -ForegroundColor White
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check MongoDB
Write-Host "MongoDB: " -NoNewline -ForegroundColor White
$mongoRunning = Get-Process mongod -ErrorAction SilentlyContinue
if ($mongoRunning) {
    Write-Host "✅ Running" -ForegroundColor Green
} else {
    Write-Host "⚠️  Not running. Please start MongoDB" -ForegroundColor Yellow
}

# Check Redis
Write-Host "Redis: " -NoNewline -ForegroundColor White
$redisRunning = Get-Process redis-server -ErrorAction SilentlyContinue
if ($redisRunning) {
    Write-Host "✅ Running" -ForegroundColor Green
} else {
    Write-Host "⚠️  Not running. Please start Redis" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Setup Backend
Set-Location backend
if (Test-Path setup.ps1) {
    .\setup.ps1
} else {
    Write-Host "Backend setup script not found!" -ForegroundColor Red
}
Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Setup Frontend
Set-Location frontend
if (Test-Path setup.ps1) {
    .\setup.ps1
} else {
    Write-Host "Frontend setup script not found!" -ForegroundColor Red
}
Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Important Configuration Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure API Keys in backend/.env:" -ForegroundColor White
Write-Host "   • OPENAI_API_KEY=sk-your-key" -ForegroundColor Gray
Write-Host "   • GOOGLE_CLOUD_CREDENTIALS_PATH=/path/to/credentials.json" -ForegroundColor Gray
Write-Host "   • AZURE_SPEECH_KEY=your-key" -ForegroundColor Gray
Write-Host "   • AZURE_SPEECH_REGION=your-region" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Create Django superuser:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 To Start the Application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Option 1 - Manual Start:" -ForegroundColor White
Write-Host "   Terminal 1: cd backend && python manage.py runserver" -ForegroundColor Gray
Write-Host "   Terminal 2: cd frontend && npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "Option 2 - Docker (if Docker installed):" -ForegroundColor White
Write-Host "   docker-compose up -d" -ForegroundColor Gray
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Yellow
Write-Host "   Frontend:  http://localhost:3000" -ForegroundColor Gray
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor Gray
Write-Host "   Admin:     http://localhost:8000/admin" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation: README.md" -ForegroundColor Yellow
Write-Host ""
