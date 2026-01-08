import { MoveEvaluation, KeyMoment } from '../types'
import { Sparkles, AlertTriangle } from 'lucide-react'

interface Props {
  moves: MoveEvaluation[]
  keyMoments: KeyMoment[]
  duration: number
}

const qualityColors = {
  brilliant: 'bg-brilliant',
  great: 'bg-great',
  good: 'bg-good',
  inaccuracy: 'bg-inaccuracy',
  mistake: 'bg-mistake',
  blunder: 'bg-blunder',
}

const qualityLabels = {
  brilliant: 'Brilliant!',
  great: 'Great',
  good: 'Good',
  inaccuracy: 'Inaccuracy',
  mistake: 'Mistake',
  blunder: 'Blunder',
}

export default function MoveTimeline({ moves, keyMoments, duration }: Props) {
  // Only show player moves
  const playerMoves = moves.filter(m => m.player === 'player')

  return (
    <div className="space-y-4">
      {/* Move quality legend */}
      <div className="flex flex-wrap gap-2 text-xs">
        {Object.entries(qualityLabels).map(([key, label]) => (
          <div key={key} className="flex items-center space-x-1">
            <div className={`w-3 h-3 rounded ${qualityColors[key as keyof typeof qualityColors]}`} />
            <span className="text-gray-400">{label}</span>
          </div>
        ))}
      </div>

      {/* Timeline */}
      <div className="space-y-3 max-h-[600px] overflow-y-auto">
        {playerMoves.map((move, i) => (
          <div
            key={i}
            className="bg-gray-700 rounded-lg p-4 hover:bg-gray-650 transition"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center space-x-3">
                {/* Time */}
                <div className="text-gray-400 font-mono text-sm">
                  {Math.floor(move.timestamp / 60)}:{(move.timestamp % 60).toFixed(0).padStart(2, '0')}
                </div>

                {/* Card name */}
                <div className="font-semibold">{move.card}</div>

                {/* Quality badge */}
                <div className={`px-2 py-1 rounded text-xs font-semibold text-white ${qualityColors[move.quality]}`}>
                  {move.quality === 'brilliant' && <Sparkles className="w-3 h-3 inline mr-1" />}
                  {move.quality === 'blunder' && <AlertTriangle className="w-3 h-3 inline mr-1" />}
                  {qualityLabels[move.quality]}
                </div>
              </div>

              {/* Score */}
              <div className={`font-mono text-sm ${
                move.score > 0 ? 'text-green-500' : move.score < 0 ? 'text-red-500' : 'text-gray-400'
              }`}>
                {move.score > 0 ? '+' : ''}{move.score.toFixed(1)}
              </div>
            </div>

            {/* Reasoning */}
            <div className="text-sm text-gray-300">{move.reasoning}</div>

            {/* Key factors */}
            {move.factors.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {move.factors.map((factor, j) => (
                  <span key={j} className="text-xs bg-gray-800 px-2 py-1 rounded text-gray-400">
                    {factor}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
