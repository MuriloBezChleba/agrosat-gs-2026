const BASE = '/api'

async function get(path) {
  const res = await fetch(BASE + path)
  if (!res.ok) throw new Error((await res.json()).error ?? res.statusText)
  return res.json()
}

async function post(path, body) {
  const res = await fetch(BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error((await res.json()).error ?? res.statusText)
  return res.json()
}

export const api = {
  stats: () => get('/stats'),
  properties: (sort = 'id', order = 'asc') =>
    get(`/properties?sort=${sort}&order=${order}`),
  property: (id) => get(`/properties/${id}`),
  searchById: (id) => get(`/search?id=${encodeURIComponent(id)}`),
  searchByMunicipality: (q) => get(`/search?municipality=${encodeURIComponent(q)}`),
  analyze: (property_id) => post('/analysis', { property_id }),
  analyzeBatch: (ids) => post('/analysis/batch', { ids }),
}
