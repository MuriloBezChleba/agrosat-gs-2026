import { useState } from 'react'
import { api } from '../api.js'
import { RiskBadge } from './RiskBadge.jsx'

export function BatchPanel() {
  const [input, setInput] = useState('')
  const [queue, setQueue] = useState([])
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  function addToQueue() {
    const ids = input.split(/[\n,]+/).map(s => s.trim().toUpperCase()).filter(Boolean)
    setQueue(prev => [...new Set([...prev, ...ids])])
    setInput('')
  }

  function removeFromQueue(id) {
    setQueue(prev => prev.filter(x => x !== id))
  }

  async function processQueue() {
    if (!queue.length) return
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const data = await api.analyzeBatch(queue)
      setResults(data)
      setQueue([])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.root}>
      <h2 style={styles.title}>Processamento em Lote</h2>
      <p style={styles.desc}>IDs separados por vírgula ou linha. Backend usa fila FIFO.</p>

      <div style={styles.inputRow}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="PR-0001, PR-0042, PR-0100"
          rows={3}
          style={styles.textarea}
        />
        <button onClick={addToQueue} style={styles.btnAdd}>Enfileirar</button>
      </div>

      {queue.length > 0 && (
        <div style={styles.queueBox}>
          <div style={styles.queueHeader}>
            <span style={styles.queueLabel}>Fila ({queue.length})</span>
            <button onClick={processQueue} disabled={loading} style={styles.btnProcess}>
              {loading ? 'Processando...' : 'Processar Fila'}
            </button>
          </div>
          <div style={styles.tags}>
            {queue.map(id => (
              <span key={id} style={styles.tag}>
                {id}
                <button onClick={() => removeFromQueue(id)} style={styles.tagRemove}>×</button>
              </span>
            ))}
          </div>
        </div>
      )}

      {error && <div style={styles.error}>{error}</div>}

      {results && (
        <div style={styles.results}>
          <p style={styles.summary}>
            {results.processed} analisadas · {results.errors.length} erros
          </p>
          <table style={styles.table}>
            <thead>
              <tr>
                {['ID', 'Município', 'Cultura', 'NDVI', 'Tendência', 'Risco'].map(h => (
                  <th key={h} style={styles.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results.results.map((r, i) => (
                <tr key={r.property_id} style={i % 2 === 0 ? {} : { background: 'var(--surface2)' }}>
                  <td style={styles.td}><b>{r.property_id}</b></td>
                  <td style={styles.td}>{r.municipality}</td>
                  <td style={styles.td}>{r.culture}</td>
                  <td style={{ ...styles.td, color: 'var(--green)' }}>{r.ndvi_mean}</td>
                  <td style={styles.td}>{r.ndvi_trend}</td>
                  <td style={styles.td}><RiskBadge riskClass={r.risk_class} score={r.risk_score} /></td>
                </tr>
              ))}
            </tbody>
          </table>
          {results.errors.length > 0 && (
            <div style={styles.errList}>
              {results.errors.map(e => (
                <span key={e.id} style={styles.errItem}>{e.id}: {e.error}</span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

const styles = {
  root: { padding: 24, display: 'flex', flexDirection: 'column', gap: 16 },
  title: { fontSize: 18, fontWeight: 700 },
  desc: { color: 'var(--muted)', fontSize: 13 },
  inputRow: { display: 'flex', gap: 10, alignItems: 'flex-start' },
  textarea: {
    flex: 1, background: 'var(--surface2)', border: '1px solid var(--border)',
    borderRadius: 'var(--radius)', color: 'var(--text)', fontSize: 13,
    padding: '8px 10px', resize: 'vertical', fontFamily: 'monospace',
  },
  btnAdd: { background: 'var(--surface2)', color: 'var(--blue)', border: '1px solid var(--blue)', padding: '8px 16px' },
  queueBox: {
    background: 'var(--surface2)', border: '1px solid var(--border)',
    borderRadius: 'var(--radius)', padding: 12, display: 'flex', flexDirection: 'column', gap: 10,
  },
  queueHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  queueLabel: { fontWeight: 600, fontSize: 13 },
  btnProcess: { background: 'var(--accent)', color: '#fff', padding: '6px 18px' },
  tags: { display: 'flex', flexWrap: 'wrap', gap: 6 },
  tag: {
    background: 'var(--blue)22', border: '1px solid var(--blue)',
    color: 'var(--blue)', borderRadius: 4, padding: '2px 8px',
    fontSize: 12, display: 'flex', alignItems: 'center', gap: 4,
  },
  tagRemove: { background: 'transparent', color: 'var(--muted)', padding: '0 2px', fontSize: 14 },
  summary: { color: 'var(--muted)', fontSize: 13 },
  results: { display: 'flex', flexDirection: 'column', gap: 10 },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: 13 },
  th: { padding: '6px 10px', textAlign: 'left', color: 'var(--muted)', borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap' },
  td: { padding: '6px 10px', borderBottom: '1px solid var(--border)22' },
  error: { color: 'var(--red)', background: 'var(--red)11', padding: 10, borderRadius: 6 },
  errList: { display: 'flex', flexDirection: 'column', gap: 4 },
  errItem: { color: 'var(--red)', fontSize: 12 },
}
