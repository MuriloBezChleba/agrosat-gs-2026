import { useEffect, useState } from 'react'
import { api } from '../api.js'
import { RiskBadge } from './RiskBadge.jsx'

const COLS = [
  { key: 'property_id', label: 'ID', sortKey: 'id' },
  { key: 'municipality', label: 'Município', sortKey: null },
  { key: 'state', label: 'UF', sortKey: null },
  { key: 'culture', label: 'Cultura', sortKey: null },
  { key: 'area_ha', label: 'Área (ha)', sortKey: null },
  { key: 'obs_count', label: 'Obs.', sortKey: null },
  { key: 'ndvi_mean', label: 'NDVI médio', sortKey: 'ndvi' },
]

export function PropertiesTable({ onSelect }) {
  const [rows, setRows] = useState([])
  const [sortKey, setSortKey] = useState('id')
  const [order, setOrder] = useState('asc')
  const [search, setSearch] = useState('')
  const [searchType, setSearchType] = useState('id')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  function load(sk = sortKey, ord = order) {
    setLoading(true)
    setError(null)
    api.properties(sk, ord)
      .then(d => setRows(d.properties))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  function handleSort(sk) {
    if (!sk) return
    const newOrder = sk === sortKey && order === 'asc' ? 'desc' : 'asc'
    setSortKey(sk); setOrder(newOrder)
    load(sk, newOrder)
  }

  async function handleSearch(e) {
    e.preventDefault()
    if (!search.trim()) { load(); return }
    setLoading(true); setError(null)
    try {
      const data = searchType === 'id'
        ? await api.searchById(search.trim())
        : await api.searchByMunicipality(search.trim())
      setRows(data.results.map(p => ({
        property_id: p.property_id,
        municipality: p.municipality,
        state: p.state,
        culture: p.culture,
        area_ha: p.area_ha,
        obs_count: p.observations?.length ?? '—',
        ndvi_mean: p.observations?.length
          ? +(p.observations.reduce((s, o) => s + o.ndvi_mean, 0) / p.observations.length).toFixed(3)
          : null,
      })))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function clearSearch() { setSearch(''); load() }

  return (
    <div style={styles.root}>
      <form onSubmit={handleSearch} style={styles.searchBar}>
        <select value={searchType} onChange={e => setSearchType(e.target.value)} style={{ width: 160 }}>
          <option value="id">Busca por ID</option>
          <option value="municipality">Busca por Município</option>
        </select>
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder={searchType === 'id' ? 'PR-0042' : 'Cascavel'}
          style={{ flex: 1, maxWidth: 280 }}
        />
        <button type="submit" style={styles.btnSearch}>Buscar</button>
        {search && <button type="button" onClick={clearSearch} style={styles.btnClear}>Limpar</button>}
        {error && <span style={{ color: 'var(--red)', fontSize: 13 }}>{error}</span>}
      </form>

      <div style={styles.tableWrap}>
        <table style={styles.table}>
          <thead>
            <tr>
              {COLS.map(c => (
                <th
                  key={c.key}
                  style={{ ...styles.th, cursor: c.sortKey ? 'pointer' : 'default' }}
                  onClick={() => handleSort(c.sortKey)}
                >
                  {c.label}
                  {c.sortKey === sortKey ? (order === 'asc' ? ' ▲' : ' ▼') : ''}
                </th>
              ))}
              <th style={styles.th}>Ação</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={COLS.length + 1} style={styles.center}>Carregando...</td></tr>
            )}
            {!loading && rows.length === 0 && (
              <tr><td colSpan={COLS.length + 1} style={styles.center}>Nenhuma propriedade encontrada.</td></tr>
            )}
            {!loading && rows.map((row, i) => (
              <tr
                key={row.property_id}
                style={i % 2 === 0 ? styles.rowEven : styles.rowOdd}
                onClick={() => onSelect(row.property_id)}
              >
                <td style={{ ...styles.td, color: 'var(--blue)', fontWeight: 600 }}>{row.property_id}</td>
                <td style={styles.td}>{row.municipality}</td>
                <td style={styles.td}>{row.state}</td>
                <td style={styles.td}>{row.culture}</td>
                <td style={{ ...styles.td, textAlign: 'right' }}>{row.area_ha?.toLocaleString('pt-BR')}</td>
                <td style={{ ...styles.td, textAlign: 'center' }}>{row.obs_count}</td>
                <td style={{ ...styles.td, color: ndviColor(row.ndvi_mean) }}>{row.ndvi_mean ?? '—'}</td>
                <td style={styles.td}>
                  <button
                    onClick={e => { e.stopPropagation(); onSelect(row.property_id) }}
                    style={styles.btnDetail}
                  >
                    Ver
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div style={styles.footer}>{rows.length} propriedade(s)</div>
    </div>
  )
}

function ndviColor(v) {
  if (v == null) return 'var(--muted)'
  if (v >= 0.6) return 'var(--green)'
  if (v >= 0.4) return 'var(--yellow)'
  return 'var(--red)'
}

const styles = {
  root: { display: 'flex', flexDirection: 'column', gap: 12, padding: 24 },
  searchBar: { display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' },
  btnSearch: { background: 'var(--accent)', color: '#fff' },
  btnClear: { background: 'transparent', color: 'var(--muted)', border: '1px solid var(--border)' },
  tableWrap: { overflowX: 'auto', border: '1px solid var(--border)', borderRadius: 'var(--radius)' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: 13 },
  th: {
    padding: '8px 12px', textAlign: 'left', background: 'var(--surface2)',
    color: 'var(--muted)', borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap',
    userSelect: 'none',
  },
  td: { padding: '7px 12px', borderBottom: '1px solid var(--border)22' },
  rowEven: { cursor: 'pointer', transition: 'background .1s' },
  rowOdd: { background: 'var(--surface2)', cursor: 'pointer', transition: 'background .1s' },
  center: { padding: 24, textAlign: 'center', color: 'var(--muted)' },
  footer: { color: 'var(--muted)', fontSize: 12, textAlign: 'right' },
  btnDetail: { background: 'var(--blue)22', color: 'var(--blue)', border: '1px solid var(--blue)', padding: '3px 10px', fontSize: 12 },
}
