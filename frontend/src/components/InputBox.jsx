import { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { Input } from './ui/input'
import { Button } from './ui/button'
import { Send, Mic, Square } from 'lucide-react'

export default function InputBox({ onSendMessage, onVoiceInput }) {
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const inputRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage?.(input)
      setInput('')
      inputRef.current?.focus()
    }
  }

  const handleVoiceToggle = () => {
    setIsRecording(!isRecording)
    onVoiceInput?.(isRecording)
  }

  const inputVariants = {
    initial: { y: 100, opacity: 0 },
    animate: { 
      y: 0, 
      opacity: 1,
      transition: { 
        duration: 0.5,
        ease: "easeOut"
      }
    }
  }

  const micButtonVariants = {
    idle: { scale: 1 },
    recording: { 
      scale: [1, 1.1, 1],
      transition: { 
        duration: 1.5,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    hover: { scale: 1.05 }
  }

  return (
    <motion.div
      variants={inputVariants}
      initial="initial"
      animate="animate"
      className="fixed bottom-6 left-1/2 transform -translate-x-1/2 w-full max-w-2xl px-4 z-20"
    >
      <div className="relative">
        {/* Main input container */}
        <div className="bg-black/60 backdrop-blur-md border border-cyan-500/30 rounded-full shadow-2xl shadow-cyan-500/20">
          <form onSubmit={handleSubmit} className="flex items-center p-2">
            <Input
              ref={inputRef}
              type="text"
              placeholder="Ask me anything..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 bg-transparent border-none text-white placeholder-gray-400 focus-visible:ring-0 focus-visible:ring-offset-0 text-lg px-4"
            />
            
            <div className="flex items-center gap-2 pr-2">
              {/* Send button */}
              <Button
                type="submit"
                disabled={!input.trim()}
                size="sm"
                className="bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 border-cyan-400/50 rounded-full h-10 w-10 p-0 disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </form>
        </div>

        {/* Floating microphone button */}
        <motion.div
          className="absolute -right-2 -top-2"
          variants={micButtonVariants}
          animate={isRecording ? 'recording' : 'idle'}
          whileHover="hover"
        >
          <Button
            type="button"
            onClick={handleVoiceToggle}
            className={`rounded-full h-14 w-14 shadow-lg ${
              isRecording
                ? 'bg-red-500/80 hover:bg-red-500/90 text-white shadow-red-500/50'
                : 'bg-cyan-500/80 hover:bg-cyan-500/90 text-white shadow-cyan-500/50'
            } backdrop-blur-sm border-2 border-white/20`}
          >
            {isRecording ? (
              <Square className="w-5 h-5" />
            ) : (
              <Mic className="w-5 h-5" />
            )}
          </Button>
        </motion.div>

        {/* Recording indicator */}
        {isRecording && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute -top-16 left-1/2 transform -translate-x-1/2"
          >
            <div className="bg-red-500/90 text-white px-4 py-2 rounded-full text-sm font-medium shadow-lg backdrop-blur-sm">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                Recording...
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input suggestions/shortcuts */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-4 flex justify-center gap-2"
      >
        <div className="text-xs text-gray-500 bg-black/40 px-3 py-1 rounded-full backdrop-blur-sm">
          Press Enter to send
        </div>
        <div className="text-xs text-gray-500 bg-black/40 px-3 py-1 rounded-full backdrop-blur-sm">
          Hold Mic to record
        </div>
      </motion.div>
    </motion.div>
  )
}
