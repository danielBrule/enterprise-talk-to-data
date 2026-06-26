import { useState, useRef, useEffect } from 'react'
import './App.css'

const ROLES = ['analyst', 'editor', 'admin']

async function askApi({ question, sessionId, conversationHistory, role }) {
  const res = await fetch('/api/v0/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Role': role,
    },
    body: JSON.stringify({
      question,
      session_id: sessionId || undefined,
      conversation_history: conversationHistory,
    }),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

async function feedbackApi(traceId, rating) {
  await fetch('/api/v0/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ trace_id: traceId, rating }),
  })
}

function ThinkingDots() {
  return (
    <div className="flex justify-start">
      <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
        <div className="flex gap-1 items-center h-4">
          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" />
        </div>
      </div>
    </div>
  )
}

function Message({ msg, onFeedback }) {
  if (msg.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] bg-blue-600 text-white rounded-2xl rounded-br-sm px-4 py-3 text-sm leading-relaxed">
          {msg.text}
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-[80%] space-y-1.5">

        {/* Answer bubble */}
        <div className={`rounded-2xl rounded-bl-sm px-4 py-3 text-sm leading-relaxed ${
          msg.refused
            ? 'bg-amber-50 border border-amber-200 text-amber-800'
            : 'bg-white border border-gray-200 text-gray-800 shadow-sm'
        }`}>
          {msg.text}
        </div>

        {/* Metadata row */}
        <div className="flex items-center gap-3 px-1 flex-wrap">
          {!msg.refused && (
            <>
              {msg.sourceView && (
                <span className="text-xs text-gray-400">
                  {msg.sourceView.replace('analytics.', '')}
                </span>
              )}
              {msg.filtersApplied?.length > 0 && (
                <span className="text-xs text-gray-400 truncate max-w-[200px]">
                  {msg.filtersApplied.join(' · ')}
                </span>
              )}
              {msg.rowCount != null && (
                <span className="text-xs text-gray-400">{msg.rowCount} rows</span>
              )}
              {msg.confidence != null && (
                <span className="text-xs text-gray-400">
                  {Math.round(msg.confidence * 100)}% conf.
                </span>
              )}
            </>
          )}
          <div className="flex gap-1 ml-auto">
            <button
              onClick={() => onFeedback(msg.id, msg.traceId, 1)}
              title="Good answer"
              className={`text-sm transition-opacity ${msg.feedback === 1 ? 'opacity-100' : 'opacity-25 hover:opacity-60'}`}
            >👍</button>
            <button
              onClick={() => onFeedback(msg.id, msg.traceId, -1)}
              title="Bad answer"
              className={`text-sm transition-opacity ${msg.feedback === -1 ? 'opacity-100' : 'opacity-25 hover:opacity-60'}`}
            >👎</button>
          </div>
        </div>

        {/* SQL expandable */}
        {msg.sql && (
          <details className="px-1">
            <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-600 select-none">
              Show SQL
            </summary>
            <pre className="mt-1.5 text-xs bg-gray-900 text-green-400 rounded-lg p-3 overflow-x-auto whitespace-pre-wrap">
              {msg.sql}
            </pre>
          </details>
        )}

      </div>
    </div>
  )
}

export default function App() {
  const [role, setRole] = useState('analyst')
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [turns, setTurns] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function send() {
    const q = input.trim()
    if (!q || loading) return
    setInput('')
    setLoading(true)

    setMessages(prev => [...prev, {
      id: crypto.randomUUID(),
      role: 'user',
      text: q,
    }])

    try {
      const data = await askApi({ question: q, sessionId, conversationHistory: turns, role })

      setSessionId(data.session_id || sessionId)

      const assistantMsg = {
        id: crypto.randomUUID(),
        role: 'assistant',
        text: data.refused ? (data.refusal_reason ?? 'Refused.') : (data.answer ?? ''),
        refused: data.refused,
        traceId: data.trace?.trace_id ?? null,
        sql: data.sql ?? null,
        sourceView: data.source_view ?? null,
        filtersApplied: data.filters_applied ?? [],
        rowCount: data.row_count ?? null,
        confidence: data.confidence ?? null,
        feedback: null,
      }
      setMessages(prev => [...prev, assistantMsg])

      if (!data.refused) {
        setTurns(prev => [...prev, {
          question: q,
          sql: data.sql ?? null,
          answer: data.answer ?? null,
        }])
      }
    } catch {
      setMessages(prev => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        text: 'Could not reach the backend. Make sure the server is running on port 8000.',
        refused: true,
        traceId: null,
        sql: null,
        filtersApplied: [],
        feedback: null,
      }])
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  async function handleFeedback(msgId, traceId, rating) {
    if (!traceId) return
    setMessages(prev => prev.map(m => m.id === msgId ? { ...m, feedback: rating } : m))
    try { await feedbackApi(traceId, rating) } catch { /* silent */ }
  }

  function handleRoleChange(newRole) {
    setRole(newRole)
    setMessages([])
    setTurns([])
    setSessionId(null)
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">

      {/* Top bar */}
      <header className="flex items-center justify-between px-6 py-3 bg-white border-b border-gray-200 shrink-0">
        <div>
          <h1 className="text-base font-semibold text-gray-900 leading-tight">Talk to Data</h1>
          <p className="text-xs text-gray-400">Newspaper analytics · governed by approved views</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">Role</span>
          <select
            value={role}
            onChange={e => handleRoleChange(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {ROLES.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-2xl mx-auto space-y-4">

          {messages.length === 0 && !loading && (
            <div className="text-center text-gray-400 mt-24 space-y-2">
              <p className="text-3xl">📊</p>
              <p className="text-sm">Ask a question about articles, keywords, contributors or ingestion errors.</p>
              <p className="text-xs text-gray-300">Signed in as <span className="font-medium">{role}</span></p>
            </div>
          )}

          {messages.map(msg => (
            <Message key={msg.id} msg={msg} onFeedback={handleFeedback} />
          ))}

          {loading && <ThinkingDots />}
          <div ref={bottomRef} />
        </div>
      </main>

      {/* Input bar */}
      <footer className="shrink-0 bg-white border-t border-gray-200 px-4 py-3">
        <div className="max-w-2xl mx-auto flex gap-2">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your data… (Enter to send)"
            rows={1}
            className="flex-1 resize-none rounded-xl border border-gray-200 px-4 py-2.5 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 leading-relaxed"
          />
          <button
            onClick={send}
            disabled={!input.trim() || loading}
            className="shrink-0 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-100 disabled:text-gray-400 text-white rounded-xl px-4 py-2.5 text-sm font-medium transition-colors"
          >
            Send
          </button>
        </div>
        {sessionId && (
          <p className="text-center text-xs text-gray-300 mt-1.5">
            session {sessionId.slice(0, 8)}
          </p>
        )}
      </footer>

    </div>
  )
}
