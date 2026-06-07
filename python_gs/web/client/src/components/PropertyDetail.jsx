import { useEffect, useState } from 'react'
import { api } from '../api.js'
import { NDVIChart } from './NDVIChart.jsx'
import { RiskBadge } from './RiskBadge.jsx'

export function PropertyDetail({ propertyId, onClose }) {
  const [prop, setProp] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!propertyId) return
    setError(null)
    Promise.all([
      api.property(propertyId),
      api.analyze(propertyId),
    ])
      .then(([p, a]) => { setProp(p); setAnalysis(a) })
      .catch(e => setError(e.message))
  }, [propertyId])

  if (!propertyId) return null

  return (
    <div style={styles.overlay} onClick={e => e.target === e.currentTarget && onClose()}>
      <div style={styles.panel}>
        <div style={styles.header}>
          <div>
            <h2 style={styles.title}>{propertyId}</h2>
            {prop && <span style={styles.sub}>{prop.municipality}/{prop.state} — {prop.culture} — {prop.area_ha.toLocaleString('pt-BR')} ha</span>}
          </div>
          <button onClick={onClose} style={styles.close}>✕</button>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {analysis && (
          <div style={styles.riskCard}>
            <div style={styles.riskRow}>
              <RiskBadge riskClass={analysis.risk_class} score={analysis.risk_score} />
              <span style={styles.trend}>Tendência: <b>{analysis.ndvi_trend}</b></span>
              <span style={{ color: 'var(--muted)' }}>NDVI médio: <b style={{ color: 'var(--green)' }}>{analysis.ndvi_mean}</b></span>
            </div>
            <p style={styles.rec}>{analysis.recommendation}</p>
          </div>
        )}

        {prop?.observations?.length > 0 && (
          <div style={styles.chartBox}>
            <h3 style={styles.sectionTitle}>Série Temporal NDVI / EVI — Sentinel-2</h3>
            <NDVIChart observations={prop.observations} />
          </div>
        )}

        {prop?.observations?.length > 0 && (
          <div style={styles.tableBox}>
            <h3 style={styles.sectionTitle}>Observações Satelitais</h3>
            <div style={styles.tableScroll}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    {['Data', 'NDVI', 'EVI', 'Nuvem %', 'Satélite'].map(h => (
                      <th key={h} style={styles.th}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[...prop.observations].reverse().map((o, i) => (
                    <tr key={i} style={i % 2 === 0 ? {} : { background: 'var(--surface2)' }}>
                      <td style={styles.td}>{o.obs_date}</td>
                      <td style={{ ...styles.td, color: ndviColor(o.ndvi_mean) }}>{o.ndvi_mean.toFixed(3)}</td>
                      <td style={styles.td}>{o.evi_mean.toFixed(3)}</td>
                      <td style={styles.td}>{o.cloud_cover_pct.toFixed(1)}</td>
                      <td style={{ ...styles.td, color: 'var(--muted)' }}>{o.satellite}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {!prop && !error && <div style={styles.loading}>Carregando...</div>}
      </div>
    </div>
  )
}

function ndviColor(v) {
  if (v >= 0.6) return 'var(--green)'
  if (v >= 0.4) return 'var(--yellow)'
  return 'var(--red)'
}

const styles = {
  overlay: {
    position: 'fixed', inset: 0, background: '#000000aa',
    display: 'flex', justifyContent: 'flex-end', zIndex: 100,
  },
  panel: {
    width: 560, background: 'var(--surface)', borderLeft: '1px solid var(--border)',
    overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 16, padding: 24,
  },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' },
  title: { fontSize: 20, fontWeight: 700 },
  sub: { color: 'var(--muted)', fontSize: 13 },
  close: { background: 'transparent', color: 'var(--muted)', fontSize: 18, padding: '2px 6px' },
  riskCard: {
    background: 'var(--surface2)', border: '1px solid var(--border)',
    borderRadius: 'var(--radius)', padding: 14, display: 'flex', flexDirection: 'column', gap: 8,
  },
  riskRow: { display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' },
  trend: { color: 'var(--text)', fontSize: 13 },
  rec: { color: 'var(--muted)', fontSize: 13, fontStyle: 'italic' },
  chartBox: { display: 'flex', flexDirection: 'column', gap: 8 },
  tableBox: { display: 'flex', flexDirection: 'column', gap: 8 },
  sectionTitle: { fontSize: 13, fontWeight: 600, color: 'var(--muted)' },
  tableScroll: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: 13 },
  th: { padding: '6px 10px', textAlign: 'left', color: 'var(--muted)', borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap' },
  td: { padding: '5px 10px', borderBottom: '1px solid var(--border)22' },
  loading: { color: 'var(--muted)', textAlign: 'center', padding: 32 },
  error: { color: 'var(--red)', background: 'var(--red)11', padding: 10, borderRadius: 6 },
}
