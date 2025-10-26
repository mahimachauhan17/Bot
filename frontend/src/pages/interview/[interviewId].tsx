import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Webcam from 'react-webcam'

interface InterviewRoomProps {}

export default function InterviewRoom({}: InterviewRoomProps) {
  const router = useRouter()
  const { interviewId } = router.query
  
  const [isConnected, setIsConnected] = useState(false)
  const [interviewStarted, setInterviewStarted] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState<string>('')
  const [showCaptions, setShowCaptions] = useState(true)
  const [audioEnabled, setAudioEnabled] = useState(true)
  const [videoEnabled, setVideoEnabled] = useState(true)
  const [messages, setMessages] = useState<Array<{ sender: string; text: string; timestamp: Date }>>([])
  const [inputMessage, setInputMessage] = useState('')
  
  const webcamRef = useRef<Webcam>(null)
  const wsRef = useRef<WebSocket | null>(null)
  
  useEffect(() => {
    if (!interviewId) return
    
    // Initialize WebSocket connection
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL}/interview/${interviewId}/`)
    wsRef.current = ws
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleWebSocketMessage(data)
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
    }
    
    return () => {
      ws.close()
    }
  }, [interviewId])
  
  const handleWebSocketMessage = (data: any) => {
    switch (data.type) {
      case 'connection_established':
        console.log('Connection confirmed:', data.message)
        break
      
      case 'interview_started':
        setInterviewStarted(true)
        setCurrentQuestion(data.message)
        addMessage('AI', data.message)
        break
      
      case 'message':
        addMessage(data.sender, data.content)
        if (data.sender === 'ai') {
          setCurrentQuestion(data.content)
        }
        break
      
      case 'interview_ended':
        setInterviewStarted(false)
        addMessage('System', 'Interview has ended. Thank you!')
        break
      
      default:
        console.log('Unknown message type:', data.type)
    }
  }
  
  const addMessage = (sender: string, text: string) => {
    setMessages(prev => [...prev, { sender, text, timestamp: new Date() }])
  }
  
  const startInterview = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'start_interview'
      }))
    }
  }
  
  const sendMessage = () => {
    if (!inputMessage.trim() || !wsRef.current) return
    
    wsRef.current.send(JSON.stringify({
      type: 'candidate_message',
      content: inputMessage
    }))
    
    addMessage('You', inputMessage)
    setInputMessage('')
  }
  
  const endInterview = () => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({
        type: 'end_interview'
      }))
    }
  }
  
  const toggleAudio = () => {
    setAudioEnabled(!audioEnabled)
    // TODO: Implement actual mic mute/unmute
  }
  
  const toggleVideo = () => {
    setVideoEnabled(!videoEnabled)
    // TODO: Implement actual video enable/disable
  }
  
  return (
    <>
      <Head>
        <title>Interview Room | Interviewer AI</title>
      </Head>
      
      <div className="min-h-screen bg-gray-900 flex flex-col">
        {/* Header */}
        <header className="bg-gray-800 text-white p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div>
              <h1 className="text-xl font-bold">Interview in Progress</h1>
              <p className="text-sm text-gray-400">Interview ID: {interviewId}</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
                <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
                <span className="text-sm">{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>
            </div>
          </div>
        </header>
        
        {/* Main Content */}
        <main className="flex-1 flex">
          {/* Video Section */}
          <div className="flex-1 p-6 space-y-4">
            {/* AI Avatar / Question Display */}
            <div className="bg-gray-800 rounded-lg p-6 text-white">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-2xl">
                  🤖
                </div>
                <div>
                  <h3 className="font-semibold">AI Interviewer</h3>
                  <p className="text-sm text-gray-400">Asking questions</p>
                </div>
              </div>
              
              {currentQuestion && (
                <div className="bg-gray-700 rounded p-4 mt-4">
                  <p className="text-lg">{currentQuestion}</p>
                </div>
              )}
            </div>
            
            {/* Candidate Video */}
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="aspect-video bg-black rounded overflow-hidden">
                {videoEnabled ? (
                  <Webcam
                    ref={webcamRef}
                    audio={audioEnabled}
                    mirrored
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">
                    <div className="text-center">
                      <div className="text-6xl mb-4">📷</div>
                      <p>Camera is off</p>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Controls */}
              <div className="mt-4 flex justify-center space-x-4">
                <button
                  onClick={toggleAudio}
                  className={`p-4 rounded-full ${audioEnabled ? 'bg-gray-700' : 'bg-red-600'} hover:opacity-80 transition`}
                >
                  {audioEnabled ? '🎤' : '🔇'}
                </button>
                <button
                  onClick={toggleVideo}
                  className={`p-4 rounded-full ${videoEnabled ? 'bg-gray-700' : 'bg-red-600'} hover:opacity-80 transition`}
                >
                  {videoEnabled ? '📹' : '📷'}
                </button>
                <button
                  onClick={() => setShowCaptions(!showCaptions)}
                  className="p-4 rounded-full bg-gray-700 hover:opacity-80 transition"
                >
                  💬
                </button>
                {interviewStarted ? (
                  <button
                    onClick={endInterview}
                    className="px-6 py-3 rounded-full bg-red-600 hover:bg-red-700 transition font-semibold"
                  >
                    End Interview
                  </button>
                ) : (
                  <button
                    onClick={startInterview}
                    className="px-6 py-3 rounded-full bg-green-600 hover:bg-green-700 transition font-semibold"
                    disabled={!isConnected}
                  >
                    Start Interview
                  </button>
                )}
              </div>
            </div>
          </div>
          
          {/* Chat Sidebar */}
          <aside className="w-96 bg-gray-800 p-4 flex flex-col">
            <h3 className="text-white font-semibold mb-4">Chat & Transcript</h3>
            
            {/* Messages */}
            <div className="flex-1 overflow-y-auto space-y-3 mb-4">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg ${
                    msg.sender === 'You' ? 'bg-blue-600 text-white ml-4' : 'bg-gray-700 text-white mr-4'
                  }`}
                >
                  <div className="text-xs opacity-75 mb-1">{msg.sender}</div>
                  <div className="text-sm">{msg.text}</div>
                  <div className="text-xs opacity-50 mt-1">
                    {msg.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              ))}
            </div>
            
            {/* Input */}
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your answer..."
                className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={!interviewStarted}
              />
              <button
                onClick={sendMessage}
                disabled={!interviewStarted || !inputMessage.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Send
              </button>
            </div>
          </aside>
        </main>
      </div>
    </>
  )
}
