from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
from pathlib import Path

from app.core.config import settings
from app.api import analysis, games, health
from app.services.video_processor import VideoProcessor
from app.services.card_detector import CardDetector
from app.services.game_analyzer import GameAnalyzer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    # Create necessary directories
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.PROCESSED_DIR).mkdir(parents=True, exist_ok=True)

    # Initialize ML models
    app.state.card_detector = CardDetector(settings.CARD_DETECTION_MODEL)
    app.state.game_analyzer = GameAnalyzer()

    print("🚀 Clash Royale Analyzer API Started")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    print(f"🎮 Card detection model loaded")

    yield

    # Cleanup
    print("👋 Shutting down...")


app = FastAPI(
    title="Clash Royale Analyzer API",
    description="AI-powered Clash Royale gameplay analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(games.router, prefix="/api/games", tags=["games"])

# Serve uploaded files
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.get("/")
async def root():
    return {
        "message": "Clash Royale Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
