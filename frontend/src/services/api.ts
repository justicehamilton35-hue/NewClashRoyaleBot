import axios from 'axios'
import { GameAnalysis, AnalysisJob } from '../types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadVideo = async (file: File): Promise<{ job_id: string }> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/analysis/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export const getAnalysisStatus = async (jobId: string): Promise<AnalysisJob> => {
  const response = await api.get(`/analysis/status/${jobId}`)
  return response.data
}

export const getAnalysisResult = async (jobId: string): Promise<GameAnalysis> => {
  const response = await api.get(`/analysis/result/${jobId}`)
  return response.data
}

export const listGames = async (limit = 10, offset = 0) => {
  const response = await api.get('/games', {
    params: { limit, offset },
  })
  return response.data
}

export const getGame = async (gameId: string): Promise<GameAnalysis> => {
  const response = await api.get(`/games/${gameId}`)
  return response.data
}

export const deleteGame = async (gameId: string) => {
  await api.delete(`/games/${gameId}`)
}

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}
