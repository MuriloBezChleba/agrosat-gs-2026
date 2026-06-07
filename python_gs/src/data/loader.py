"""
Carrega CSVs de NDVI e clima, constrói lista de Property com
DoublyLinkedList de observações ordenadas por data via merge_sort.
"""

import csv
from datetime import date
from pathlib import Path
from typing import Optional

from src.models.property import Observation, Property
from src.structures.linked_list import DoublyLinkedList
from src.algorithms.sort import merge_sort
from src.utils.logger import get_logger

logger = get_logger()

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_properties(ndvi_path: Optional[Path] = None) -> list[Property]:
    """
    Lê ndvi_series.csv e monta lista de Property.
    Cada Property.observations é DoublyLinkedList de Observation ordenada por data.
    """
    path = ndvi_path or DATA_DIR / "ndvi_series.csv"

    try:
        raw = _read_csv(path)
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {path}")
        raise

    # Agrupa linhas por property_id
    groups: dict[str, dict] = {}
    for row in raw:
        pid = row["property_id"]
        if pid not in groups:
            groups[pid] = {
                "property_id": pid,
                "municipality": row["municipality"],
                "state": row["state"],
                "culture": row["culture"],
                "area_ha": float(row["area_ha"]),
                "obs_rows": [],
            }
        groups[pid]["obs_rows"].append(row)

    properties = []
    for g in groups.values():
        obs_list = [_parse_observation(r) for r in g["obs_rows"]]
        # Ordena observações por data com merge_sort
        obs_list = merge_sort(obs_list, key=lambda o: o.obs_date)

        linked = DoublyLinkedList()
        for obs in obs_list:
            linked.append(obs)

        prop = Property(
            property_id=g["property_id"],
            municipality=g["municipality"],
            state=g["state"],
            culture=g["culture"],
            area_ha=g["area_ha"],
        )
        prop.observations = linked
        properties.append(prop)

    logger.info(f"Carregadas {len(properties)} propriedades de {path.name}")
    return properties


def load_climate(climate_path: Optional[Path] = None) -> dict[tuple, dict]:
    """
    Lê climate_data.csv e retorna dict keyed por (municipality, obs_date).
    """
    path = climate_path or DATA_DIR / "climate_data.csv"

    try:
        raw = _read_csv(path)
    except FileNotFoundError:
        logger.warning(f"Dados climáticos não encontrados: {path}")
        return {}

    climate = {}
    for row in raw:
        key = (row["municipality"], row["obs_date"])
        climate[key] = {
            "temp_max_c": float(row["temp_max_c"]),
            "temp_min_c": float(row["temp_min_c"]),
            "precipitation_mm": float(row["precipitation_mm"]),
            "humidity_pct": float(row["humidity_pct"]),
        }

    logger.info(f"Carregados {len(climate)} registros climáticos de {path.name}")
    return climate


def _read_csv(path: Path) -> list[dict]:
    try:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            raise ValueError(f"CSV vazio: {path}")
        return rows
    except csv.Error as e:
        logger.error(f"Erro ao ler CSV {path}: {e}")
        raise


def _parse_observation(row: dict) -> Observation:
    try:
        return Observation(
            obs_date=date.fromisoformat(row["obs_date"]),
            ndvi_mean=float(row["ndvi_mean"]),
            ndvi_std=float(row["ndvi_std"]),
            evi_mean=float(row["evi_mean"]),
            cloud_cover_pct=float(row["cloud_cover_pct"]),
            satellite=row["satellite"],
        )
    except (KeyError, ValueError) as e:
        logger.error(f"Linha inválida no CSV: {row} — {e}")
        raise
