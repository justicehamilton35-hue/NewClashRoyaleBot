import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class Card:
    """Represents a Clash Royale card"""
    name: str
    elixir_cost: int
    card_type: str  # troop, spell, building
    rarity: str  # common, rare, epic, legendary


@dataclass
class DetectedCard:
    """Represents a detected card in a frame"""
    card: Card
    confidence: float
    position: Tuple[int, int]
    player: str  # 'player' or 'opponent'
    timestamp: float


# Clash Royale card data
CARDS = {
    "knight": Card("Knight", 3, "troop", "common"),
    "archers": Card("Archers", 3, "troop", "common"),
    "goblins": Card("Goblins", 2, "troop", "common"),
    "giant": Card("Giant", 5, "troop", "rare"),
    "pekka": Card("P.E.K.K.A", 7, "troop", "epic"),
    "prince": Card("Prince", 5, "troop", "epic"),
    "wizard": Card("Wizard", 5, "troop", "rare"),
    "mini_pekka": Card("Mini P.E.K.K.A", 4, "troop", "rare"),
    "valkyrie": Card("Valkyrie", 4, "troop", "rare"),
    "skeleton_army": Card("Skeleton Army", 3, "troop", "epic"),
    "bomber": Card("Bomber", 2, "troop", "common"),
    "musketeer": Card("Musketeer", 4, "troop", "rare"),
    "baby_dragon": Card("Baby Dragon", 4, "troop", "epic"),
    "witch": Card("Witch", 5, "troop", "epic"),
    "barbarians": Card("Barbarians", 5, "troop", "common"),
    "golem": Card("Golem", 8, "troop", "epic"),
    "skeletons": Card("Skeletons", 1, "troop", "common"),
    "minions": Card("Minions", 3, "troop", "common"),
    "balloon": Card("Balloon", 5, "troop", "epic"),
    "hog_rider": Card("Hog Rider", 4, "troop", "rare"),
    "fireball": Card("Fireball", 4, "spell", "rare"),
    "arrows": Card("Arrows", 3, "spell", "common"),
    "zap": Card("Zap", 2, "spell", "common"),
    "lightning": Card("Lightning", 6, "spell", "epic"),
    "rage": Card("Rage", 2, "spell", "epic"),
    "freeze": Card("Freeze", 4, "spell", "epic"),
    "mirror": Card("Mirror", 1, "spell", "epic"),
    "rocket": Card("Rocket", 6, "spell", "rare"),
    "goblin_barrel": Card("Goblin Barrel", 3, "spell", "epic"),
    "cannon": Card("Cannon", 3, "building", "common"),
    "tesla": Card("Tesla", 4, "building", "common"),
    "inferno_tower": Card("Inferno Tower", 5, "building", "rare"),
    "bomb_tower": Card("Bomb Tower", 4, "building", "rare"),
    "barbarian_hut": Card("Barbarian Hut", 6, "building", "rare"),
    "elixir_collector": Card("Elixir Collector", 6, "building", "rare"),
}


class CardDetector:
    """Detect cards being played in Clash Royale gameplay"""

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize card detector

        Args:
            model_path: Path to trained YOLO model (optional)
        """
        self.model_path = model_path
        self.model = None

        # Try to load YOLO model if available
        if model_path and Path(model_path).exists():
            try:
                from ultralytics import YOLO
                self.model = YOLO(model_path)
                logger.info(f"Loaded YOLO model from {model_path}")
            except ImportError:
                logger.warning("ultralytics not installed, using fallback detection")
            except Exception as e:
                logger.warning(f"Could not load model: {e}, using fallback detection")

    def detect_cards_in_frame(
        self,
        frame: np.ndarray,
        timestamp: float
    ) -> List[DetectedCard]:
        """
        Detect cards being played in a frame

        Args:
            frame: Video frame
            timestamp: Frame timestamp

        Returns:
            List of detected cards
        """
        if self.model:
            return self._detect_with_yolo(frame, timestamp)
        else:
            return self._detect_with_template_matching(frame, timestamp)

    def _detect_with_yolo(
        self,
        frame: np.ndarray,
        timestamp: float
    ) -> List[DetectedCard]:
        """
        Detect cards using YOLO model

        Args:
            frame: Video frame
            timestamp: Frame timestamp

        Returns:
            List of detected cards
        """
        results = self.model(frame)

        detected_cards = []

        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Extract detection info
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                # Get card name from class ID
                card_name = result.names[class_id]

                if card_name in CARDS:
                    card = CARDS[card_name]

                    # Determine if player or opponent based on position
                    frame_height = frame.shape[0]
                    center_y = (y1 + y2) / 2
                    player = "player" if center_y > frame_height / 2 else "opponent"

                    detected_cards.append(DetectedCard(
                        card=card,
                        confidence=confidence,
                        position=(int((x1 + x2) / 2), int(center_y)),
                        player=player,
                        timestamp=timestamp
                    ))

        return detected_cards

    def _detect_with_template_matching(
        self,
        frame: np.ndarray,
        timestamp: float
    ) -> List[DetectedCard]:
        """
        Detect cards using template matching (fallback method)

        This is a simplified detection method for when YOLO model is not available.
        In production, you should use a trained YOLO model for better accuracy.

        Args:
            frame: Video frame
            timestamp: Frame timestamp

        Returns:
            List of detected cards (simulated for demo)
        """
        # This is a placeholder implementation
        # In a real implementation, you would:
        # 1. Extract card templates from the game
        # 2. Use template matching to find cards in frame
        # 3. Track card movements frame-to-frame

        detected_cards = []

        # For now, return empty list
        # In production, implement proper template matching or use YOLO

        logger.debug(f"Template matching detection at {timestamp}s (fallback mode)")

        return detected_cards

    def detect_placement(
        self,
        frame: np.ndarray,
        card: Card,
        timestamp: float
    ) -> Optional[Tuple[int, int]]:
        """
        Detect where a card was placed on the arena

        Args:
            frame: Video frame
            card: Card that was played
            timestamp: Frame timestamp

        Returns:
            (x, y) position on arena, or None if not detected
        """
        # This would analyze the frame to detect where the card appeared
        # For now, return None (placeholder)
        return None

    def get_elixir_count(self, frame: np.ndarray) -> int:
        """
        Extract elixir count from frame using OCR

        Args:
            frame: Video frame

        Returns:
            Current elixir count
        """
        # Extract elixir region
        height, width = frame.shape[:2]
        elixir_region = frame[
            int(height * 0.75):int(height * 0.85),
            int(width * 0.05):int(width * 0.15)
        ]

        # In production, use OCR (Tesseract) to read the number
        # For now, return placeholder
        return 5

    def get_tower_health(self, frame: np.ndarray, player: str) -> Dict[str, int]:
        """
        Extract tower health from frame

        Args:
            frame: Video frame
            player: 'player' or 'opponent'

        Returns:
            Dictionary with tower health values
        """
        # In production, use OCR or CV to detect tower health bars
        # For now, return placeholder
        return {
            "king_tower": 2534,
            "left_tower": 1512,
            "right_tower": 1512
        }
