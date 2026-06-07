from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Observation:
    obs_date: date
    ndvi_mean: float
    ndvi_std: float
    evi_mean: float
    cloud_cover_pct: float
    satellite: str

    def __repr__(self) -> str:
        return f"Observation({self.obs_date}, NDVI={self.ndvi_mean:.3f})"


@dataclass
class Property:
    property_id: str
    municipality: str
    state: str
    culture: str
    area_ha: float

    def __repr__(self) -> str:
        return f"Property({self.property_id}, {self.municipality}/{self.state}, {self.culture})"


@dataclass
class AnalysisResult:
    property_id: str
    municipality: str
    analysis_date: datetime
    risk_score: float
    risk_class: str
    ndvi_mean: float
    ndvi_trend: str
    recommendation: str

    def __repr__(self) -> str:
        return f"AnalysisResult({self.property_id}, {self.risk_class}, score={self.risk_score:.1f})"
