import express from 'express'
import cors from 'cors'
import { loadAll } from './lib/loader.js'
import { quickSort, binarySearch, linearSearch } from './lib/algorithms.js'
import { calculateRisk } from './lib/risk.js'

const app = express()
app.use(cors())
app.use(express.json())

// Carrega dados na inicialização
let db
try {
  db = loadAll()
  console.log(`[AgroSat] ${db.properties.length} propriedades carregadas`)
} catch (err) {
  console.error('[AgroSat] Erro ao carregar dados:', err.message)
  process.exit(1)
}

// ── GET /api/properties ────────────────────────────────────────────────────
// Query params: sort=ndvi|risk|id  order=asc|desc
app.get('/api/properties', (req, res) => {
  const { sort = 'id', order = 'asc' } = req.query

  let list = [...db.properties].map(p => ({
    property_id: p.property_id,
    municipality: p.municipality,
    state: p.state,
    culture: p.culture,
    area_ha: p.area_ha,
    obs_count: p.observations.length,
    ndvi_mean: p.observations.length
      ? +(p.observations.reduce((s, o) => s + o.ndvi_mean, 0) / p.observations.length).toFixed(3)
      : null,
    latest_ndvi: p.observations.at(-1)?.ndvi_mean ?? null,
    latest_date: p.observations.at(-1)?.obs_date ?? null,
  }))

  const keyFns = {
    ndvi: p => p.ndvi_mean ?? -1,
    id:   p => p.property_id,
    risk: p => p.property_id, // placeholder; real risk via /api/analysis
  }
  quickSort(list, keyFns[sort] ?? keyFns.id)
  if (order === 'desc') list.reverse()

  res.json({ total: list.length, properties: list })
})

// ── GET /api/properties/:id ────────────────────────────────────────────────
app.get('/api/properties/:id', (req, res) => {
  const prop = binarySearch(db.sortedById, req.params.id.toUpperCase(), p => p.property_id)
  if (!prop) return res.status(404).json({ error: 'Propriedade não encontrada' })
  res.json(prop)
})

// ── GET /api/search ────────────────────────────────────────────────────────
// ?id=PR-0042           → busca binária por ID
// ?municipality=cascavel → busca linear por município
app.get('/api/search', (req, res) => {
  const { id, municipality } = req.query

  if (id) {
    const found = binarySearch(db.sortedById, id.toUpperCase(), p => p.property_id)
    return res.json({ type: 'binary', results: found ? [found] : [] })
  }

  if (municipality) {
    const q = municipality.toLowerCase()
    const found = linearSearch(db.properties, p => p.municipality.toLowerCase().includes(q))
    return res.json({ type: 'linear', results: found })
  }

  res.status(400).json({ error: 'Informe id ou municipality' })
})

// ── POST /api/analysis ─────────────────────────────────────────────────────
// Body: { property_id: "PR-0042" }
app.post('/api/analysis', (req, res) => {
  const { property_id } = req.body
  if (!property_id) return res.status(400).json({ error: 'property_id obrigatório' })

  const prop = binarySearch(db.sortedById, property_id.toUpperCase(), p => p.property_id)
  if (!prop) return res.status(404).json({ error: 'Propriedade não encontrada' })

  const result = calculateRisk(prop, db.climate)
  res.json(result)
})

// ── POST /api/analysis/batch ───────────────────────────────────────────────
// Body: { ids: ["PR-0001", "PR-0002", ...] }
app.post('/api/analysis/batch', (req, res) => {
  const { ids } = req.body
  if (!Array.isArray(ids) || !ids.length) return res.status(400).json({ error: 'ids[] obrigatório' })

  const results = [], errors = []
  for (const id of ids) {
    const prop = binarySearch(db.sortedById, id.toUpperCase(), p => p.property_id)
    if (!prop) { errors.push({ id, error: 'não encontrado' }); continue }
    results.push(calculateRisk(prop, db.climate))
  }

  res.json({ processed: results.length, errors: errors.length, results, errors })
})

// ── GET /api/stats ─────────────────────────────────────────────────────────
app.get('/api/stats', (req, res) => {
  const props = db.properties
  const allNdvi = props.flatMap(p => p.observations.map(o => o.ndvi_mean))
  const avgNdvi = allNdvi.length
    ? +(allNdvi.reduce((a, b) => a + b, 0) / allNdvi.length).toFixed(3)
    : 0

  // Risco rápido de todos
  const risks = props.map(p => calculateRisk(p, db.climate).risk_class)
  const high  = risks.filter(r => r === 'ALTO').length
  const mid   = risks.filter(r => r === 'MÉDIO').length
  const low   = risks.filter(r => r === 'BAIXO').length

  res.json({ total: props.length, avg_ndvi: avgNdvi, risk_alto: high, risk_medio: mid, risk_baixo: low })
})

const PORT = process.env.PORT || 3001
app.listen(PORT, () => console.log(`[AgroSat] API em http://localhost:${PORT}`))
