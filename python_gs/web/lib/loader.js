import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { parse } from 'csv-parse/sync'
import { mergeSort } from './algorithms.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const DATA_DIR = path.resolve(__dirname, '../../data')

let _properties = null
let _climate = null
let _sortedById = null

export function loadAll() {
  if (_properties) return { properties: _properties, climate: _climate, sortedById: _sortedById }

  const ndviRaw = parse(fs.readFileSync(path.join(DATA_DIR, 'ndvi_series.csv'), 'utf8'), {
    columns: true, skip_empty_lines: true,
  })

  const climateRaw = parse(fs.readFileSync(path.join(DATA_DIR, 'climate_data.csv'), 'utf8'), {
    columns: true, skip_empty_lines: true,
  })

  // Monta mapa de clima por (municipality, obs_date)
  _climate = {}
  for (const row of climateRaw) {
    _climate[`${row.municipality}||${row.obs_date}`] = {
      temp_max_c: parseFloat(row.temp_max_c),
      temp_min_c: parseFloat(row.temp_min_c),
      precipitation_mm: parseFloat(row.precipitation_mm),
      humidity_pct: parseFloat(row.humidity_pct),
    }
  }

  // Agrupa observações por property_id
  const groups = {}
  for (const row of ndviRaw) {
    const pid = row.property_id
    if (!groups[pid]) {
      groups[pid] = {
        property_id: pid,
        municipality: row.municipality,
        state: row.state,
        culture: row.culture,
        area_ha: parseFloat(row.area_ha),
        observations: [],
      }
    }
    groups[pid].observations.push({
      obs_date: row.obs_date,
      ndvi_mean: parseFloat(row.ndvi_mean),
      ndvi_std: parseFloat(row.ndvi_std),
      evi_mean: parseFloat(row.evi_mean),
      cloud_cover_pct: parseFloat(row.cloud_cover_pct),
      satellite: row.satellite,
    })
  }

  // Ordena observações por data com mergeSort
  _properties = Object.values(groups).map(p => ({
    ...p,
    observations: mergeSort(p.observations, o => o.obs_date),
  }))

  // Índice ordenado por ID para binarySearch
  _sortedById = [..._properties].sort((a, b) => a.property_id.localeCompare(b.property_id))

  return { properties: _properties, climate: _climate, sortedById: _sortedById }
}
