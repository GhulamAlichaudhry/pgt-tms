# Script to update backend URL for ngrok
param(
    [Parameter(Mandatory=$true)]
    [string]$BackendUrl
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PGT TMS - Backend URL Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate URL format
if ($BackendUrl -notmatch '^https?://') {
    Write-Host "ERROR: Invalid URL format. Must start with http:// or https://" -ForegroundColor Red
    Write-Host "Example: https://abc123.ngrok-free.app" -ForegroundColor Yellow
    exit 1
}

# Remove trailing slash if present
$BackendUrl = $BackendUrl.TrimEnd('/')

Write-Host "Updating backend URL to: $BackendUrl" -ForegroundColor Yellow
Write-Host ""

# Update .env file
$envPath = "frontend\.env"
$envContent = "# PGT TMS Frontend Configuration`n# Backend API URL configured for ngrok`n`nREACT_APP_API_URL=$BackendUrl"

Set-Content -Path $envPath -Value $envContent

Write-Host "✓ Updated $envPath" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Configuration Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Restart the frontend server (Ctrl+C in the terminal, then 'npm start')" -ForegroundColor White
Write-Host "2. Wait for compilation to complete" -ForegroundColor White
Write-Host "3. Share the frontend ngrok URL with your team" -ForegroundColor White
Write-Host ""

Write-Host "Frontend will now connect to: $BackendUrl" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
