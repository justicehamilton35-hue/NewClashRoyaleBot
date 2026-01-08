# Clash Royale Gameplay Analyzer

A comprehensive gameplay analyzer for Clash Royale, inspired by Stockfish for chess. Upload your gameplay videos and get detailed AI-powered analysis including optimal moves, blunders, brilliant plays, win probability over time, and personalized playstyle recommendations.

## Features

- 🎥 **Video Upload & Processing**: Upload MP4 gameplay videos for analysis
- 🃏 **Card Detection**: AI-powered detection of all cards played by both players
- 🧠 **Move Analysis**: Stockfish-style evaluation of every move (Brilliant, Good, Inaccurate, Mistake, Blunder)
- 📊 **Win Probability**: Real-time win % calculation throughout the game
- 🎮 **Replay System**: Watch your game with overlaid analysis and annotations
- 📈 **Timeline View**: See what should have been played at each moment
- 🎯 **Playstyle Analysis**: Get personalized recommendations based on your gameplay
- 🌐 **Chess.com-style Interface**: Clean, intuitive web interface

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **OpenCV**: Video processing and frame extraction
- **YOLO/TensorFlow**: Card detection and recognition
- **PostgreSQL**: Game and analysis storage
- **Redis**: Caching and job queue

### Frontend
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Styling
- **Recharts**: Win probability graphs
- **Video.js**: Video playback

### AI Engine
- **Game State Analyzer**: Tracks elixir, cards, towers
- **Move Evaluator**: Evaluates placement quality
- **Win Probability Calculator**: Monte Carlo simulations
- **Playstyle Classifier**: Identifies play patterns

## Project Structure

```
NewClashRoyaleBot/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core config and settings
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   │   ├── video_processor.py
│   │   │   ├── card_detector.py
│   │   │   ├── game_analyzer.py
│   │   │   └── move_evaluator.py
│   │   └── ml/               # ML models
│   │       ├── card_detection/
│   │       └── game_engine/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # API services
│   │   └── types/            # TypeScript types
│   ├── package.json
│   └── public/
├── models/                   # Trained ML models
├── docker-compose.yml
└── README.md
```

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Database Setup

```bash
# Create PostgreSQL database
createdb clash_royale_analyzer

# Run migrations
cd backend
alembic upgrade head
```

## Running the Application

### Development Mode

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Redis (if not running as service)
redis-server
```

Access the application at `http://localhost:3000`

## Usage

1. **Upload Video**: Click "Upload Gameplay" and select your MP4 file
2. **Processing**: The AI will analyze your video (takes 2-5 minutes depending on length)
3. **Review Analysis**:
   - View win probability graph
   - See move classifications (brilliant/blunder)
   - Watch replay with annotations
   - Read playstyle recommendations
4. **Improve**: Apply the insights to your gameplay!

## How It Works

### Card Detection
Uses YOLO v8 trained on Clash Royale card sprites to detect cards being played in real-time from video frames.

### Move Evaluation
Evaluates each card placement based on:
- Elixir efficiency
- Defensive/offensive value
- Counter-play potential
- Tower damage optimization
- Synergy with existing cards

### Win Probability
Calculates win % using:
- Current tower HP
- Elixir advantage
- Card cycle position
- Time remaining
- Historical game data

### Playstyle Analysis
Identifies patterns like:
- Aggressive (pressure-focused)
- Control (defensive counter-push)
- Cycle (fast cycle cards)
- Beatdown (heavy tank pushes)
- Chip (spell damage focused)

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Multi-language support
- [ ] Live streaming analysis
- [ ] Deck recommendation system
- [ ] Tournament mode with multiple games
- [ ] Mobile app
- [ ] Community sharing and leaderboards

## Credits

Inspired by Stockfish chess engine and chess.com's analysis interface.
