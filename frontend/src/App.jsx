import { useState, useRef, useEffect } from "react"
import ReactMarkdown from "react-markdown"
import "./App.css"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Dashboard from "./Dashboard"

function ChatPage() {
  const [message, setMessage] = useState("")
  const [chatHistory, setChatHistory] = useState([])
  const [defenseInfo, setDefenseInfo] = useState(null)
  const [loading, setLoading] = useState(false)

  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [chatHistory])

  const sendMessage = async () => {
    if (!message.trim() || loading) return

    const userMessage = message
    setMessage("")
    setLoading(true)

    // Show user message immediately
   // Add user message + thinking bubble together
setChatHistory(prev => [
  ...prev,
  { role: "user", content: userMessage },
  { role: "thinking", content: "AI is thinking..." }
])

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      })

      const data = await response.json()

      setChatHistory(prev => {
        const withoutThinking = prev.slice(0, -1)

        if (data.safe) {
          return [
            ...withoutThinking,
            { role: "ai", content: data.response }
          ]
        } else {
          const neutralReplies = [
            "I'm sorry, I can’t assist with that request.",
            "I’m unable to provide that information.",
            "That request cannot be fulfilled.",
            "Let’s try a different question."
          ]

          const randomReply =
            neutralReplies[Math.floor(Math.random() * neutralReplies.length)]

          return [
            ...withoutThinking,
            { role: "ai", content: randomReply }
          ]
        }
      })

      let riskLevel = "green"

if (!data.safe) {
  riskLevel = "red"
} else if (data.keyword_flag) {
  riskLevel = "yellow"
}

setDefenseInfo({
  final_status: data.safe ? "SAFE" : "BLOCKED",
  risk_level: riskLevel,
  blocked_by: data.blocked_by,
  ai_reason: data.reason,
  keyword_flag: data.keyword_flag,
  keyword_reason: data.keyword_reason
})

    } catch (error) {
      setChatHistory(prev => {
        const withoutThinking = prev.slice(0, -1)
        return [
          ...withoutThinking,
          { role: "ai", content: "Connection error. Backend unreachable." }
        ]
      })
    }

    setLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app-container">
      <div className="app-background"></div>

      <div className="chat-container">
        <div className="chat-header">
          <div className="chat-header-icon">🤖</div>
          <div className="chat-header-text">
            <span className="chat-title">Protected AI Assistant</span>
            <span className="chat-subtitle">Secured by Multi-Layer Defense</span>
          </div>
          <div className="status-indicator"></div>
        </div>
        <div className="chat-history">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              {msg.role === "thinking" ? (
  <span className="typing">
    <span></span>
    <span></span>
    <span></span>
  </span>
) : msg.role === "ai" ? (
  <ReactMarkdown>{msg.content}</ReactMarkdown>
) : (
  msg.content
)}  
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>

        <div className="input-container">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message Protected AI..."
          />
          <button className="send-btn" onClick={sendMessage} disabled={loading || !message.trim()}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>

<div className={`defense-panel ${defenseInfo?.risk_level || ""}`}>
  <div className="defense-header">
    <div className="defense-icon">🛡</div>
    <h3>Defense Panel</h3>
  </div>

  {defenseInfo ? (
    <>
      <div className="defense-section status-section">
        <div className="section-label">Final Status</div>
        <div className={`status-badge ${defenseInfo.final_status.toLowerCase()}`}>
          {defenseInfo.final_status}
        </div>
      </div>

      <div className="defense-divider"></div>

      <div className="defense-section">
        <div className="section-label">
          <span className="layer-icon">🔍</span>
          Keyword Layer
        </div>
        <div className="section-content">
          <div className={`flag-indicator ${defenseInfo.keyword_flag ? 'flagged' : 'clear'}`}>
            {defenseInfo.keyword_flag ? "FLAGGED ⚠️" : "CLEAR ✓"}
          </div>
          {defenseInfo.keyword_flag && (
            <div className="reason-text">{defenseInfo.keyword_reason}</div>
          )}
        </div>
      </div>

      <div className="defense-divider"></div>

      <div className="defense-section">
        <div className="section-label">
          <span className="layer-icon">🧠</span>
          AI Judge
        </div>
        <div className="section-content">
          <div className={`decision-indicator ${defenseInfo.final_status === "SAFE" ? 'safe' : 'unsafe'}`}>
            {defenseInfo.final_status === "SAFE" ? "SAFE" : "UNSAFE"}
          </div>
          {defenseInfo.ai_reason && (
            <div className="reason-text">{defenseInfo.ai_reason}</div>
          )}
        </div>
      </div>
    </>
  ) : (
    <div className="empty-state">
      <div className="empty-icon">💬</div>
      <p>No messages yet.</p>
      <span>Send a message to see defense analysis</span>
    </div>
  )}
</div>

    </div>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  )
}

export default App