# Quick Start Guide for Windows ⚡

Get the Clash Royale Analyzer running on Windows in just a few steps!

---

## 🚀 Method 1: Docker (Easiest - 2 minutes)

### Requirements
- Docker Desktop for Windows

### Steps

1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop/
   - Install and restart your computer
   - Start Docker Desktop (check system tray)

2. **Double-click: `start-windows.bat`**

   That's it! The script will start everything automatically.

3. **Open your browser**: http://localhost:3000

---

## 💻 Method 2: Manual Setup (15 minutes)

### Requirements
- Python 3.10+ → https://www.python.org/downloads/ ✅ Check "Add to PATH"
- Node.js 18+ → https://nodejs.org/
- PostgreSQL 14+ → https://www.postgresql.org/download/windows/
- Redis → https://github.com/microsoftarchive/redis/releases

### Steps

#### 1. Install Prerequisites
Install all 4 programs above (remember your PostgreSQL password!)

#### 2. Setup Database
```powershell
# Open Command Prompt
psql -U postgres
CREATE DATABASE clash_royale_analyzer;
\q
```

#### 3. Setup Backend
**Double-click: `setup-backend.bat`**
- This installs backend dependencies
- Edit the `.env` file with your PostgreSQL password when prompted

#### 4. Setup Frontend
**Double-click: `setup-frontend.bat`**
- This installs frontend dependencies (takes 2-3 minutes)

#### 5. Start the Application

**Open TWO Command Prompt windows:**

**Window 1** - Double-click: `start-backend.bat`
- Starts the backend server
- Wait for "Application startup complete"

**Window 2** - Double-click: `start-frontend.bat`
- Starts the frontend
- Browser will open automatically

**Go to**: http://localhost:3000

---

## 📹 Using the Analyzer

### Step 1: Upload Video
1. Click "Select Video File" or drag & drop
2. Choose your Clash Royale gameplay MP4
3. Click upload

### Step 2: Wait for Analysis
- Progress shown on screen (2-5 minutes)
- Don't close the browser!

### Step 3: View Results
You'll see:
- ✨ **Win Probability Graph** - Your chances over time
- 📊 **Move Timeline** - Every card evaluated
- 🎯 **Move Quality** - Brilliant, Great, Good, Mistake, Blunder
- 📈 **Statistics** - Accuracy, move counts
- 💡 **Recommendations** - Tips to improve
- 🃏 **Deck Analysis** - Your cards and opponent's

---

## 🔧 Common Issues

### "Python not found"
- Reinstall Python and CHECK "Add Python to PATH"

### "Port 3000 already in use"
```powershell
netstat -ano | findstr :3000
taskkill /PID [number] /F
```

### "Cannot connect to database"
- Make sure PostgreSQL service is running
- Check Services (Win+R → services.msc)
- Start "postgresql-x64-14"

### "Redis connection failed"
- Install Redis or use memurai: https://www.memurai.com/

---

## 🎯 File Reference

| File | Purpose |
|------|---------|
| `start-windows.bat` | Auto-start with Docker |
| `setup-backend.bat` | Setup backend (one-time) |
| `setup-frontend.bat` | Setup frontend (one-time) |
| `start-backend.bat` | Start backend server |
| `start-frontend.bat` | Start frontend |
| `stop-docker.bat` | Stop Docker services |

---

## 🛑 Stopping the Application

### Docker Method
**Double-click: `stop-docker.bat`**

### Manual Method
- Press `Ctrl+C` in both command prompt windows
- Close the windows

---

## 📖 More Help

- **Full Windows Guide**: See `WINDOWS_SETUP.md`
- **Complete Documentation**: See `SETUP.md`
- **Contributing**: See `CONTRIBUTING.md`

---

## 🎮 Ready to Analyze!

1. Start the application (choose Docker or Manual method)
2. Go to http://localhost:3000
3. Upload your Clash Royale MP4
4. Get AI-powered insights!
5. Improve your gameplay!

**First time?** Try with a short video (1-2 minutes) to see how it works!

🏆 Happy Gaming!
