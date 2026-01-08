import { GameStatistics as Stats } from '../types'
import { Target, TrendingUp, Zap } from 'lucide-react'

interface Props {
  stats: Stats
}

export default function GameStatistics({ stats }: Props) {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-lg font-bold mb-4">Statistics</h3>

      <div className="space-y-4">
        {/* Accuracy */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              <Target className="w-4 h-4 text-cr-blue" />
              <span className="text-sm text-gray-400">Accuracy</span>
            </div>
            <span className="font-semibold">{stats.accuracy?.toFixed(1) || 0}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className="bg-cr-blue h-2 rounded-full transition-all"
              style={{ width: `${stats.accuracy || 0}%` }}
            />
          </div>
        </div>

        {/* Total Moves */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-cr-purple" />
            <span className="text-sm text-gray-400">Total Moves</span>
          </div>
          <span className="font-semibold">{stats.total_moves || 0}</span>
        </div>

        {/* Average Score */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-cr-orange" />
            <span className="text-sm text-gray-400">Avg Score</span>
          </div>
          <span className={`font-semibold ${
            (stats.average_score || 0) > 0 ? 'text-green-500' : 'text-red-500'
          }`}>
            {(stats.average_score || 0) > 0 ? '+' : ''}
            {stats.average_score?.toFixed(1) || 0}
          </span>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-700 my-4" />

        {/* Move Quality Breakdown */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-brilliant">● Brilliant</span>
            <span className="font-semibold">{stats.brilliant_moves || 0}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-good">● Good</span>
            <span className="font-semibold">{stats.good_moves || 0}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-mistake">● Mistakes</span>
            <span className="font-semibold">{stats.mistakes || 0}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-blunder">● Blunders</span>
            <span className="font-semibold">{stats.blunders || 0}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
