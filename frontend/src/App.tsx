import { useState, useEffect } from 'react'
import TopBar from './components/TopBar/TopBar'
import Chat from './components/Chat/Chat'
import InputBar from './components/Input/InputBar'
import './components/TopBar/TopBar.scss'
import './components/Chat/Chat.scss'
import './components/Input/InputBar.scss'
import './components/Message/Message.scss'

type Theme = 'light' | 'dark'
type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  sql?: string
  timestamp: string
}

export default function App() {
  const [theme, setTheme] = useState<Theme>('dark')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  const handleSend = (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    // Stub assistant response for now
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'This is a stubbed response. Backend not connected yet.',
        sql: 'SELECT * FROM expenses LIMIT 10;',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      setMessages(prev => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="app">
      <TopBar theme={theme} onToggleTheme={toggleTheme} />
      <Chat messages={messages} isLoading={isLoading} />
      <InputBar onSend={handleSend} isLoading={isLoading} />
    </div>
  )
}