import { Card } from '../types'

interface Props {
  title: string
  deck: Card[]
  highlight?: boolean
}

export default function DeckDisplay({ title, deck, highlight = false }: Props) {
  if (!deck || deck.length === 0) {
    return null
  }

  return (
    <div className={`rounded-lg p-6 ${
      highlight ? 'bg-gradient-to-br from-cr-blue to-cr-purple' : 'bg-gray-800'
    }`}>
      <h3 className="text-lg font-bold mb-4">{title}</h3>

      <div className="grid grid-cols-2 gap-3">
        {deck.map((card, i) => (
          <div
            key={i}
            className={`rounded-lg p-3 ${
              highlight ? 'bg-white bg-opacity-10' : 'bg-gray-700'
            }`}
          >
            <div className="font-semibold text-sm mb-1">{card.name}</div>
            <div className="flex items-center justify-between text-xs">
              <span className={`capitalize ${
                card.type === 'troop' ? 'text-cr-orange' :
                card.type === 'spell' ? 'text-cr-purple' :
                'text-cr-blue'
              }`}>
                {card.type}
              </span>
              <span className="bg-gray-900 bg-opacity-50 px-2 py-0.5 rounded">
                {card.elixir} ⚡
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Average elixir cost */}
      <div className="mt-4 pt-4 border-t border-gray-700 text-sm">
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Avg Elixir Cost</span>
          <span className="font-semibold">
            {(deck.reduce((sum, card) => sum + card.elixir, 0) / deck.length).toFixed(1)} ⚡
          </span>
        </div>
      </div>
    </div>
  )
}
