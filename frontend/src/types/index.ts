export interface Card {
  name: string
  elixir: number
  type: 'troop' | 'spell' | 'building'
}

export interface Move {
  timestamp: number
  player: 'player' | 'opponent'
  card: string
  elixir_cost: number
  position: [number, number]
}

export type MoveQuality = 'brilliant' | 'great' | 'good' | 'inaccuracy' | 'mistake' | 'blunder'

export interface MoveEvaluation {
  timestamp: number
  card: string
  player: 'player' | 'opponent'
  quality: MoveQuality
  score: number
  reasoning: string
  factors: string[]
}

export interface WinProbabilityPoint {
  timestamp: number
  win_probability: number
}

export interface KeyMoment {
  timestamp: number
  description: string
}

export interface GameStatistics {
  total_moves: number
  accuracy: number
  brilliant_moves: number
  good_moves: number
  mistakes: number
  blunders: number
  average_score: number
}

export type Playstyle = 'aggressive' | 'control' | 'cycle' | 'beatdown' | 'chip' | 'defensive'

export interface GameAnalysis {
  game_id: string
  duration: number
  winner: 'player' | 'opponent' | 'draw' | null
  video_metadata: {
    fps: number
    resolution: [number, number]
    total_frames: number
  }
  player_deck: Card[]
  opponent_deck: Card[]
  moves: Move[]
  move_evaluations: MoveEvaluation[]
  win_probability_timeline: WinProbabilityPoint[]
  playstyle: Playstyle
  key_moments: KeyMoment[]
  statistics: GameStatistics
  recommendations: string[]
}

export interface AnalysisJob {
  job_id: string
  status: 'processing' | 'completed' | 'failed'
  progress: number
  video_path?: string
  filename?: string
  error?: string
  analysis?: GameAnalysis
}
