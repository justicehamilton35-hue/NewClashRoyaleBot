# Setup Guide - Clash Royale Analyzer

This guide will help you set up and run the Clash Royale Analyzer on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **PostgreSQL 14+** ([Download](https://www.postgresql.org/download/))
- **Redis 7+** ([Download](https://redis.io/download))
- **Docker & Docker Compose** (Optional, for containerized setup)

## Quick Start with Docker (Recommended)

The easiest way to run the entire application is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd NewClashRoyaleBot

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Manual Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and configure your settings
# Make sure PostgreSQL and Redis are running

# Create necessary directories
mkdir -p uploads processed models

# Initialize database (optional - auto-created on first run)
# python -c "from app.models.database import init_db; init_db()"

# Start the backend server
python main.py
```

The backend API will be available at http://localhost:8000

### 2. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at http://localhost:3000

### 3. Database Setup

#### PostgreSQL

```bash
# Create database
createdb clash_royale_analyzer

# Or using psql:
psql -U postgres
CREATE DATABASE clash_royale_analyzer;
\q
```

#### Redis

```bash
# Start Redis server
redis-server

# Or on macOS with Homebrew:
brew services start redis

# Or on Linux with systemd:
sudo systemctl start redis
```

## Configuration

### Backend Configuration (.env)

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/clash_royale_analyzer

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# File Upload
MAX_UPLOAD_SIZE=524288000  # 500MB
UPLOAD_DIR=./uploads
PROCESSED_DIR=./processed

# ML Models
CARD_DETECTION_MODEL=./models/card_detector.pt
```

### Frontend Configuration

The frontend automatically proxies API requests to `http://localhost:8000` via Vite.

## Training the Card Detection Model

The card detection model uses YOLO v8. To train your own model:

### 1. Prepare Dataset

```bash
# Create dataset structure
models/
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
└── data.yaml
```

### 2. Collect Training Data

- Extract frames from Clash Royale gameplay videos
- Label cards using tools like [LabelImg](https://github.com/heartexlabs/labelImg) or [Roboflow](https://roboflow.com/)
- Export labels in YOLO format

### 3. Train Model

```python
from ultralytics import YOLO

# Load a pretrained YOLOv8 model
model = YOLO('yolov8n.pt')

# Train the model
results = model.train(
    data='models/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='clash_royale_card_detector'
)

# Save the model
model.save('models/card_detector.pt')
```

### 4. Test Model

```python
from ultralytics import YOLO

model = YOLO('models/card_detector.pt')

# Test on an image
results = model('test_image.jpg')
results[0].show()
```

## Usage

### 1. Upload a Video

1. Go to http://localhost:3000
2. Click "Select Video File" or drag & drop your gameplay MP4
3. Wait for the upload to complete

### 2. View Analysis

- The analysis starts automatically after upload
- Progress is shown in real-time
- Once complete, you'll see:
  - Win probability graph
  - Move-by-move analysis
  - Move quality classifications (Brilliant, Good, Mistake, Blunder)
  - Game statistics
  - Personalized recommendations
  - Deck information

### 3. Understanding the Analysis

#### Move Quality

- **Brilliant** ✨: Best possible move, exceptional play
- **Great**: Very good move
- **Good**: Solid move
- **Inaccuracy**: Suboptimal but acceptable
- **Mistake**: Clear error
- **Blunder** ⚠️: Major mistake that significantly impacts the game

#### Evaluation Score

Similar to chess "centipawns":
- Positive scores favor you
- Negative scores favor opponent
- Each point represents a small advantage

#### Win Probability

Shows your chances of winning at each moment:
- 50% = Even game
- Above 50% = You're winning
- Below 50% = You're losing

## Troubleshooting

### Backend Issues

#### Database Connection Error

```bash
# Check if PostgreSQL is running
pg_isready

# Check connection
psql -U postgres -d clash_royale_analyzer
```

#### Redis Connection Error

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

#### Import Errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

#### Port Already in Use

```bash
# Kill process on port 3000
# macOS/Linux:
lsof -ti:3000 | xargs kill

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

#### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Card Detection Not Working

If card detection isn't working:

1. The project uses a placeholder detection system by default
2. For production use, you need to train a YOLO model on Clash Royale cards
3. See "Training the Card Detection Model" section above
4. Place your trained model at `backend/models/card_detector.pt`

## Performance Tips

### Backend

- Use a GPU for faster video processing (requires CUDA)
- Adjust `FPS_SAMPLE_RATE` in config (lower = faster but less accurate)
- Use Redis for caching

### Frontend

- Use production build for deployment: `npm run build`
- Enable gzip compression on server
- Use CDN for static assets

## Production Deployment

### Backend

```bash
# Install production dependencies only
pip install -r requirements.txt --no-dev

# Use gunicorn instead of uvicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
# Build for production
npm run build

# Serve with a static file server
npm install -g serve
serve -s dist -p 3000
```

### Environment Variables

Update `.env` for production:
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Use production database credentials
- Set appropriate `MAX_UPLOAD_SIZE`

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues, questions, or contributions:
- Check existing issues on GitHub
- Create a new issue with detailed information
- Include logs and error messages

## Next Steps

1. Upload your first gameplay video
2. Review the analysis
3. Apply the recommendations to improve
4. Track your progress over multiple games
5. Share insights with friends!

Happy analyzing! 🏆
