import { Outlet, Link, useLocation } from 'react-router-dom'
import { Crown, Upload, List } from 'lucide-react'

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header - Chess.com style */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2 hover:opacity-80 transition">
              <Crown className="w-8 h-8 text-cr-orange" />
              <span className="text-xl font-bold">Clash Royale Analyzer</span>
            </Link>

            {/* Navigation */}
            <nav className="flex items-center space-x-6">
              <Link
                to="/"
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition ${
                  location.pathname === '/'
                    ? 'bg-gray-700 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700'
                }`}
              >
                <Upload className="w-4 h-4" />
                <span>Analyze</span>
              </Link>
              <Link
                to="/games"
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition ${
                  location.pathname === '/games'
                    ? 'bg-gray-700 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700'
                }`}
              >
                <List className="w-4 h-4" />
                <span>My Games</span>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-gray-400 text-sm">
            <p>Clash Royale Analyzer - Stockfish for Clash Royale</p>
            <p className="mt-2">Upload your gameplay and get AI-powered insights</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
