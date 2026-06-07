import { useEffect, useState } from 'react'
import { api } from '../api.js'

export function StatsBar() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.stats().then(setStats).catch(console.error)
  }, [])

  if (!stats) return <div style={styles.bar}><span style={styles.muted}>Carregando...</span></div>

  return (
    <div style={styles.bar}>
      <Stat label="Propriedades" value={stats.total} color="var(--blue)" />
      <Stat label="NDVI Médio" value={stats.avg_ndvi} color="var(--green)" />
      <Stat label="Risco ALTO" value={stats.risk_alto} color="var(--red)" />
      <Stat label="Risco MÉDIO" value={stats.risk_medio} color="var(--yellow)" />
      <Stat label="Risco BAIXO" value={stats.risk_baixo} color="var(--green)" />
    </div>
  )
}

function Stat({ label, value, color }) {
  return (
    <div style={styles.stat}>
      <span style={{ ...styles.value, color }}>{value}</span>
      <span style={styles.label}>{label}</span>
    </div>
  )
}

const styles = {
  bar: {
    display: 'flex', gap: 2, padding: '12px 24px',
    background: 'var(--surface)', borderBottom: '1px solid var(--border)',
  },
  stat: {
    display: 'flex', flexDirection: 'column', alignItems: 'center',
    padding: '6px 20px', borderRadius: 'var(--radius)',
    background: 'var(--surface2)', minWidth: 100,
  },
  value: { fontSize: 22, fontWeight: 700, lineHeight: 1.2 },
  label: { fontSize: 11, color: 'var(--muted)', marginTop: 2 },
  muted: { color: 'var(--muted)', fontSize: 13 },
}
