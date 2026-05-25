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

  const handleSend = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

        try {
        const res = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: content })
        })

        const data = await res.json()

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.response,
          sql: data.sql,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
        setMessages(prev => [...prev, assistantMessage])
      } catch (error) {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Something went wrong. Make sure the backend is running.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
        setMessages(prev => [...prev, errorMessage])
      } finally {
        setIsLoading(false)
      }
  }

  return (
    <div className="app">
      <TopBar theme={theme} onToggleTheme={toggleTheme} />
      <Chat messages={messages} isLoading={isLoading} />
      <InputBar onSend={handleSend} isLoading={isLoading} />
    </div>
  )
}