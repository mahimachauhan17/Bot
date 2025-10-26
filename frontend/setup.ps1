# Interviewer AI Frontend Setup Script
# Run this script to set up the frontend environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Interviewer AI - Frontend Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js version
Write-Host "Checking Node.js version..." -ForegroundColor Yellow
node --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Node.js is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check npm version
Write-Host "Checking npm version..." -ForegroundColor Yellow
npm --version

# Install dependencies
Write-Host ""
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

# Copy environment file
Write-Host ""
Write-Host "Setting up environment file..." -ForegroundColor Yellow
if (!(Test-Path .env.local)) {
    Copy-Item .env.local.example .env.local
    Write-Host "Created .env.local file" -ForegroundColor Green
} else {
    Write-Host ".env.local file already exists" -ForegroundColor Yellow
}

# Build the project
Write-Host ""
Write-Host "Building the project..." -ForegroundColor Yellow
npm run build

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure backend is running on http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "2. Start the development server:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "3. Access the application:" -ForegroundColor White
Write-Host "   http://localhost:3000" -ForegroundColor White
Write-Host ""
