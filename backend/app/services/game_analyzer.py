from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import numpy as np

from .card_detector import Card, DetectedCard

logger = logging.getLogger(__name__)


class MoveQuality(Enum):
    """Move quality classification (like Stockfish)"""
    BRILLIANT = "brilliant"  # Best move, exceptional play
    GREAT = "great"  # Very good move
    GOOD = "good"  # Solid move
    INACCURACY = "inaccuracy"  # Suboptimal but not terrible
    MISTAKE = "mistake"  # Clear error
    BLUNDER = "blunder"  # Major mistake, game-changing


class Playstyle(Enum):
    """Player playstyle classifications"""
    AGGRESSIVE = "aggressive"
    CONTROL = "control"
    CYCLE = "cycle"
    BEATDOWN = "beatdown"
    CHIP = "chip"
    DEFENSIVE = "defensive"


@dataclass
class GameState:
    """Represents the current state of the game"""
    timestamp: float
    player_elixir: int
    opponent_elixir: int
    player_towers: Dict[str, int]
    opponent_towers: Dict[str, int]
    player_cards_in_hand: List[Card]
    opponent_cards_in_hand: List[Card]
    cards_on_field: List[Tuple[Card, str, Tuple[int, int]]]  # (card, player, position)
    player_card_cycle: List[Card]
    opponent_card_cycle: List[Card]


@dataclass
class Move:
    """Represents a card play"""
    timestamp: float
    player: str
    card: Card
    position: Tuple[int, int]
    elixir_before: int
    elixir_after: int


@dataclass
class MoveEvaluation:
    """Evaluation of a move"""
    move: Move
    quality: MoveQuality
    evaluation_score: float  # -100 to +100 (like centipawns in chess)
    alternative_moves: List[Tuple[Move, float]]  # Better moves and their scores
    reasoning: str
    key_factors: List[str]


@dataclass
class GameAnalysis:
    """Complete analysis of a game"""
    game_id: str
    duration: float
    winner: Optional[str]
    player_deck: List[Card]
    opponent_deck: List[Card]
    moves: List[Move]
    move_evaluations: List[MoveEvaluation]
    win_probability_timeline: List[Tuple[float, float]]  # (timestamp, win_prob)
    player_playstyle: Playstyle
    key_moments: List[Tuple[float, str]]  # (timestamp, description)
    statistics: Dict[str, any]
    recommendations: List[str]


