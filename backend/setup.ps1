# Interviewer AI Backend Setup Script
# Run this script to set up the backend environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Interviewer AI - Backend Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
Write-Host ""
Write-Host "Setting up environment file..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Created .env file. Please edit it with your API keys!" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Yellow
}

# Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Create superuser prompt
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your API keys:" -ForegroundColor White
Write-Host "   - OPENAI_API_KEY" -ForegroundColor White
Write-Host "   - GOOGLE_CLOUD_CREDENTIALS_PATH" -ForegroundColor White
Write-Host "   - AZURE_SPEECH_KEY" -ForegroundColor White
Write-Host ""
Write-Host "2. Create a superuser:" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor White
Write-Host ""
Write-Host "3. Start the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "4. Access the admin panel:" -ForegroundColor White
Write-Host "   http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
