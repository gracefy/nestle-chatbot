import { User, BotMessageSquare } from 'lucide-react'
import { clsx } from 'clsx'

export interface Props {
  role: 'user' | 'bot'
  text: string
}

// Display single chat message from user or bot
export const MessageBubble = ({ role, text }: Props) => {
  const isUser = role === 'user'

  return (
    <div className={clsx('flex w-full', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={clsx(
          'relative max-w-[85%] md:max-w-[70%] whitespace-pre-wrap rounded-xl px-4 py-2 text-sm md:text-base shadow-sm',
          isUser ? 'bg-gray-100/80 text-brand' : 'bg-brand/80 text-gray-100'
        )}
      >
        {/* Bot icon */}
        {!isUser && (
          <div className="absolute -top-4 left-0 flex flex-col items-center">
            <BotMessageSquare className="w-4 h-4 text-brand scale-x-[-1]" />
          </div>
        )}

        {text}

        {/* User icon */}
        {isUser && (
          <div className="absolute -top-4 right-0 flex flex-col items-center">
            <User className="w-4 h-4 text-gray-400" />
          </div>
        )}
      </div>
    </div>
  )
}
