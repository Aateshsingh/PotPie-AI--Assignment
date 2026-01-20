import React, { useEffect, useState } from 'react'

function App() {
  const [isOnline, setIsOnline] = useState(navigator.onLine)

  useEffect(() => {
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  if (!isOnline) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh',
        background: '#f5f5f5',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <h1>📡 No Internet Connection</h1>
        <p>Please check your internet connection and try again.</p>
      </div>
    )
  }

  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleReview = async () => {
    if (!code.trim()) {
      setError('Please enter some code to review')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/review`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          language
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to review code')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Failed to review code. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setCode('')
    setResult(null)
    setError(null)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>💻 Code Review Agent</h1>
        <p>AI-powered code analysis and improvement suggestions</p>
      </div>

      <div className="content">
        {/* Input Section */}
        <div className="section">
          <h2>Your Code</h2>
          
          <label htmlFor="language" style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: '#666' }}>
            Programming Language:
          </label>
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
            <option value="csharp">C#</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
          </select>

          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
            rows="15"
            disabled={loading}
          />

          <button onClick={handleReview} disabled={loading || !code.trim()}>
            {loading ? (
              <span className="loading">
                <span className="spinner"></span>
                Analyzing...
              </span>
            ) : (
              '🔍 Review Code'
            )}
          </button>

          <button 
            onClick={handleClear} 
            style={{ 
              background: '#999',
              marginTop: '8px'
            }}
            disabled={loading}
          >
            Clear
          </button>
        </div>

        {/* Output Section */}
        <div className="section">
          <h2>Review Results</h2>

          {error && (
            <div className="error">
              ⚠️ {error}
            </div>
          )}

          {result && (
            <div className="result">
              <div className="review-card">
                <div className={`severity-badge severity-${result.severity_level || 'low'}`}>
                  Severity: {(result.severity_level || 'low').toUpperCase()}
                </div>
                
                <div className="review-text">
                  {result.review}
                </div>

                {result.suggestions && result.suggestions.length > 0 && (
                  <>
                    <h3 style={{ fontSize: '14px', fontWeight: '600', marginTop: '16px', marginBottom: '8px', color: '#333' }}>
                      📋 Suggestions:
                    </h3>
                    <ul className="suggestions-list">
                      {result.suggestions.map((suggestion, index) => (
                        <li key={index}>{suggestion}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </div>
          )}

          {!result && !error && (
            <div style={{ 
              color: '#999', 
              textAlign: 'center', 
              padding: '40px 20px',
              fontSize: '14px'
            }}>
              Your code review will appear here
            </div>
          )}
        </div>
      </div>

      <div className="footer">
        <p>Powered by Pydantic AI & OpenRouter | © 2026 Code Review Agent</p>
      </div>
    </div>
  )
}

export default App
