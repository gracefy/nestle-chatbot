import { BotMessageSquare } from 'lucide-react'
import { clsx } from 'clsx'
import { motion } from 'framer-motion'

interface Props {
  onClick: () => void
}

export const FloatingChatButton = ({ onClick }: Props) => {
  return (
    <motion.div layoutId="chat" className={clsx('fixed bottom-6 right-6 z-50')}>
      <button
        className={clsx(
          'cursor-pointer flex items-center justify-center gap-2 px-4 shadow-md rounded-xl',
          ' w-[140px] md:w-[200px] h-[40px] md:h-[50px] bg-brand text-white text-sm font-semibold',
          'hover:bg-brand-hover transition-all duration-300'
        )}
        onClick={onClick}
        aria-label="Open chat"
      >
        <BotMessageSquare className="w-6 h-6 scale-x-[-1]" />
        <span className="text-xs md:text-sm">Need Help?</span>
      </button>
    </motion.div>
  )
}
