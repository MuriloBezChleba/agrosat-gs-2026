const COLORS = { BAIXO: '#3fb950', MÉDIO: '#d29922', ALTO: '#f85149' }

export function RiskBadge({ riskClass, score }) {
  const color = COLORS[riskClass] ?? '#8b949e'
  return (
    <span style={{
      background: color + '22',
      border: `1px solid ${color}`,
      color,
      borderRadius: 4,
      padding: '2px 8px',
      fontWeight: 600,
      fontSize: 12,
      whiteSpace: 'nowrap',
    }}>
      {riskClass}{score != null ? ` ${score}` : ''}
    </span>
  )
}
