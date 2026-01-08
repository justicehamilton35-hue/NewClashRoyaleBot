import { Crown } from 'lucide-react'

export default function GamesPage() {
  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">My Analyzed Games</h1>

      <div className="text-center py-12">
        <Crown className="w-16 h-16 mx-auto mb-4 text-gray-600" />
        <p className="text-xl text-gray-400 mb-2">No games analyzed yet</p>
        <p className="text-gray-500">Upload your first gameplay video to get started</p>
      </div>
    </div>
  )
}
