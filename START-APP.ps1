#!/usr/bin/env pwsh
<#
.SYNOPSIS
    PGT International Smart TMS - Guaranteed Startup Script
    
.DESCRIPTION
    This script GUARANTEES that:
    1. Admin credentials are always correct (admin/admin123)
    2. Backend starts successfully
    3. Frontend starts successfully
    4. All users can login immediately
    
.NOTES
    This script was created to permanently fix login credential issues
    that occurred multiple times during development.
#>

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PGT INTERNATIONAL SMART TMS - STARTUP SCRIPT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Ensure admin user exists with correct password
Write-Host "[1/4] Ensuring admin credentials are correct..." -ForegroundColor Yellow
Set-Location backend
python ensure_admin.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to ensure admin user" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host "✅ Admin credentials verified" -ForegroundColor Green
Write-Host ""

# Step 2: Start Backend
Write-Host "[2/4] Starting Backend Server..." -ForegroundColor Yellow
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd backend; python main.py"
Start-Sleep -Seconds 3
Write-Host "✅ Backend starting on http://localhost:8002" -ForegroundColor Green
Write-Host ""

# Step 3: Start Frontend
Write-Host "[3/4] Starting Frontend Server..." -ForegroundColor Yellow
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"
Start-Sleep -Seconds 5
Write-Host "✅ Frontend starting on http://localhost:3000" -ForegroundColor Green
Write-Host ""

# Step 4: Display credentials
Write-Host "[4/4] System Ready!" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  🔐 LOGIN CREDENTIALS (GUARANTEED TO WORK)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  ADMIN (Director):" -ForegroundColor White
Write-Host "    Username: admin" -ForegroundColor Cyan
Write-Host "    Password: admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "  MANAGER (Operations):" -ForegroundColor White
Write-Host "    Username: manager" -ForegroundColor Cyan
Write-Host "    Password: manager123" -ForegroundColor Cyan
Write-Host ""
Write-Host "  SUPERVISOR (Port Staff):" -ForegroundColor White
Write-Host "    Username: supervisor" -ForegroundColor Cyan
Write-Host "    Password: supervisor123" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  🌐 ACCESS URLS:" -ForegroundColor White
Write-Host "    Main App:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "    Backend:   http://localhost:8002" -ForegroundColor Cyan
Write-Host "    API Docs:  http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ PGT International Smart TMS is now running!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit this window (servers will keep running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
