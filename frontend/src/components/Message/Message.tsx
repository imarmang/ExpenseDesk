import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronDown, faChevronUp, faCopy, faCheck } from '@fortawesome/free-solid-svg-icons'

export type MessageType = {
  id: string
  role: 'user' | 'assistant'
  content: string
  sql?: string
  timestamp: string
}

type Props = {
  message: MessageType
}

export default function Message({ message }: Props) {
  const [sqlOpen, setSqlOpen] = useState(true)
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    if (!message.sql) return
    navigator.clipboard.writeText(message.sql)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className={`message message--${message.role}`}>
      <div className="message__bubble">
        {message.content}
      </div>

      {message.sql && (
        <div className="message__sql">
          <div className="message__sql-header" onClick={() => setSqlOpen(prev => !prev)}>
            <div className="message__sql-header-left">
              <div className="message__sql-dot" />
              <span className="message__sql-label">generated sql</span>
            </div>
            <div className="message__sql-actions">
              <button
                className="message__sql-copy"
                onClick={e => { e.stopPropagation(); handleCopy() }}
                aria-label="Copy SQL"
              >
                <FontAwesomeIcon icon={copied ? faCheck : faCopy} />
                <span>{copied ? 'copied' : 'copy'}</span>
              </button>
              <FontAwesomeIcon
                icon={sqlOpen ? faChevronUp : faChevronDown}
                className="message__sql-chevron"
              />
            </div>
          </div>

          {sqlOpen && (
            <pre className="message__sql-body">{message.sql}</pre>
          )}
        </div>
      )}

      <span className="message__meta">
        {message.role === 'user' ? 'You' : 'ExpenseDesk'} · {message.timestamp}
      </span>
    </div>
  )
}