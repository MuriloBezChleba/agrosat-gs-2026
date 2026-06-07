const NDVI_REFERENCE = {
  soja: 0.72, milho: 0.68, trigo: 0.65,
  'cana-de-açúcar': 0.75, algodão: 0.60,
}
const DEFAULT_REF = 0.65

const W_NDVI = 0.40, W_TREND = 0.25, W_PRECIP = 0.20, W_CLOUD = 0.15

export function calculateRisk(property, climate) {
  const obs = property.observations
  if (!obs.length) return _make(property, 0, 'ALTO', 'sem dados', 0)

  const recent = obs.slice(-3)
  const values = recent.map(o => o.ndvi_mean)
  const ndviMean = values.reduce((a, b) => a + b, 0) / values.length
  const ref = NDVI_REFERENCE[property.culture] ?? DEFAULT_REF
  const ndviScore = Math.min(100, (ndviMean / ref) * 100)

  let trend, trendScore
  if (values.length >= 2) {
    const delta = values.at(-1) - values[0]
    if (delta > 0.05)       { trend = 'CRESCENTE';   trendScore = 80 }
    else if (delta < -0.05) { trend = 'DECLINANTE';  trendScore = 20 }
    else                    { trend = 'ESTÁVEL';      trendScore = 55 }
  } else {
    trend = 'INSUFICIENTE'; trendScore = 50
  }

  const lastObs = recent.at(-1)
  let precipScore = 50
  const climKey = `${property.municipality}||${lastObs.obs_date}`
  const clim = climate[climKey]
  if (clim) {
    const p = clim.precipitation_mm
    precipScore = p >= 80 ? Math.min(100, (p / 140) * 80) : (p / 80) * 40
  }

  const cloudScore = Math.max(0, 100 - lastObs.cloud_cover_pct * 1.5)

  const score = +(
    ndviScore  * W_NDVI +
    trendScore * W_TREND +
    precipScore * W_PRECIP +
    cloudScore * W_CLOUD
  ).toFixed(1)

  const riskClass = score >= 67 ? 'BAIXO' : score >= 34 ? 'MÉDIO' : 'ALTO'
  return _make(property, score, riskClass, trend, ndviMean)
}

function _make(property, score, riskClass, trend, ndviMean) {
  const recs = {
    BAIXO: 'Lavoura saudável. Manter monitoramento mensal.',
    MÉDIO: 'Atenção: monitorar precipitação e NDVI semanalmente.',
    ALTO:  'Risco elevado: considerar vistoria técnica urgente.',
  }
  return {
    property_id: property.property_id,
    municipality: property.municipality,
    culture: property.culture,
    area_ha: property.area_ha,
    analysis_date: new Date().toISOString(),
    risk_score: score,
    risk_class: riskClass,
    ndvi_mean: +ndviMean.toFixed(3),
    ndvi_trend: trend,
    recommendation: recs[riskClass] ?? recs.ALTO,
  }
}
