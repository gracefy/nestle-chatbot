import React, { useState } from 'react'
import { Send } from 'lucide-react'

interface Props {
  onSend: (question: string) => void
  isLoading: boolean
}

// User input field and send button
export const ChatInput = ({ onSend, isLoading }: Props) => {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return
    onSend(input)
    setInput('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 bg-white p-2">
      <input
        className="flex-1 border border-brand rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-brand"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask something..."
        disabled={isLoading}
      />
      <button
        type="submit"
        className=" text-brand hover:text-brand-hover p-2 disabled:opacity-50 cursor-pointer transition-colors duration-200"
        disabled={isLoading}
        aria-label="Send message"
      >
        {isLoading ? '...' : <Send className="w-5 h-5" />}
      </button>
    </form>
  )
}
