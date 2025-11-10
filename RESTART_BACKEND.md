# How to Restart Backend Server

## Quick Restart Steps

### Step 1: Stop the Current Server

**Option A: If running in a terminal window**
- Go to the terminal window where the backend is running
- Press `Ctrl+C` to stop the server

**Option B: Stop all Python processes**
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Step 2: Start the Server Again

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

Or using uvicorn directly:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Complete Restart Command (One Line)

```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force; cd backend; .\venv\Scripts\Activate.ps1; python main.py
```

## Verify Server is Running

After restarting, check if it's running:
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing
```

You should see: `{"status":"healthy"}`

## Troubleshooting

- **Port already in use**: Wait a few seconds after stopping, then restart
- **Module not found**: Make sure you're in the virtual environment (`.\venv\Scripts\Activate.ps1`)
- **Permission denied**: Run PowerShell as Administrator

