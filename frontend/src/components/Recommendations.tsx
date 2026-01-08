import { Lightbulb } from 'lucide-react'

interface Props {
  recommendations: string[]
}

export default function Recommendations({ recommendations }: Props) {
  if (!recommendations || recommendations.length === 0) {
    return null
  }

  return (
    <div className="bg-gradient-to-r from-cr-blue to-cr-purple rounded-lg p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Lightbulb className="w-6 h-6" />
        <h2 className="text-xl font-bold">Recommendations</h2>
      </div>

      <ul className="space-y-3">
        {recommendations.map((rec, i) => (
          <li key={i} className="flex items-start space-x-2">
            <span className="text-white font-bold mt-0.5">•</span>
            <span className="text-white">{rec}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
