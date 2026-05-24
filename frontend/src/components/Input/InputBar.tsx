import { useState } from 'react'
import type { KeyboardEvent } from 'react'

type Props = {
  onSend: (message: string) => void
  isLoading: boolean
}

export default function InputBar({ onSend, isLoading }: Props) {
  const [value, setValue] = useState('')

  const handleSend = () => {
    if (!value.trim() || isLoading) return
    onSend(value.trim())
    setValue('')
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="inputbar">
      <div className="inputbar__row">
        <input
          className="inputbar__field"
          type="text"
          placeholder="Ask about your expenses..."
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button
          className="inputbar__send"
          onClick={handleSend}
          disabled={isLoading || !value.trim()}
          aria-label="Send message"
        >
          ↑
        </button>
      </div>
      <p className="inputbar__hint">
        ExpenseDesk · Powered by Ollama · Fully offline
      </p>
    </div>
  )
}