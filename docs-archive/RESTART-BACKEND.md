# How to Restart Backend Server

## The Issue
The cancelled trip amounts are still showing in totals because the backend server needs to be restarted to load the updated code.

## Solution: Restart the Backend

### Option 1: Using Command Line

1. **Stop the current backend server**:
   - Press `Ctrl+C` in the terminal where backend is running

2. **Start the backend server again**:
   ```bash
   cd backend
   python main.py
   ```
   OR if using uvicorn:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8002
   ```

### Option 2: If Running as Background Process

1. **Find the process**:
   ```bash
   netstat -ano | findstr :8002
   ```

2. **Kill the process** (replace PID with actual process ID):
   ```bash
   taskkill /PID <PID> /F
   ```

3. **Start backend again**:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8002
   ```

## What Will Happen After Restart

Once the backend restarts with the updated code:

### Dashboard Will Show:
- **Total Client Revenue**: Rs 480,000 (was Rs 980,000)
  - Excludes the Rs 500,000 from cancelled trip
  
- **Total Company Profit**: Rs 270,000 (was Rs 370,000)
  - Excludes the Rs 100,000 profit from cancelled trip

### Fleet Operations Page Will Show:
- **Total Client Revenue**: Rs 480,000
  - Only counts: Rs 400,000 + Rs 40,000 + Rs 40,000 = Rs 480,000
  - Excludes: Rs 500,000 (cancelled)

- **Total Company Profit**: Rs 270,000
  - Only counts: Rs 100,000 + Rs 10,000 + Rs 10,000 + Rs 250,000 - Rs 100,000 = Rs 270,000
  - Excludes: Rs 100,000 (cancelled trip profit)

## Verification Steps

After restarting:

1. **Refresh the Dashboard** (F5 or Ctrl+R)
2. **Check Total Client Revenue** - should be Rs 480,000
3. **Check Total Company Profit** - should be Rs 270,000
4. **Go to Fleet Operations page**
5. **Verify summary cards** - should match dashboard
6. **Cancelled trip should still appear in list** with ❌ Cancelled badge

## Why This Happens

Python/FastAPI servers cache the code in memory. When you update the code:
- The file changes on disk
- But the running server still uses the old code from memory
- Restarting loads the new code into memory

## Using --reload Flag (Recommended)

To avoid manual restarts in the future, always start backend with `--reload`:

```bash
uvicorn main:app --reload --port 8002
```

This automatically restarts the server when code changes are detected!

## Troubleshooting

### If amounts still don't update:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Check browser console for errors (F12)
4. Verify backend is actually restarted (check terminal for startup messages)

### If backend won't start:
1. Check if port 8002 is already in use
2. Check for syntax errors in Python files
3. Verify all dependencies are installed
4. Check backend terminal for error messages
