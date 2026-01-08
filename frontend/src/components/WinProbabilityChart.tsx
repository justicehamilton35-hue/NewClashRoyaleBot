import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { WinProbabilityPoint } from '../types'

interface Props {
  data: WinProbabilityPoint[]
}

export default function WinProbabilityChart({ data }: Props) {
  // Transform data for recharts
  const chartData = data.map(point => ({
    time: Math.floor(point.timestamp / 60) + ':' + (point.timestamp % 60).toFixed(0).padStart(2, '0'),
    timestamp: point.timestamp,
    probability: point.win_probability,
  }))

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis
            dataKey="time"
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
          />
          <YAxis
            domain={[0, 100]}
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
            label={{ value: 'Win %', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1F2937',
              border: '1px solid #374151',
              borderRadius: '0.5rem',
              color: '#F3F4F6'
            }}
            formatter={(value: number) => [`${value.toFixed(1)}%`, 'Win Probability']}
          />
          <ReferenceLine y={50} stroke="#6B7280" strokeDasharray="3 3" />
          <Line
            type="monotone"
            dataKey="probability"
            stroke="#3B82F6"
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
