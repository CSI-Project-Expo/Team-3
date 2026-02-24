import { useEffect, useState } from "react"
import "./Dashboard.css"

function Dashboard() {
  const [logs, setLogs] = useState([])
  const [filter, setFilter] = useState("all")
  const [search, setSearch] = useState("")

  const fetchLogs = async () => {
    try {
      let url = "http://127.0.0.1:8000/logs"

      const params = []
      if (filter === "safe") params.push("safe=true")
      if (filter === "blocked") params.push("safe=false")
      if (search.trim()) params.push(`search=${search}`)

      if (params.length > 0) {
        url += "?" + params.join("&")
      }

      const res = await fetch(url)
      const data = await res.json()
      setLogs(data)
    } catch (err) {
      console.error("Failed to fetch logs")
    }
  }

  useEffect(() => {
    fetchLogs()
  }, [filter])

  const total = logs.length
  const safeCount = logs.filter(l => l.safe).length
  const blockedCount = logs.filter(l => l.safe === false).length

  return (
    <div className="dashboard-container">

      <div className="dashboard-header">
        <div className="title-section">
          <h1>🛡 Security Logs</h1>
          <p className="subtitle">AI Protection Monitoring Console</p>
        </div>

        <div className="controls">
          <input
            type="text"
            placeholder="Search messages..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button onClick={fetchLogs}>Search</button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card total">
          <h3>Total Logs</h3>
          <p>{total}</p>
        </div>

        <div className="stat-card safe">
          <h3>Safe</h3>
          <p>{safeCount}</p>
        </div>

        <div className="stat-card blocked">
          <h3>Blocked</h3>
          <p>{blockedCount}</p>
        </div>
      </div>

      <div className="filter-buttons">
        <button onClick={() => setFilter("all")}>All</button>
        <button onClick={() => setFilter("safe")}>Safe</button>
        <button onClick={() => setFilter("blocked")}>Blocked</button>
      </div>

      <div className="logs-grid">
        {logs.map((log) => (
          <div
            key={log._id}
            className={`log-card ${log.safe ? "safe" : "blocked"}`}
          >
            <div className="log-header">
              <span className={`status ${log.safe ? "safe-text" : "blocked-text"}`}>
                {log.safe ? "SAFE ✓" : "BLOCKED ⚠"}
              </span>
              <span className="time">
                {log.timestamp
                  ? new Date(log.timestamp).toLocaleString()
                  : "No time"}
              </span>
            </div>

            <div className="message">
              {log.message}
            </div>

            {!log.safe && (
              <div className="reason">
                <strong>Reason:</strong> {log.ai_reason}
              </div>
            )}
          </div>
        ))}
      </div>

    </div>
  )
}

export default Dashboard