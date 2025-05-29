import { BotMessageSquare } from 'lucide-react'
import { clsx } from 'clsx'

interface Props {
  onClick: () => void
}

export const FloatingChatButton = ({ onClick }: Props) => {
  return (
    <button
      className={clsx(
        'cursor-pointer flex items-center justify-center gap-2 px-4 shadow-md rounded-xl',
        ' w-[140px] md:w-[200px] h-[40px] md:h-[50px] bg-brand/80 text-white text-sm font-semibold',
        'hover:bg-brand-hover transition-all duration-300'
      )}
      onClick={onClick}
      aria-label="Open chat"
    >
      <BotMessageSquare className="w-6 h-6 scale-x-[-1]" />
      <span className="text-xs md:text-sm">Need Help?</span>
    </button>
  )
}
