import { useState } from 'react'
import { FloatingChatButton } from '@/components/floatingChatButton'
import { ChatWindow } from '@/components/chatWindow'
import { type Props as Message } from '@/components/messageBubble'
import { LayoutGroup } from 'framer-motion'
import { extractUsedIndices, remapAnswer, getUsedSources } from './utils'

// Global chatbot state and layout controller
export const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  // UI mode: controls whether to show button / chat / expanded
  const [mode, setMode] = useState<'normal' | 'expanded' | 'closed'>('closed')
  const defaultGreeting: Message = {
    role: 'bot',
    text: 'Hello, I’m Nesti. How can I help you today?',
    sources: [],
    mode: mode,
  }

  const handleSend = async (question: string) => {
    const userMessage: Message = { role: 'user', text: question, sources: [], mode }
    const loadingMessage: Message = { role: 'bot', text: '', sources: [], mode, isLoading: true }

    setMessages((prev) => [...prev, userMessage, loadingMessage])
    setIsLoading(true)

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      const data = await res.json()
      // console.log('Response from server:', data)

      const usedIndices = extractUsedIndices(data.answer)
      const remappedAnswer = remapAnswer(data.answer, usedIndices)
      const filteredSources = getUsedSources(data.sources, usedIndices)

      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: 'bot',
          text: remappedAnswer,
          sources: filteredSources,
          mode,
        }
        return updated
      })
    } catch {
      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: 'bot',
          text: 'Sorry, I encountered an error while processing your request.',
          sources: [],
          mode,
        }
        return updated
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <LayoutGroup>
      {mode === 'closed' ? (
        <FloatingChatButton
          onClick={() => {
            setMode('normal')
            setMessages((prev) => [...prev, defaultGreeting])
          }}
        />
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
