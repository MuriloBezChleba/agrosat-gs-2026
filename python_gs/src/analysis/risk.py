"""
Cálculo de score de risco agrícola baseado em NDVI (Sentinel-2) e dados climáticos.

Score 0–100:
  67–100 → BAIXO risco  (verde)
  34–66  → MÉDIO risco  (amarelo)
  0–33   → ALTO risco   (vermelho)
"""

from datetime import datetime
from typing import Optional

from src.models.property import AnalysisResult, Property
from src.utils.logger import get_logger

logger = get_logger()

# Pesos do score de risco
_W_NDVI_MEAN  = 0.40
_W_NDVI_TREND = 0.25
_W_PRECIP     = 0.20
_W_CLOUD      = 0.15

# NDVI de referência por cultura (saudável)
_NDVI_REFERENCE = {
    "soja":           0.72,
    "milho":          0.68,
    "trigo":          0.65,
    "cana-de-açúcar": 0.75,
    "algodão":        0.60,
}
_NDVI_DEFAULT_REF = 0.65


def calculate_risk(
    prop: Property,
    climate: Optional[dict] = None,
) -> AnalysisResult:
    """
    Calcula score de risco para uma propriedade.
    Usa últimas 3 observações da DoublyLinkedList.
    """
    obs_list = prop.observations.to_list()

    if not obs_list:
        logger.warning(f"{prop.property_id}: sem observações — risco máximo assumido")
        return _make_result(prop, 0.0, "sem dados", 0.0)

    # Últimas 3 obs (mais recentes)
    recent = obs_list[-3:]
    ndvi_values = [o.ndvi_mean for o in recent]
    last_obs = recent[-1]

    ndvi_mean = sum(ndvi_values) / len(ndvi_values)
    ndvi_ref = _NDVI_REFERENCE.get(prop.culture, _NDVI_DEFAULT_REF)

    # Componente 1: NDVI relativo à referência da cultura (0–100)
    ndvi_score = min(100.0, (ndvi_mean / ndvi_ref) * 100)

    # Componente 2: tendência NDVI (crescente = bom, declinante = ruim)
    if len(ndvi_values) >= 2:
        delta = ndvi_values[-1] - ndvi_values[0]
        if delta > 0.05:
            trend = "CRESCENTE"
            trend_score = 80.0
        elif delta < -0.05:
            trend = "DECLINANTE"
            trend_score = 20.0
        else:
            trend = "ESTÁVEL"
            trend_score = 55.0
    else:
        trend = "INSUFICIENTE"
        trend_score = 50.0

    # Componente 3: precipitação (referência Paraná: 140 mm/mês)
    precip_score = 50.0
    if climate:
        key = (prop.municipality, last_obs.obs_date.isoformat())
        c = climate.get(key)
        if c:
            precip = c["precipitation_mm"]
            if precip >= 80:
                precip_score = min(100.0, (precip / 140) * 80)
            else:
                precip_score = (precip / 80) * 40

    # Componente 4: cobertura de nuvens (alta cobertura = dado menos confiável)
    cloud_score = max(0.0, 100 - last_obs.cloud_cover_pct * 1.5)

    # Score final ponderado
    score = (
        ndvi_score  * _W_NDVI_MEAN
        + trend_score * _W_NDVI_TREND
        + precip_score * _W_PRECIP
        + cloud_score * _W_CLOUD
    )
    score = round(min(100.0, max(0.0, score)), 1)

    logger.info(
        f"{prop.property_id} | score={score} | ndvi={ndvi_mean:.3f} | trend={trend}"
    )
    return _make_result(prop, score, trend, ndvi_mean)


def _make_result(
    prop: Property, score: float, trend: str, ndvi_mean: float
) -> AnalysisResult:
    if score >= 67:
        risk_class = "BAIXO"
        recommendation = "Lavoura saudável. Manter monitoramento mensal."
    elif score >= 34:
        risk_class = "MÉDIO"
        recommendation = "Atenção: monitorar precipitação e NDVI semanalmente."
    else:
        risk_class = "ALTO"
        recommendation = "Risco elevado: considerar vistoria técnica urgente."

    return AnalysisResult(
        property_id=prop.property_id,
        municipality=prop.municipality,
        analysis_date=datetime.now(),
        risk_score=score,
        risk_class=risk_class,
        ndvi_mean=ndvi_mean,
        ndvi_trend=trend,
        recommendation=recommendation,
    )
