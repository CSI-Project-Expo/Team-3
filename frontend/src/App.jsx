import { useState, useRef, useEffect } from "react"
import "./App.css"

function App() {
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

      <div className="chat-container">
        <div className="chat-history">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              {msg.content}
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
        </div>
      </div>

<div className={`defense-panel ${defenseInfo?.risk_level || ""}`}>
  <h3>🛡 Defense Panel</h3>

  {defenseInfo ? (
    <>
      <p><strong>Final Status:</strong> {defenseInfo.final_status}</p>

      <hr />

      <p><strong>Keyword Layer:</strong></p>
      <p>
        Flagged: {defenseInfo.keyword_flag ? "YES ⚠️" : "NO"}
      </p>
      {defenseInfo.keyword_flag && (
        <p>Reason: {defenseInfo.keyword_reason}</p>
      )}

      <hr />

      <p><strong>AI Judge:</strong></p>
      <p>
        Decision: {defenseInfo.final_status === "SAFE" ? "SAFE" : "UNSAFE"}
      </p>
      {defenseInfo.ai_reason && (
        <p>Reason: {defenseInfo.ai_reason}</p>
      )}
    </>
  ) : (
    <p>No messages yet.</p>
  )}
</div>

    </div>
  )
}

export default App