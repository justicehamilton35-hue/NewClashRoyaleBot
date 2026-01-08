import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AnalysisPage from './pages/AnalysisPage'
import GamesPage from './pages/GamesPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="analysis/:jobId" element={<AnalysisPage />} />
        <Route path="games" element={<GamesPage />} />
      </Route>
    </Routes>
  )
}

export default App
