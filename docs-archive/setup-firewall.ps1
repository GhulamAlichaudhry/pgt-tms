# PGT TMS - Firewall Setup Script
# Run this as Administrator to allow network access

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PGT TMS - Firewall Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Adding firewall rules..." -ForegroundColor Yellow
Write-Host ""

# Remove existing rules if they exist
Write-Host "Removing old rules (if any)..." -ForegroundColor Gray
Remove-NetFirewallRule -DisplayName "PGT TMS Frontend" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "PGT TMS Backend" -ErrorAction SilentlyContinue

# Add Frontend rule (Port 3000)
Write-Host "Adding Frontend rule (Port 3000)..." -ForegroundColor Green
New-NetFirewallRule -DisplayName "PGT TMS Frontend" `
    -Direction Inbound `
    -LocalPort 3000 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any `
    -Description "Allow access to PGT TMS Frontend (React)" | Out-Null

# Add Backend rule (Port 8000)
Write-Host "Adding Backend rule (Port 8000)..." -ForegroundColor Green
New-NetFirewallRule -DisplayName "PGT TMS Backend" `
    -Direction Inbound `
    -LocalPort 8000 `
    -Protocol TCP `
    -Action Allow `
    -Profile Any `
    -Description "Allow access to PGT TMS Backend (FastAPI)" | Out-Null

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Firewall Configuration Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Get network information
Write-Host "Your Network Information:" -ForegroundColor Cyan
Write-Host "------------------------" -ForegroundColor Cyan
$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.*" }

foreach ($ip in $ipAddresses) {
    $adapter = Get-NetAdapter | Where-Object { $_.ifIndex -eq $ip.InterfaceIndex }
    Write-Host "Interface: $($adapter.Name)" -ForegroundColor Yellow
    Write-Host "IP Address: $($ip.IPAddress)" -ForegroundColor White
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Share These URLs with Your Team:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Show the most likely IP (usually the last one that's not a virtual adapter)
$mainIP = ($ipAddresses | Where-Object { $_.PrefixOrigin -eq "Dhcp" -or $_.PrefixOrigin -eq "Manual" } | Select-Object -Last 1).IPAddress

if ($mainIP) {
    Write-Host "Frontend URL: http://$mainIP:3000" -ForegroundColor Green
    Write-Host "Backend URL:  http://$mainIP:8000" -ForegroundColor Green
} else {
    Write-Host "Frontend URL: http://YOUR_IP:3000" -ForegroundColor Green
    Write-Host "Backend URL:  http://YOUR_IP:8000" -ForegroundColor Green
    Write-Host ""
    Write-Host "Replace YOUR_IP with one of the IP addresses shown above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Make sure both servers are running:" -ForegroundColor White
Write-Host "   - Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "   - Backend:  http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Share the URLs above with your team" -ForegroundColor White
Write-Host ""
Write-Host "3. Team members should be on the same network" -ForegroundColor White
Write-Host ""
Write-Host "4. If it doesn't work, check:" -ForegroundColor White
Write-Host "   - Both servers are running" -ForegroundColor Gray
Write-Host "   - Team is on same WiFi/Network" -ForegroundColor Gray
Write-Host "   - Try different IP address from the list above" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"
