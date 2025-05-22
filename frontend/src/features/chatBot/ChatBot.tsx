import { useState } from 'react'
import { FloatingChatButton } from '@/components/floatingChatButton'
import { ChatWindow } from '@/components/chatWindow'
import { type Props as Message } from '@/components/messageBubble'
import { LayoutGroup } from 'framer-motion'

// Global chatbot state and layout controller
export const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  // UI mode: controls whether to show button / chat / expanded
  const [mode, setMode] = useState<'normal' | 'expanded' | 'closed'>('closed')

  const handleSend = async (question: string) => {
    setMessages((prev) => [...prev, { role: 'user', text: question }])
    setIsLoading(true)

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'bot', text: data.answer }])
    } catch {
      setMessages((prev) => [...prev, { role: 'bot', text: 'Something went wrong.' }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <LayoutGroup>
      {mode === 'closed' ? (
        <FloatingChatButton onClick={() => setMode('normal')} />
      ) : (
        <ChatWindow
          mode={mode}
          onToggleSize={() => setMode(mode === 'normal' ? 'expanded' : 'normal')}
          onClose={() => setMode('closed')}
          onSend={handleSend}
          messages={messages}
          isLoading={isLoading}
        />
      )}
    </LayoutGroup>
  )
}