class GameAnalyzer:
    """Analyze Clash Royale gameplay like Stockfish analyzes chess"""

    def __init__(self):
        self.elixir_regen_rate = 1.0  # per second
        self.max_elixir = 10
        self.overtime_elixir_rate = 2.0

    def analyze_game(
        self,
        detected_cards: List[DetectedCard],
        video_duration: float
    ) -> GameAnalysis:
        """
        Analyze complete game

        Args:
            detected_cards: All detected cards from video
            video_duration: Total video duration

        Returns:
            Complete game analysis
        """
        logger.info("Starting game analysis...")

        # Build game timeline
        moves = self._build_move_timeline(detected_cards)

        # Evaluate each move
        move_evaluations = []
        game_states = self._reconstruct_game_states(moves)

        for i, move in enumerate(moves):
            if i < len(game_states):
                evaluation = self._evaluate_move(move, game_states[i])
                move_evaluations.append(evaluation)

        # Calculate win probability over time
        win_prob_timeline = self._calculate_win_probability_timeline(game_states)

        # Determine playstyle
        playstyle = self._determine_playstyle(moves, move_evaluations)

        # Find key moments
        key_moments = self._find_key_moments(move_evaluations, win_prob_timeline)

        # Generate statistics
        statistics = self._calculate_statistics(moves, move_evaluations)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            moves, move_evaluations, playstyle, statistics
        )

        # Determine winner (simplified - based on final tower health)
        winner = self._determine_winner(game_states)

        # Extract decks
        player_deck = list(set(m.card for m in moves if m.player == "player"))
        opponent_deck = list(set(m.card for m in moves if m.player == "opponent"))

        return GameAnalysis(
            game_id="game_1",
            duration=video_duration,
            winner=winner,
            player_deck=player_deck,
            opponent_deck=opponent_deck,
            moves=moves,
            move_evaluations=move_evaluations,
            win_probability_timeline=win_prob_timeline,
            player_playstyle=playstyle,
            key_moments=key_moments,
            statistics=statistics,
            recommendations=recommendations
        )

    def _build_move_timeline(self, detected_cards: List[DetectedCard]) -> List[Move]:
        """Build chronological list of moves from detected cards"""
        moves = []

        for detected in detected_cards:
            move = Move(
                timestamp=detected.timestamp,
                player=detected.player,
                card=detected.card,
                position=detected.position,
                elixir_before=5,  # Placeholder
                elixir_after=5 - detected.card.elixir_cost
            )
            moves.append(move)

        moves.sort(key=lambda m: m.timestamp)

        return moves

    def _reconstruct_game_states(self, moves: List[Move]) -> List[GameState]:
        """Reconstruct game state at each move"""
        states = []

        # Initialize starting state
        current_state = GameState(
            timestamp=0.0,
            player_elixir=5,
            opponent_elixir=5,
            player_towers={"king": 2534, "left": 1512, "right": 1512},
            opponent_towers={"king": 2534, "left": 1512, "right": 1512},
            player_cards_in_hand=[],
            opponent_cards_in_hand=[],
            cards_on_field=[],
            player_card_cycle=[],
            opponent_card_cycle=[]
        )

        for move in moves:
            # Update elixir based on time passed
            if states:
                time_diff = move.timestamp - states[-1].timestamp
                current_state.player_elixir = min(
                    self.max_elixir,
                    current_state.player_elixir + time_diff * self.elixir_regen_rate
                )
                current_state.opponent_elixir = min(
                    self.max_elixir,
                    current_state.opponent_elixir + time_diff * self.elixir_regen_rate
                )

            # Apply move
            if move.player == "player":
                current_state.player_elixir -= move.card.elixir_cost
            else:
                current_state.opponent_elixir -= move.card.elixir_cost

            current_state.timestamp = move.timestamp

            # Add card to field
            current_state.cards_on_field.append(
                (move.card, move.player, move.position)
            )

            states.append(current_state)

        return states

    def _evaluate_move(self, move: Move, game_state: GameState) -> MoveEvaluation:
        """
        Evaluate a single move (like Stockfish evaluates chess moves)

        This is the core AI evaluation engine
        """
        # Calculate evaluation score based on multiple factors
        score = 0.0
        factors = []

        # Factor 1: Elixir efficiency
        elixir_score = self._evaluate_elixir_efficiency(move, game_state)
        score += elixir_score
        if abs(elixir_score) > 10:
            factors.append(f"Elixir efficiency: {elixir_score:+.1f}")

        # Factor 2: Defensive value
        defensive_score = self._evaluate_defensive_value(move, game_state)
        score += defensive_score
        if abs(defensive_score) > 10:
            factors.append(f"Defensive value: {defensive_score:+.1f}")

        # Factor 3: Offensive threat
        offensive_score = self._evaluate_offensive_threat(move, game_state)
        score += offensive_score
        if abs(offensive_score) > 10:
            factors.append(f"Offensive pressure: {offensive_score:+.1f}")

        # Factor 4: Card synergy
        synergy_score = self._evaluate_synergy(move, game_state)
        score += synergy_score
        if abs(synergy_score) > 10:
            factors.append(f"Card synergy: {synergy_score:+.1f}")

        # Factor 5: Timing
        timing_score = self._evaluate_timing(move, game_state)
        score += timing_score
        if abs(timing_score) > 10:
            factors.append(f"Timing: {timing_score:+.1f}")

        # Determine move quality based on score
        quality = self._classify_move_quality(score)

        # Generate alternative moves (what should have been played)
        alternatives = self._generate_alternatives(move, game_state)

        # Generate reasoning
        reasoning = self._generate_reasoning(move, quality, factors)

        return MoveEvaluation(
            move=move,
            quality=quality,
            evaluation_score=score,
            alternative_moves=alternatives,
            reasoning=reasoning,
            key_factors=factors
        )

    def _evaluate_elixir_efficiency(self, move: Move, state: GameState) -> float:
        """Evaluate elixir efficiency of the move"""
        # Good elixir trades are positive, bad trades are negative
        score = 0.0

        # Don't overcommit elixir
        if move.player == "player":
            remaining = state.player_elixir - move.card.elixir_cost
            if remaining < 2:
                score -= 15  # Risky to go too low on elixir

        # Playing expensive cards when low on elixir is bad
        if move.card.elixir_cost >= 6 and state.player_elixir < 8:
            score -= 10

        return score

    def _evaluate_defensive_value(self, move: Move, state: GameState) -> float:
        """Evaluate defensive value"""
        score = 0.0

        # Check if there are opponent threats on field
        opponent_cards = [c for c, p, pos in state.cards_on_field if p == "opponent"]

        if opponent_cards:
            # Playing defense is good
            if move.card.card_type == "troop":
                score += 20
            if move.card.card_type == "spell":
                score += 15

        return score

    def _evaluate_offensive_threat(self, move: Move, state: GameState) -> float:
        """Evaluate offensive pressure"""
        score = 0.0

        # Heavy cards create strong pushes
        if move.card.elixir_cost >= 5 and move.card.card_type == "troop":
            score += 15

        # Supporting troops
        player_cards = [c for c, p, pos in state.cards_on_field if p == move.player]
        if len(player_cards) > 0 and move.card.card_type == "troop":
            score += 10  # Good to support existing push

        return score

    def _evaluate_synergy(self, move: Move, state: GameState) -> float:
        """Evaluate card synergy"""
        score = 0.0

        player_cards = [c for c, p, pos in state.cards_on_field if p == move.player]

        for card in player_cards:
            # Example synergies
            if card.name == "Giant" and move.card.name in ["Wizard", "Musketeer"]:
                score += 25  # Great synergy
            if card.name == "Hog Rider" and move.card.name == "Freeze":
                score += 20

        return score

    def _evaluate_timing(self, move: Move, state: GameState) -> float:
        """Evaluate move timing"""
        score = 0.0

        # Don't waste spells when nothing is on field
        if move.card.card_type == "spell":
            opponent_cards = [c for c, p, pos in state.cards_on_field if p == "opponent"]
            if not opponent_cards:
                score -= 30  # Major waste

        return score

    def _classify_move_quality(self, score: float) -> MoveQuality:
        """Classify move based on evaluation score"""
        if score >= 50:
            return MoveQuality.BRILLIANT
        elif score >= 30:
            return MoveQuality.GREAT
        elif score >= 10:
            return MoveQuality.GOOD
        elif score >= -10:
            return MoveQuality.INACCURACY
        elif score >= -30:
            return MoveQuality.MISTAKE
        else:
            return MoveQuality.BLUNDER

    def _generate_alternatives(
        self,
        move: Move,
        state: GameState
    ) -> List[Tuple[Move, float]]:
        """Generate better alternative moves"""
        # In production, this would use ML to suggest better plays
        # For now, return empty list
        return []

    def _generate_reasoning(
        self,
        move: Move,
        quality: MoveQuality,
        factors: List[str]
    ) -> str:
        """Generate human-readable reasoning"""
        if quality == MoveQuality.BRILLIANT:
            reason = f"Excellent play! {move.card.name} was the perfect card here."
        elif quality == MoveQuality.BLUNDER:
            reason = f"This was a mistake. {move.card.name} should not have been played here."
        else:
            reason = f"{move.card.name} played at {move.timestamp:.1f}s."

        if factors:
            reason += " " + " ".join(factors)

        return reason

    def _calculate_win_probability_timeline(
        self,
        states: List[GameState]
    ) -> List[Tuple[float, float]]:
        """Calculate win probability over time"""
        timeline = []

        for state in states:
            # Simple win probability based on tower health and elixir
            player_health = sum(state.player_towers.values())
            opponent_health = sum(state.opponent_towers.values())

            total_health = player_health + opponent_health
            if total_health > 0:
                win_prob = (player_health / total_health) * 100
            else:
                win_prob = 50.0

            # Adjust for elixir advantage
            elixir_diff = state.player_elixir - state.opponent_elixir
            win_prob += elixir_diff * 2

            # Clamp between 0-100
            win_prob = max(0, min(100, win_prob))

            timeline.append((state.timestamp, win_prob))

        return timeline

    def _determine_playstyle(
        self,
        moves: List[Move],
        evaluations: List[MoveEvaluation]
    ) -> Playstyle:
        """Determine player's playstyle"""
        player_moves = [m for m in moves if m.player == "player"]

        if not player_moves:
            return Playstyle.CONTROL

        # Calculate average elixir cost
        avg_cost = sum(m.card.elixir_cost for m in player_moves) / len(player_moves)

        # Count card types
        spell_count = sum(1 for m in player_moves if m.card.card_type == "spell")
        troop_count = sum(1 for m in player_moves if m.card.card_type == "troop")

        if avg_cost >= 5:
            return Playstyle.BEATDOWN
        elif avg_cost <= 3:
            return Playstyle.CYCLE
        elif spell_count > troop_count:
            return Playstyle.CHIP
        else:
            return Playstyle.CONTROL

    def _find_key_moments(
        self,
        evaluations: List[MoveEvaluation],
        win_prob: List[Tuple[float, float]]
    ) -> List[Tuple[float, str]]:
        """Find key moments in the game"""
        moments = []

        # Find brilliant moves
        for eval in evaluations:
            if eval.quality == MoveQuality.BRILLIANT:
                moments.append((
                    eval.move.timestamp,
                    f"Brilliant: {eval.move.card.name} by {eval.move.player}"
                ))

        # Find blunders
        for eval in evaluations:
            if eval.quality == MoveQuality.BLUNDER:
                moments.append((
                    eval.move.timestamp,
                    f"Blunder: {eval.move.card.name} by {eval.move.player}"
                ))

        # Find big win probability swings
        for i in range(1, len(win_prob)):
            diff = abs(win_prob[i][1] - win_prob[i - 1][1])
            if diff > 20:
                moments.append((
                    win_prob[i][0],
                    f"Major shift in advantage ({diff:.0f}% swing)"
                ))

        moments.sort(key=lambda x: x[0])

        return moments

    def _calculate_statistics(
        self,
        moves: List[Move],
        evaluations: List[MoveEvaluation]
    ) -> Dict[str, any]:
        """Calculate game statistics"""
        player_moves = [e for e in evaluations if e.move.player == "player"]

        if not player_moves:
            return {}

        accuracy = sum(
            1 for e in player_moves
            if e.quality in [MoveQuality.BRILLIANT, MoveQuality.GREAT, MoveQuality.GOOD]
        ) / len(player_moves) * 100

        return {
            "total_moves": len(player_moves),
            "accuracy": accuracy,
            "brilliant_moves": sum(1 for e in player_moves if e.quality == MoveQuality.BRILLIANT),
            "good_moves": sum(1 for e in player_moves if e.quality == MoveQuality.GOOD),
            "mistakes": sum(1 for e in player_moves if e.quality == MoveQuality.MISTAKE),
            "blunders": sum(1 for e in player_moves if e.quality == MoveQuality.BLUNDER),
            "average_score": sum(e.evaluation_score for e in player_moves) / len(player_moves)
        }

    def _generate_recommendations(
        self,
        moves: List[Move],
        evaluations: List[MoveEvaluation],
        playstyle: Playstyle,
        stats: Dict[str, any]
    ) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []

        # Based on accuracy
        if stats.get("accuracy", 0) < 50:
            recommendations.append(
                "Focus on improving card placement timing and positioning"
            )

        # Based on blunders
        if stats.get("blunders", 0) > 3:
            recommendations.append(
                "Avoid panic plays - wait for the right moment to use your cards"
            )

        # Based on playstyle
        if playstyle == Playstyle.AGGRESSIVE:
            recommendations.append(
                "Consider playing more defensively to build stronger counter-pushes"
            )
        elif playstyle == Playstyle.DEFENSIVE:
            recommendations.append(
                "Try to apply more pressure to force your opponent to respond"
            )

        # Elixir management
        recommendations.append(
            "Manage your elixir carefully - avoid going below 2 elixir unless necessary"
        )

        return recommendations

    def _determine_winner(self, states: List[GameState]) -> Optional[str]:
        """Determine game winner based on final state"""
        if not states:
            return None

        final_state = states[-1]

        player_health = sum(final_state.player_towers.values())
        opponent_health = sum(final_state.opponent_towers.values())

        if player_health > opponent_health:
            return "player"
        elif opponent_health > player_health:
            return "opponent"
        else:
            return "draw"
