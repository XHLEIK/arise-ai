import { motion, AnimatePresence } from 'framer-motion'
import { Card, CardContent } from './ui/card'
import { ScrollArea } from './ui/scroll-area'
import { Bot, User } from 'lucide-react'

export default function ChatLog({ messages, isVisible }) {
  const containerVariants = {
    hidden: { 
      opacity: 0, 
      x: -300,
      transition: { duration: 0.3 }
    },
    visible: { 
      opacity: 1, 
      x: 0,
      transition: { 
        duration: 0.5,
        ease: "easeOut",
        staggerChildren: 0.1
      }
    }
  }

  const messageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.3 }
    }
  }

  // Sample messages for demonstration
  const sampleMessages = messages || [
    { id: 1, type: 'user', content: 'Hello, AI assistant!', timestamp: new Date() },
    { id: 2, type: 'ai', content: 'Hello! How can I assist you today?', timestamp: new Date() },
    { id: 3, type: 'user', content: 'What can you help me with?', timestamp: new Date() },
  ]

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          exit="hidden"
          className="fixed left-4 top-4 bottom-4 w-80 z-10"
        >
          <Card className="h-full bg-black/60 border-cyan-500/30 backdrop-blur-md">
            <CardContent className="p-4 h-full flex flex-col">
              <div className="flex items-center gap-2 mb-4">
                <Bot className="w-5 h-5 text-cyan-400" />
                <h3 className="text-cyan-400 font-medium">Chat History</h3>
              </div>
              
              <ScrollArea className="flex-1">
                <div className="space-y-3">
                  <AnimatePresence>
                    {sampleMessages.map((message) => (
                      <motion.div
                        key={message.id}
                        variants={messageVariants}
                        initial="hidden"
                        animate="visible"
                        exit="hidden"
                        layout
                      >
                        <Card className={`p-3 ${
                          message.type === 'user' 
                            ? 'bg-blue-500/20 border-blue-400/30 ml-4' 
                            : 'bg-cyan-500/20 border-cyan-400/30 mr-4'
                        }`}>
                          <div className="flex items-start gap-2">
                            {message.type === 'user' ? (
                              <User className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
                            ) : (
                              <Bot className="w-4 h-4 text-cyan-400 mt-0.5 flex-shrink-0" />
                            )}
                            <div className="flex-1">
                              <p className={`text-sm ${
                                message.type === 'user' 
                                  ? 'text-blue-100' 
                                  : 'text-cyan-100'
                              }`}>
                                {message.content}
                              </p>
                              <span className="text-xs text-gray-400 mt-1 block">
                                {new Date(message.timestamp).toLocaleTimeString()}
                              </span>
                            </div>
                          </div>
                        </Card>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
              </ScrollArea>
              
              <div className="mt-4 pt-3 border-t border-cyan-500/20">
                <p className="text-xs text-gray-400 text-center">
                  {sampleMessages.length} messages
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
