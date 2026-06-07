import { useState } from 'react'
import { StatsBar } from './components/StatsBar.jsx'
import { PropertiesTable } from './components/PropertiesTable.jsx'
import { PropertyDetail } from './components/PropertyDetail.jsx'
import { BatchPanel } from './components/BatchPanel.jsx'

const TABS = ['Propriedades', 'Processamento em Lote']

export default function App() {
  const [tab, setTab] = useState(0)
  const [selectedId, setSelectedId] = useState(null)

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <div style={styles.logo}>
          <span style={styles.logoText}>AgroSat</span>
          <span style={styles.logoSub}>Inteligência Agrícola por Satélite · Sentinel-2 / INMET</span>
        </div>
      </header>

      <StatsBar />

      <nav style={styles.nav}>
        {TABS.map((t, i) => (
          <button
            key={t}
            onClick={() => setTab(i)}
            style={{ ...styles.navBtn, ...(tab === i ? styles.navActive : {}) }}
          >
            {t}
          </button>
        ))}
      </nav>

      <main style={styles.main}>
        {tab === 0 && <PropertiesTable onSelect={id => setSelectedId(id)} />}
        {tab === 1 && <BatchPanel />}
      </main>

      <PropertyDetail
        propertyId={selectedId}
        onClose={() => setSelectedId(null)}
      />
    </div>
  )
}

const styles = {
  app: { minHeight: '100vh', display: 'flex', flexDirection: 'column' },
  header: {
    padding: '12px 24px',
    background: 'var(--surface)',
    borderBottom: '1px solid var(--border)',
    display: 'flex', alignItems: 'center',
  },
  logo: { display: 'flex', alignItems: 'baseline', gap: 12 },
  logoText: { fontSize: 20, fontWeight: 800, color: 'var(--green)', letterSpacing: -0.5 },
  logoSub: { fontSize: 12, color: 'var(--muted)' },
  nav: {
    display: 'flex', gap: 0,
    borderBottom: '1px solid var(--border)',
    padding: '0 24px',
    background: 'var(--surface)',
  },
  navBtn: {
    background: 'transparent', color: 'var(--muted)',
    borderRadius: 0, padding: '10px 16px',
    borderBottom: '2px solid transparent',
    fontSize: 13,
  },
  navActive: { color: 'var(--text)', borderBottom: '2px solid var(--green)' },
  main: { flex: 1 },
}
