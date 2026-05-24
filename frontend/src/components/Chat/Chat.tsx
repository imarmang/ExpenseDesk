import { useEffect, useRef, useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import Message from '../Message/Message'
import type { MessageType } from '../Message/Message'
import { faArrowDown, faCommentDots } from '@fortawesome/free-solid-svg-icons'

type Props = {
  messages: MessageType[]
  isLoading: boolean
}

export default function Chat({ messages, isLoading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [showScrollBtn, setShowScrollBtn] = useState(false)

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const handleScroll = () => {
    const el = containerRef.current
    if (!el) return
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight
    setShowScrollBtn(distanceFromBottom > 100)
  }

  return (
    <div
      className="chat"
      ref={containerRef}
      onScroll={handleScroll}
    >
      <div className="chat__inner">
        {messages.length === 0 && !isLoading ? (
          <div className="chat__empty">
            <div className="chat__empty-icon">
              <FontAwesomeIcon icon={faCommentDots} />
            </div>
            <p className="chat__empty-title">Welcome to ExpenseDesk</p>
            <p className="chat__empty-sub">
              Ask anything about your company expenses.<br />
              Try <em>"Show me all pending expenses this month"</em>
            </p>
          </div>
        ) : (
          <>
            {messages.map(msg => (
              <Message key={msg.id} message={msg} />
            ))}

            {isLoading && (
              <div className="chat__typing message message--assistant">
                <div className="chat__bubble-typing message__bubble">
                  <span className="chat__dot" />
                  <span className="chat__dot" />
                  <span className="chat__dot" />
                </div>
              </div>
            )}
          </>
        )}

        <div ref={bottomRef} />
      </div>

      {showScrollBtn && (
        <button className="chat__scroll-btn" onClick={scrollToBottom} aria-label="Scroll to bottom">
          <FontAwesomeIcon icon={faArrowDown} />
        </button>
      )}
    </div>
  )
}