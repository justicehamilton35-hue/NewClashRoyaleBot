# Windows Setup Guide - Clash Royale Analyzer

Complete guide for setting up the Clash Royale Analyzer on Windows.

## Prerequisites

Download and install these in order:

### 1. Python 3.10+
- Download: https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation
- Verify: Open Command Prompt and run `python --version`

### 2. Node.js 18+
- Download: https://nodejs.org/en/download/
- Install the LTS version
- Verify: Open Command Prompt and run `node --version` and `npm --version`

### 3. PostgreSQL 14+
- Download: https://www.postgresql.org/download/windows/
- Remember your password during installation
- Verify: Open Command Prompt and run `psql --version`

### 4. Redis (Windows)
- Download: https://github.com/microsoftarchive/redis/releases
- Get Redis-x64-3.0.504.msi
- Install and start the Redis service
- Or use WSL2: `wsl --install` then `sudo apt install redis-server`

---

## Quick Start with Docker (Recommended)

### 1. Install Docker Desktop
- Download: https://www.docker.com/products/docker-desktop/
- Install and restart your computer
- Start Docker Desktop (check system tray)

### 2. Run the Application
```powershell
# Open PowerShell in project folder
cd path\to\NewClashRoyaleBot

# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop when done
docker-compose down
```

### 3. Access
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Manual Setup (Without Docker)

### Step 1: Setup PostgreSQL Database

```powershell
# Open Command Prompt or PowerShell

# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE clash_royale_analyzer;

# Exit
\q
```

### Step 2: Start Redis

```powershell
# If installed as Windows service, it should auto-start
# Check if running:
redis-cli ping
# Should return: PONG

# If not running:
redis-server
```

### Step 3: Setup Backend

```powershell
# Open PowerShell
cd path\to\NewClashRoyaleBot\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env

# Edit .env file with Notepad
notepad .env
```

Update `.env` file:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/clash_royale_analyzer
REDIS_URL=redis://localhost:6379/0
DEBUG=True
```

```powershell
# Create directories
mkdir uploads
mkdir processed
mkdir models

# Start the backend server
python main.py
```

**Keep this terminal open!** Backend will run at http://localhost:8000

### Step 4: Setup Frontend

```powershell
# Open a NEW PowerShell window
cd path\to\NewClashRoyaleBot\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Keep this terminal open too!** Frontend will run at http://localhost:3000

### Step 5: Open the Application

Open your browser and go to: **http://localhost:3000**

---

## Using the Application

### Upload a Video

1. Go to http://localhost:3000
2. Click "Select Video File" or drag & drop your Clash Royale MP4
3. Wait for upload and processing (2-5 minutes)
4. View your analysis!

### What You'll See

- **Win Probability Graph**: Your chances throughout the game
- **Move Timeline**: Every card play evaluated
- **Move Quality**: Brilliant, Great, Good, Inaccuracy, Mistake, Blunder
- **Statistics**: Accuracy, move counts, average score
- **Recommendations**: Personalized tips to improve
- **Deck Info**: Your deck and opponent's deck

---

## Troubleshooting

### "Python not found"
```powershell
# Add Python to PATH manually
# System Properties → Environment Variables → Path → Add:
# C:\Users\YourName\AppData\Local\Programs\Python\Python310
# C:\Users\YourName\AppData\Local\Programs\Python\Python310\Scripts
```

### "psql not found"
```powershell
# Add PostgreSQL to PATH
# Add to System Path:
# C:\Program Files\PostgreSQL\14\bin
```

### Port Already in Use
```powershell
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual number)
taskkill /PID 1234 /F

# Same for port 8000 if needed
netstat -ano | findstr :8000
taskkill /PID 5678 /F
```

### Redis Connection Failed
```powershell
# If using Windows Redis:
# Go to Services (services.msc)
# Find "Redis" service
# Right-click → Start

# Or download memurai (Redis alternative for Windows):
# https://www.memurai.com/get-memurai
```

### Backend Import Errors
```powershell
# Make sure virtual environment is activated
cd backend
.\venv\Scripts\activate

# You should see (venv) in your prompt
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Database Connection Error
```powershell
# Check PostgreSQL is running
# Press Win+R, type "services.msc"
# Find "postgresql-x64-14" service
# Right-click → Start

# Test connection
psql -U postgres -d clash_royale_analyzer
```

---

## Running in the Future

### With Docker
```powershell
# Start
docker-compose up -d

# Stop
docker-compose down
```

### Manual Setup
```powershell
# Terminal 1: Backend
cd backend
.\venv\Scripts\activate
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Make sure PostgreSQL and Redis services are running
```

---

## Video Requirements

- **Format**: MP4, MOV, or AVI
- **Max Size**: 500MB (configurable in .env)
- **Content**: Clash Royale gameplay
- **Quality**: Higher resolution = better detection
- **Duration**: Any length (longer videos take more time to process)

---

## Performance Tips

- Close unnecessary programs during video processing
- Use SSD for faster file processing
- More RAM = faster video processing
- GPU helps but is not required

---

## Stopping the Application

### Docker
```powershell
docker-compose down
```

### Manual
- Press `Ctrl+C` in both PowerShell windows (backend and frontend)
- Close the terminals

---

## Getting Help

If you encounter issues:

1. Check the error message carefully
2. Make sure all prerequisites are installed
3. Verify services are running (PostgreSQL, Redis)
4. Check the logs in the terminal
5. Try the Docker method if manual setup fails

---

## Next Steps

1. Start the application
2. Upload your first Clash Royale gameplay video
3. Wait for analysis to complete
4. Review your moves and learn from mistakes
5. Apply recommendations in your next game!

Happy analyzing! 🏆
