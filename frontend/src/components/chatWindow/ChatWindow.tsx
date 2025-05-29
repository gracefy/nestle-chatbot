import { useEffect, useRef } from 'react'
import { clsx } from 'clsx'
import { X, BotMessageSquare, Maximize2, Minimize2 } from 'lucide-react'
import { ChatInput } from '@/components/chatInput'
import { MessageBubble, type Props as Message } from '@/components/messageBubble'

interface Props {
  onClose: () => void
  onSend: (question: string) => void
  onToggleSize: () => void
  messages: Message[]
  isLoading: boolean
  mode: 'normal' | 'expanded' | 'closed'
}

// Display chat UI in normal / expanded mode
export const ChatWindow = ({ onClose, onSend, onToggleSize, messages, isLoading, mode }: Props) => {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const isExpanded = mode === 'expanded'

  return (
    <div
      className={clsx(
        'font-sans bg-white shadow-lg ring-1 ring-brand rounded-xl flex flex-col',
        isExpanded
          ? 'w-[90vw] h-[90vh] md:w-[70vw] md:h-[80vh]'
          : 'w-[300px] md:w-[400px] h-[500px] md:h-[600px]'
      )}
    >
      {/* Header */}
      <div className="bg-brand text-white px-4 py-2 flex items-center justify-between text-sm font-semibold rounded-t-xl">
        <div className="flex items-center gap-2">
          <BotMessageSquare className="w-6 h-6 scale-x-[-1]" />
          <span>Nesti</span>
        </div>

        <div className="flex items-center gap-2">
          {/* Toggle window size */}
          <button
            onClick={onToggleSize}
            className="hover:text-gray-300 cursor-pointer transition-colors duration-200"
            aria-label="Toggle size"
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>

          {/* Close button */}
          <button
            onClick={onClose}
            className="hover:text-gray-300 cursor-pointer transition-colors duration-200"
            aria-label="Close chat"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Message  list*/}
      <div className="flex-1 overflow-y-auto px-4 py-6 flex flex-col gap-6">
        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            role={msg.role}
            text={msg.text}
            sources={msg.sources}
            mode={mode}
            isLoading={isLoading && i === messages.length - 1} // Show loading only for last message
          />
        ))}
        <div ref={messagesEndRef} className="h-0" /> {/* auto scroll anchor */}
      </div>

      {/* Input */}
      <div className="border-t px-4 py-2 border-brand/30 bg-white rounded-b-xl shadow-lg">
        <ChatInput onSend={onSend} isLoading={isLoading} />
      </div>
    </div>
  )
}
