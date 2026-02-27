# PGT TMS Project Cleanup Script
Write-Host "Starting PGT TMS Project Cleanup..." -ForegroundColor Cyan

# Create archive folder
$archiveFolder = "docs-archive"
if (-not (Test-Path $archiveFolder)) {
    New-Item -ItemType Directory -Path $archiveFolder | Out-Null
    Write-Host "Created archive folder: $archiveFolder" -ForegroundColor Green
}

# Files to KEEP
$keepFiles = @(
    "README.md",
    "README-FINAL.md",
    "DEPLOYMENT.md",
    "START-APP.ps1",
    "CPANEL-DEPLOYMENT-GUIDE.md",
    "START-DEPLOYMENT-HERE.md",
    "DEPLOYMENT-READY.md",
    "DEPLOYMENT-COMPLETE-PACKAGE.md",
    "SETTINGS-COMPLETE.md",
    "TEST-ENHANCED-REPORTS-NOW.md",
    "CLEANUP-NOW.ps1",
    "CLEANUP-PROJECT.ps1",
    "pgt_tms.db"
)

# Move old docs
$allFiles = Get-ChildItem -Path . -File | Where-Object { 
    $_.Extension -in @('.md', '.ps1', '.txt') -and 
    $_.Name -notin $keepFiles 
}

Write-Host "Moving old documentation files..." -ForegroundColor Yellow
$movedCount = 0
foreach ($file in $allFiles) {
    try {
        Move-Item -Path $file.FullName -Destination $archiveFolder -Force
        $movedCount++
    } catch {
        Write-Host "Could not move: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "Moved $movedCount files to archive" -ForegroundColor Green

# Clean backend temp files
Write-Host "Cleaning backend temporary files..." -ForegroundColor Yellow

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
        } catch {
            Write-Host "Could not move: $file" -ForegroundColor Red
        }
    }
}

Write-Host "Moved $backendMovedCount backend scripts" -ForegroundColor Green

# Summary
Write-Host "`nCLEANUP SUMMARY" -ForegroundColor Cyan
Write-Host "Root docs moved: $movedCount" -ForegroundColor Green
Write-Host "Backend scripts archived: $backendMovedCount" -ForegroundColor Green
Write-Host "`nArchives created:" -ForegroundColor Yellow
Write-Host "  - $archiveFolder" -ForegroundColor Gray
Write-Host "  - $backendArchive" -ForegroundColor Gray
Write-Host "`nCleanup complete!" -ForegroundColor Green
