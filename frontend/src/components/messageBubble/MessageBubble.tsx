import { User, BotMessageSquare } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { clsx } from 'clsx'

export interface Props {
  role: 'user' | 'bot'
  text: string
  mode: 'normal' | 'expanded' | 'closed'
  sources?: { title: string; url: string }[]
  isLoading?: boolean
}

// Display single chat message from user or bot
export const MessageBubble = ({ role, text, sources, mode, isLoading }: Props) => {
  const isUser = role === 'user'
  const isExpanded = mode === 'expanded'

  if (isLoading) {
    return (
      <div className={clsx('flex w-full mb-4 gap-2 items-center')}>
        <BotMessageSquare className="w-5 h-5 text-brand/80 scale-x-[-1]" />

        <div className="bot-bubble text-gray-100 italic px-4 py-2 rounded-xl bg-brand/80 flex gap-1">
          <span>Thinking</span>
          <span className="animate-bounce [animation-delay:0ms]">.</span>
          <span className="animate-bounce [animation-delay:200ms]">.</span>
          <span className="animate-bounce [animation-delay:400ms]">.</span>
        </div>
      </div>
    )
  }

  return (
    <div className={clsx('flex w-full mb-4', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={clsx(
          'relative flex flex-col gap-1 ',
          isExpanded ? 'max-w-[50%]' : 'max-w-[90%]'
        )}
      >
        {/* Avatar*/}
        {!isUser && (
          <div className="absolute -top-4 left-0">
            <BotMessageSquare className="w-5 h-5 text-brand scale-x-[-1]" />
          </div>
        )}
        {isUser && (
          <div className="absolute -top-4 right-0">
            <User className="w-5 h-5 text-gray-400" />
          </div>
        )}

        <div
          className={clsx(
            'rounded-xl px-3 py-1.5 text-sm md:text-base shadow-sm w-fit whitespace-pre-wrap',
            isUser ? 'bg-gray-100 text-brand' : 'bg-brand/80 text-white'
          )}
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ node, ...props }) => <p className="prose prose-slate" {...props} />,
              ol: ({ node, ...props }) => <ol className="list-decimal pl-6" {...props} />,
              li: ({ node, ...props }) => <li className="my-1" {...props} />,
            }}
          >
            {text}
          </ReactMarkdown>
        </div>

        {/* References block */}
        {sources && sources.length > 0 && (
          <div className="ml-6 mt-1 flex items-center gap-1 text-xs ">
            <span className="font-medium text-gray-400">References:</span>
            {sources.map((s, i) => (
              <a
                key={i}
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
                className="underline text-brand/80 hover:text-brand"
              >
                [{i + 1}]
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
