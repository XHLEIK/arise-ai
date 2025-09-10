import { useState, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'
import { motion } from 'framer-motion'
import Sphere from './components/Sphere'
import Particles from './components/Particles'
import ChatLog from './components/ChatLog'
import InputBox from './components/InputBox'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [showChatLog, setShowChatLog] = useState(false)

  const handleSendMessage = (message) => {
    const newMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
    
    // Show chat log when first message is sent
    if (!showChatLog) {
      setShowChatLog(true)
    }
    
    // Simulate AI response (replace with actual AI integration later)
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: `I received your message: "${message}". This is a placeholder response.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiResponse])
    }, 1000)
  }

  const handleVoiceInput = (isRecording) => {
    // Placeholder for voice input handling
    console.log('Voice recording:', isRecording)
  }

  return (
    <div className="w-full h-screen overflow-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 relative">
      {/* Background gradient overlay */}
      <div className="absolute inset-0 bg-gradient-radial from-transparent via-cyan-900/10 to-slate-900/90" />
      
      {/* 3D Scene */}
      <div className="absolute inset-0">
        <Canvas
          camera={{ 
            position: [0, 0, 8], 
            fov: 60,
            near: 0.1,
            far: 1000 
          }}
          gl={{ 
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
          }}
        >
          <Suspense fallback={null}>
            {/* Lighting */}
            <ambientLight intensity={0.2} />
            <directionalLight 
              position={[10, 10, 5]} 
              intensity={1}
              color="#ffffff"
            />
            
            {/* Environment for reflections */}
            <Environment preset="night" />
            
            {/* Particles background */}
            <Particles count={100} />
            
            {/* Main glowing sphere */}
            <Sphere />
            
            {/* Camera controls (disabled for production, useful for development) */}
            {/* <OrbitControls enableZoom={false} enablePan={false} /> */}
          </Suspense>
        </Canvas>
      </div>

      {/* UI Overlay */}
      <div className="relative z-10 h-full flex flex-col">
        {/* Chat Log */}
        <ChatLog 
          messages={messages} 
          isVisible={showChatLog}
        />
        
        {/* Status indicator */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="absolute top-6 right-6"
        >
          <div className="bg-black/40 backdrop-blur-md rounded-full px-4 py-2 border border-cyan-500/30">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse" />
              <span className="text-cyan-400 text-sm font-medium">AI Assistant Ready</span>
            </div>
          </div>
        </motion.div>

        {/* Toggle chat log button */}
        {messages.length > 0 && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            onClick={() => setShowChatLog(!showChatLog)}
            className="absolute top-20 left-6 bg-cyan-500/20 hover:bg-cyan-500/30 backdrop-blur-md rounded-full p-3 border border-cyan-400/30 transition-colors"
          >
            <motion.div
              animate={{ rotate: showChatLog ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <svg 
                className="w-5 h-5 text-cyan-400" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </motion.div>
          </motion.button>
        )}

        {/* Welcome text */}
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.5 }}
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center"
          >
            <h1 className="text-4xl font-light text-white mb-4">
              Welcome to <span className="text-cyan-400 font-medium">Arise AI</span>
            </h1>
            <p className="text-gray-300 text-lg">
              Your intelligent assistant is ready to help
            </p>
          </motion.div>
        )}

        {/* Input Box */}
        <InputBox 
          onSendMessage={handleSendMessage}
          onVoiceInput={handleVoiceInput}
        />
      </div>
    </div>
  )
}

export default App
