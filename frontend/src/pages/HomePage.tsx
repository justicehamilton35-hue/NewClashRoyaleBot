import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, Sparkles, TrendingUp, Target, Brain } from 'lucide-react'
import { uploadVideo } from '../services/api'

export default function HomePage() {
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const navigate = useNavigate()

  const handleUpload = async (file: File) => {
    if (!file.type.includes('video')) {
      alert('Please upload a video file')
      return
    }

    setUploading(true)

    try {
      const result = await uploadVideo(file)
      navigate(`/analysis/${result.job_id}`)
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file) {
      handleUpload(file)
    }
  }, [])

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const onFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleUpload(file)
    }
  }, [])

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-4">
          Clash Royale Gameplay Analyzer
        </h1>
        <p className="text-xl text-gray-400 mb-2">
          Stockfish-level analysis for your Clash Royale games
        </p>
        <p className="text-gray-500">
          Upload your gameplay and get AI-powered insights on every move
        </p>
      </div>

      {/* Upload Area - Chess.com style */}
      <div
        className={`border-4 border-dashed rounded-2xl p-12 mb-12 transition-all ${
          isDragging
            ? 'border-cr-blue bg-cr-blue bg-opacity-10'
            : 'border-gray-700 hover:border-gray-600'
        } ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
      >
        <div className="text-center">
          <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />

          <h2 className="text-2xl font-semibold mb-2">
            {uploading ? 'Uploading...' : 'Upload Your Gameplay'}
          </h2>

          <p className="text-gray-400 mb-6">
            Drag and drop your MP4 file here, or click to browse
          </p>

          <label className="inline-block">
            <input
              type="file"
              accept="video/*"
              onChange={onFileSelect}
              className="hidden"
              disabled={uploading}
            />
            <span className="px-8 py-3 bg-cr-blue hover:bg-opacity-90 rounded-lg cursor-pointer inline-block transition">
              Select Video File
            </span>
          </label>

          <p className="text-sm text-gray-500 mt-4">
            Supported formats: MP4, MOV, AVI (Max: 500MB)
          </p>
        </div>
      </div>

      {/* Features Grid - Chess.com style */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <FeatureCard
          icon={<Brain className="w-8 h-8" />}
          title="AI Analysis"
          description="Stockfish-level move evaluation for every card played"
          color="text-cr-blue"
        />
        <FeatureCard
          icon={<Target className="w-8 h-8" />}
          title="Find Blunders"
          description="Identify mistakes and learn from them"
          color="text-red-500"
        />
        <FeatureCard
          icon={<Sparkles className="w-8 h-8" />}
          title="Brilliant Moves"
          description="Highlight your best plays and strategies"
          color="text-brilliant"
        />
        <FeatureCard
          icon={<TrendingUp className="w-8 h-8" />}
          title="Win Probability"
          description="Track your chances throughout the game"
          color="text-cr-orange"
        />
      </div>

      {/* How It Works */}
      <div className="bg-gray-800 rounded-2xl p-8 mb-12">
        <h3 className="text-2xl font-bold mb-6 text-center">How It Works</h3>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-cr-blue rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
              1
            </div>
            <h4 className="font-semibold mb-2">Upload Video</h4>
            <p className="text-sm text-gray-400">
              Upload your Clash Royale gameplay video (MP4 format)
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-cr-purple rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
              2
            </div>
            <h4 className="font-semibold mb-2">AI Analysis</h4>
            <p className="text-sm text-gray-400">
              Our AI detects every card and analyzes your moves
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-cr-orange rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
              3
            </div>
            <h4 className="font-semibold mb-2">Get Insights</h4>
            <p className="text-sm text-gray-400">
              Review detailed analysis with move quality and recommendations
            </p>
          </div>
        </div>
      </div>

      {/* Example Results */}
      <div className="text-center text-gray-400">
        <p className="mb-2">Example Analysis Features:</p>
        <div className="flex flex-wrap justify-center gap-4">
          <span className="px-4 py-2 bg-brilliant rounded-lg text-white text-sm">
            Brilliant Moves
          </span>
          <span className="px-4 py-2 bg-great rounded-lg text-white text-sm">
            Great Plays
          </span>
          <span className="px-4 py-2 bg-good rounded-lg text-white text-sm">
            Good Moves
          </span>
          <span className="px-4 py-2 bg-inaccuracy rounded-lg text-white text-sm">
            Inaccuracies
          </span>
          <span className="px-4 py-2 bg-mistake rounded-lg text-white text-sm">
            Mistakes
          </span>
          <span className="px-4 py-2 bg-blunder rounded-lg text-white text-sm">
            Blunders
          </span>
        </div>
      </div>
    </div>
  )
}

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
  color: string
}

function FeatureCard({ icon, title, description, color }: FeatureCardProps) {
  return (
    <div className="bg-gray-800 rounded-xl p-6 hover:bg-gray-750 transition">
      <div className={`mb-3 ${color}`}>{icon}</div>
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  )
}
