import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class VideoFrame:
    frame_number: int
    timestamp: float
    image: np.ndarray


@dataclass
class VideoMetadata:
    fps: float
    total_frames: int
    duration: float
    width: int
    height: int
    resolution: Tuple[int, int]


class VideoProcessor:
    """Process Clash Royale gameplay videos frame by frame"""

    def __init__(self, sample_rate: int = 2):
        """
        Initialize video processor

        Args:
            sample_rate: Number of frames to process per second
        """
        self.sample_rate = sample_rate

    def extract_metadata(self, video_path: str) -> VideoMetadata:
        """Extract metadata from video file"""
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0

        cap.release()

        logger.info(f"Video metadata: {width}x{height}, {fps}fps, {duration:.2f}s")

        return VideoMetadata(
            fps=fps,
            total_frames=total_frames,
            duration=duration,
            width=width,
            height=height,
            resolution=(width, height)
        )

    def process_video(self, video_path: str) -> List[VideoFrame]:
        """
        Process video and extract frames at specified sample rate

        Args:
            video_path: Path to video file

        Returns:
            List of VideoFrame objects
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / self.sample_rate) if fps > 0 else 1

        frames = []
        frame_count = 0

        logger.info(f"Processing video at {self.sample_rate} fps (every {frame_interval} frames)")

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if frame_count % frame_interval == 0:
                timestamp = frame_count / fps if fps > 0 else 0

                frames.append(VideoFrame(
                    frame_number=frame_count,
                    timestamp=timestamp,
                    image=frame
                ))

            frame_count += 1

            if frame_count % 100 == 0:
                logger.debug(f"Processed {frame_count} frames...")

        cap.release()

        logger.info(f"Extracted {len(frames)} frames from {frame_count} total frames")

        return frames

    def extract_game_area(self, frame: np.ndarray) -> np.ndarray:
        """
        Extract the game playing area from frame (remove UI elements)

        Args:
            frame: Input frame

        Returns:
            Cropped frame with game area
        """
        height, width = frame.shape[:2]

        # Clash Royale game area is roughly centered
        # Remove top UI (elixir, cards) and bottom UI
        top_margin = int(height * 0.15)
        bottom_margin = int(height * 0.20)

        game_area = frame[top_margin:height - bottom_margin, :]

        return game_area

    def extract_card_region(self, frame: np.ndarray) -> np.ndarray:
        """
        Extract the card region from bottom of frame

        Args:
            frame: Input frame

        Returns:
            Cropped frame with card area
        """
        height, width = frame.shape[:2]

        # Cards are at the bottom of the screen
        card_region_start = int(height * 0.80)

        card_area = frame[card_region_start:, :]

        return card_area

    def extract_elixir_region(self, frame: np.ndarray) -> np.ndarray:
        """
        Extract the elixir counter region

        Args:
            frame: Input frame

        Returns:
            Cropped frame with elixir area
        """
        height, width = frame.shape[:2]

        # Elixir is typically shown near the bottom-left
        elixir_region = frame[
            int(height * 0.75):int(height * 0.85),
            int(width * 0.05):int(width * 0.15)
        ]

        return elixir_region

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for card detection

        Args:
            frame: Input frame

        Returns:
            Preprocessed frame
        """
        # Convert to RGB (OpenCV uses BGR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize if needed
        # resized = cv2.resize(rgb_frame, (1280, 720))

        return rgb_frame

    def save_frame(self, frame: np.ndarray, output_path: str):
        """Save frame to file"""
        cv2.imwrite(output_path, frame)
        logger.debug(f"Saved frame to {output_path}")
