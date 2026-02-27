# PGT TMS Project Cleanup Script
# This script organizes and removes unnecessary documentation files

Write-Host "🧹 Starting PGT TMS Project Cleanup..." -ForegroundColor Cyan

# Create archive folder for old documentation
$archiveFolder = "docs-archive"
if (-not (Test-Path $archiveFolder)) {
    New-Item -ItemType Directory -Path $archiveFolder | Out-Null
    Write-Host "✅ Created archive folder: $archiveFolder" -ForegroundColor Green
}

# Files to KEEP in root (essential documentation)
$keepFiles = @(
    "README.md",
    "DEPLOYMENT.md",
    "START-APP.ps1",
    "CPANEL-DEPLOYMENT-GUIDE.md",
    "START-DEPLOYMENT-HERE.md",
    "DEPLOYMENT-READY.md",
    "DEPLOYMENT-COMPLETE-PACKAGE.md",
    "SETTINGS-COMPLETE.md",
    "TEST-ENHANCED-REPORTS-NOW.md",
    "pgt_tms.db"
)

# Get all .md and .ps1 files in root
$allFiles = Get-ChildItem -Path . -File | Where-Object { 
    $_.Extension -in @('.md', '.ps1', '.txt') -and 
    $_.Name -notin $keepFiles 
}

Write-Host "`n📦 Moving old documentation files to archive..." -ForegroundColor Yellow

$movedCount = 0
foreach ($file in $allFiles) {
    try {
        Move-Item -Path $file.FullName -Destination $archiveFolder -Force
        $movedCount++
        Write-Host "  Moved: $($file.Name)" -ForegroundColor Gray
    } catch {
        Write-Host "  ⚠️  Could not move: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "`n✅ Moved $movedCount files to $archiveFolder" -ForegroundColor Green

# Clean up backend temporary files
Write-Host "`n🧹 Cleaning backend temporary files..." -ForegroundColor Yellow

$backendTempFiles = @(
    "backend/add_ceo_capital_table.py",
    "backend/add_ceo_capital_link_to_expenses.py",
    "backend/add_enhanced_report_endpoints.py",
    "backend/debug_login.py",
    "backend/find_sample_ids.py",
    "backend/add_staff_advance_ledger.py",
    "backend/add_office_expenses_table.py",
    "backend/set_office_expense_opening_balance.py",
    "backend/add_common_clients.py",
    "backend/add_common_vendors.py",
    "backend/add_fleet_vehicles.py",
    "backend/add_local_shifting_charges.py",
    "backend/recreate_cash_transactions.py",
    "backend/fix_payables_outstanding.py",
    "backend/fix_trip_status.py",
    "backend/migrate_complete_integration.py",
    "backend/migrate_enhancements.py"
)

$backendArchive = "backend/scripts-archive"
if (-not (Test-Path $backendArchive)) {
    New-Item -ItemType Directory -Path $backendArchive | Out-Null
}

$backendMovedCount = 0
foreach ($file in $backendTempFiles) {
    if (Test-Path $file) {
        try {
            $fileName = Split-Path $file -Leaf
            Move-Item -Path $file -Destination "$backendArchive/$fileName" -Force
            $backendMovedCount++
            Write-Host "  Moved: $fileName" -ForegroundColor Gray
        } catch {
            Write-Host "  ⚠️  Could not move: $file" -ForegroundColor Red
        }
    }
}

Write-Host "✅ Moved $backendMovedCount backend scripts to archive" -ForegroundColor Green

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=".PadRight(50, '=') -ForegroundColor Cyan
Write-Host "📊 CLEANUP SUMMARY" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=".PadRight(50, '=') -ForegroundColor Cyan

Write-Host "`n✅ Root documentation files moved: $movedCount" -ForegroundColor Green
Write-Host "✅ Backend scripts archived: $backendMovedCount" -ForegroundColor Green
Write-Host "`n📁 Archives created:" -ForegroundColor Yellow
Write-Host "   - $archiveFolder (root documentation)" -ForegroundColor Gray
Write-Host "   - $backendArchive (migration scripts)" -ForegroundColor Gray

Write-Host "`n📝 Essential files kept in root:" -ForegroundColor Yellow
foreach ($file in $keepFiles) {
    if (Test-Path $file) {
        Write-Host "   ✓ $file" -ForegroundColor Green
    }
}

Write-Host "`n🎯 Project is now clean and organized!" -ForegroundColor Cyan
Write-Host "   - All old docs are in: $archiveFolder" -ForegroundColor Gray
Write-Host "   - Migration scripts in: $backendArchive" -ForegroundColor Gray
Write-Host "   - Essential docs remain in root" -ForegroundColor Gray

Write-Host "`n✨ Cleanup complete!" -ForegroundColor Green
