import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const checkMessage = async () => {
    if (!message.trim()) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/check-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({
        safe: false,
        layer: 'error',
        reason: 'Failed to connect to backend: ' + error.message,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ Dual-Layer Defense System</h1>
        <p>AI-Powered Content Safety Scanner</p>
      </header>

      <main className="container">
        <div className="chat-box">
          <textarea
            className="message-input"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Enter message to scan..."
            rows={5}
          />
          
          <button 
            className="scan-button" 
            onClick={checkMessage}
            disabled={loading || !message.trim()}
          >
            {loading ? 'Scanning...' : 'Scan Message'}
          </button>
        </div>

        {result && (
          <div className={`result-box ${result.safe ? 'safe' : 'unsafe'}`}>
            <div className="status-indicator">
              <span className={`status-light ${result.safe ? 'green' : 'red'}`}></span>
              <h2>{result.safe ? '✅ Safe' : '⚠️ Unsafe'}</h2>
            </div>
            <div className="result-details">
              <p><strong>Layer:</strong> {result.layer}</p>
              <p><strong>Reason:</strong> {result.reason}</p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
