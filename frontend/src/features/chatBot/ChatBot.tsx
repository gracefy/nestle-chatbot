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

  // Chat UI display mode: closed, normal (default size), expanded (large size)
  const [mode, setMode] = useState<'normal' | 'expanded' | 'closed'>('closed')

  // Default greeting message shown when chat opens
  const defaultGreeting: Message = {
    role: 'bot',
    text: 'Hello, I’m Nesti. How can I help you today?',
    sources: [],
    mode: mode,
  }

  // Handle user question and send to backend API
  const handleSend = async (question: string) => {
    const userMessage: Message = { role: 'user', text: question, sources: [], mode }
    const loadingMessage: Message = { role: 'bot', text: '', sources: [], mode, isLoading: true }

    // Show user message and loading indicator
    setMessages((prev) => [...prev, userMessage, loadingMessage])
    setIsLoading(true)

    // Get the base URL from environment variables
    const baseUrl = import.meta.env.VITE_API_BASE_URL

    try {
      // Send question to backend /chat endpoint
      const res = await fetch(`${baseUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      const data = await res.json()
      // console.log('Response from server:', data)

      // Process answer and filter source references
      const usedIndices = extractUsedIndices(data.answer)
      const remappedAnswer = remapAnswer(data.answer, usedIndices)
      const filteredSources = getUsedSources(data.sources, usedIndices)

      // Replace loading message with final bot response
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
      // On error, show fallback error message
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
