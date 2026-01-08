import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { getAnalysisStatus, getAnalysisResult } from '../services/api'
import { GameAnalysis } from '../types'
import WinProbabilityChart from '../components/WinProbabilityChart'
import MoveTimeline from '../components/MoveTimeline'
import GameStatistics from '../components/GameStatistics'
import Recommendations from '../components/Recommendations'
import DeckDisplay from '../components/DeckDisplay'

export default function AnalysisPage() {
  const { jobId } = useParams<{ jobId: string }>()
  const [analysis, setAnalysis] = useState<GameAnalysis | null>(null)

  // Poll for job status
  const { data: job, isLoading } = useQuery({
    queryKey: ['analysis-status', jobId],
    queryFn: () => getAnalysisStatus(jobId!),
    refetchInterval: (data) => {
      // Stop polling when completed or failed
      if (data?.status === 'completed' || data?.status === 'failed') {
        return false
      }
      return 2000 // Poll every 2 seconds
    },
    enabled: !!jobId,
  })

  // Fetch full analysis when complete
  useEffect(() => {
    if (job?.status === 'completed') {
      getAnalysisResult(jobId!).then(setAnalysis)
    }
  }, [job?.status, jobId])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-cr-blue" />
      </div>
    )
  }

  if (job?.status === 'failed') {
    return (
      <div className="text-center py-12">
        <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-8 max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-red-500 mb-4">Analysis Failed</h2>
          <p className="text-gray-300">{job.error || 'An error occurred during analysis'}</p>
        </div>
      </div>
    )
  }

  if (job?.status === 'processing') {
    return (
      <div className="text-center py-12">
        <div className="bg-gray-800 rounded-lg p-8 max-w-2xl mx-auto">
          <Loader2 className="w-12 h-12 animate-spin text-cr-blue mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-4">Analyzing Your Game...</h2>
          <p className="text-gray-400 mb-6">
            Our AI is processing your video and analyzing every move
          </p>

          {/* Progress Bar */}
          <div className="w-full bg-gray-700 rounded-full h-4 mb-4">
            <div
              className="bg-cr-blue h-4 rounded-full transition-all duration-500"
              style={{ width: `${job.progress}%` }}
            />
          </div>

          <p className="text-sm text-gray-500">{job.progress}% complete</p>

          <div className="mt-8 text-left">
            <p className="text-sm text-gray-400 mb-2">Processing steps:</p>
            <ul className="space-y-2 text-sm">
              <li className={job.progress >= 20 ? 'text-green-500' : 'text-gray-500'}>
                ✓ Video uploaded
              </li>
              <li className={job.progress >= 40 ? 'text-green-500' : 'text-gray-500'}>
                {job.progress >= 40 ? '✓' : '○'} Extracting frames
              </li>
              <li className={job.progress >= 70 ? 'text-green-500' : 'text-gray-500'}>
                {job.progress >= 70 ? '✓' : '○'} Detecting cards
              </li>
              <li className={job.progress >= 90 ? 'text-green-500' : 'text-gray-500'}>
                {job.progress >= 90 ? '✓' : '○'} Analyzing gameplay
              </li>
              <li className={job.progress === 100 ? 'text-green-500' : 'text-gray-500'}>
                {job.progress === 100 ? '✓' : '○'} Finalizing results
              </li>
            </ul>
          </div>
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-cr-blue mx-auto" />
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Game Analysis</h1>
        <div className="flex items-center space-x-4 text-gray-400">
          <span>Duration: {Math.floor(analysis.duration / 60)}:{(analysis.duration % 60).toFixed(0).padStart(2, '0')}</span>
          <span>•</span>
          <span>Playstyle: <span className="text-cr-blue capitalize">{analysis.playstyle}</span></span>
          {analysis.winner && (
            <>
              <span>•</span>
              <span className={analysis.winner === 'player' ? 'text-green-500' : 'text-red-500'}>
                Winner: {analysis.winner === 'player' ? 'You' : 'Opponent'}
              </span>
            </>
          )}
        </div>
      </div>

      {/* Chess.com-style Layout: Main content on left, sidebar on right */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main Content - 2/3 width */}
        <div className="lg:col-span-2 space-y-6">
          {/* Win Probability Chart */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Win Probability</h2>
            <WinProbabilityChart data={analysis.win_probability_timeline} />
          </div>

          {/* Move Timeline */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Move Timeline</h2>
            <MoveTimeline
              moves={analysis.move_evaluations}
              keyMoments={analysis.key_moments}
              duration={analysis.duration}
            />
          </div>

          {/* Recommendations */}
          <Recommendations recommendations={analysis.recommendations} />
        </div>

        {/* Sidebar - 1/3 width */}
        <div className="space-y-6">
          {/* Statistics */}
          <GameStatistics stats={analysis.statistics} />

          {/* Player Deck */}
          <DeckDisplay
            title="Your Deck"
            deck={analysis.player_deck}
            highlight
          />

          {/* Opponent Deck */}
          <DeckDisplay
            title="Opponent Deck"
            deck={analysis.opponent_deck}
          />

          {/* Key Moments */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-bold mb-4">Key Moments</h3>
            <div className="space-y-3">
              {analysis.key_moments.slice(0, 5).map((moment, i) => (
                <div key={i} className="text-sm">
                  <div className="text-gray-400">
                    {Math.floor(moment.timestamp / 60)}:{(moment.timestamp % 60).toFixed(0).padStart(2, '0')}
                  </div>
                  <div className="text-gray-200">{moment.description}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
