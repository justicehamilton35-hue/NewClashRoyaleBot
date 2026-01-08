from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from typing import Optional
import uuid
import os
from pathlib import Path
import logging

from app.core.config import settings
from app.services.video_processor import VideoProcessor
from app.services.card_detector import CardDetector
from app.services.game_analyzer import GameAnalyzer

router = APIRouter()
logger = logging.getLogger(__name__)

# Store analysis results in memory (in production, use Redis or database)
analysis_jobs = {}


@router.post("/upload")
async def upload_video(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload gameplay video for analysis

    Args:
        file: MP4 video file

    Returns:
        Job ID for tracking analysis progress
    """
    # Validate file type
    if not file.filename.endswith(('.mp4', '.mov', '.avi')):
        raise HTTPException(
            status_code=400,
            detail="Only video files (mp4, mov, avi) are supported"
        )

    # Generate unique job ID
    job_id = str(uuid.uuid4())

    # Save uploaded file
    upload_path = Path(settings.UPLOAD_DIR) / f"{job_id}_{file.filename}"

    try:
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"Uploaded video: {upload_path}")

        # Initialize job status
        analysis_jobs[job_id] = {
            "status": "processing",
            "progress": 0,
            "video_path": str(upload_path),
            "filename": file.filename
        }

        # Start analysis in background
        logger.info(f"Adding background task for job {job_id}")
        background_tasks.add_task(
            process_video_analysis,
            job_id,
            str(upload_path),
            request.app.state.card_detector,
            request.app.state.game_analyzer
        )
        logger.info(f"Background task added for job {job_id}")

        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Video uploaded successfully, analysis started"
        }

    except Exception as e:
        logger.error(f"Error uploading video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}")
async def get_analysis_status(job_id: str):
    """
    Get analysis job status

    Args:
        job_id: Job ID from upload

    Returns:
        Job status and progress
    """
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return analysis_jobs[job_id]


@router.get("/result/{job_id}")
async def get_analysis_result(job_id: str):
    """
    Get complete analysis result

    Args:
        job_id: Job ID from upload

    Returns:
        Complete game analysis
    """
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = analysis_jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Analysis not completed yet (status: {job['status']})"
        )

    return job["analysis"]


def process_video_analysis(
    job_id: str,
    video_path: str,
    card_detector: CardDetector,
    game_analyzer: GameAnalyzer
):
    """
    Process video and perform analysis (background task)

    Args:
        job_id: Job ID
        video_path: Path to uploaded video
        card_detector: Card detection service
        game_analyzer: Game analysis service
    """
    try:
        logger.info(f"Starting analysis for job {job_id}")

        # Update status
        analysis_jobs[job_id]["status"] = "processing"
        analysis_jobs[job_id]["progress"] = 10

        # Initialize video processor
        video_processor = VideoProcessor(sample_rate=settings.FPS_SAMPLE_RATE)

        # Extract video metadata
        metadata = video_processor.extract_metadata(video_path)
        logger.info(f"Video metadata: {metadata}")

        analysis_jobs[job_id]["progress"] = 20

        # Process video frames
        frames = video_processor.process_video(video_path)
        logger.info(f"Extracted {len(frames)} frames")

        analysis_jobs[job_id]["progress"] = 40

        # Detect cards in frames
        detected_cards = []
        for i, frame in enumerate(frames):
            preprocessed = video_processor.preprocess_frame(frame.image)
            cards = card_detector.detect_cards_in_frame(preprocessed, frame.timestamp)
            detected_cards.extend(cards)

            # Update progress
            progress = 40 + (i / len(frames)) * 30
            analysis_jobs[job_id]["progress"] = int(progress)

        logger.info(f"Detected {len(detected_cards)} cards")

        analysis_jobs[job_id]["progress"] = 70

        # Analyze game
        analysis = game_analyzer.analyze_game(detected_cards, metadata.duration)
        logger.info("Analysis complete")

        analysis_jobs[job_id]["progress"] = 90

        # Convert analysis to JSON-serializable format
        result = {
            "game_id": analysis.game_id,
            "duration": analysis.duration,
            "winner": analysis.winner,
            "video_metadata": {
                "fps": metadata.fps,
                "resolution": metadata.resolution,
                "total_frames": metadata.total_frames
            },
            "player_deck": [
                {"name": c.name, "elixir": c.elixir_cost, "type": c.card_type}
                for c in analysis.player_deck
            ],
            "opponent_deck": [
                {"name": c.name, "elixir": c.elixir_cost, "type": c.card_type}
                for c in analysis.opponent_deck
            ],
            "moves": [
                {
                    "timestamp": m.timestamp,
                    "player": m.player,
                    "card": m.card.name,
                    "elixir_cost": m.card.elixir_cost,
                    "position": m.position
                }
                for m in analysis.moves
            ],
            "move_evaluations": [
                {
                    "timestamp": e.move.timestamp,
                    "card": e.move.card.name,
                    "player": e.move.player,
                    "quality": e.quality.value,
                    "score": e.evaluation_score,
                    "reasoning": e.reasoning,
                    "factors": e.key_factors
                }
                for e in analysis.move_evaluations
            ],
            "win_probability_timeline": [
                {"timestamp": t, "win_probability": p}
                for t, p in analysis.win_probability_timeline
            ],
            "playstyle": analysis.player_playstyle.value,
            "key_moments": [
                {"timestamp": t, "description": d}
                for t, d in analysis.key_moments
            ],
            "statistics": analysis.statistics,
            "recommendations": analysis.recommendations
        }

        # Save result
        analysis_jobs[job_id]["status"] = "completed"
        analysis_jobs[job_id]["progress"] = 100
        analysis_jobs[job_id]["analysis"] = result

        logger.info(f"Analysis completed for job {job_id}")

    except Exception as e:
        logger.error(f"Error processing video: {e}", exc_info=True)
        analysis_jobs[job_id]["status"] = "failed"
        analysis_jobs[job_id]["error"] = str(e)
