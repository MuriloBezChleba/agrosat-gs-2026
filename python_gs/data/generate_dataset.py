"""
Gera datasets sintéticos baseados em distribuições reais de NDVI do Sentinel-2
para região agrícola do Paraná. Executa uma vez para criar os CSVs.

Uso: python data/generate_dataset.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).parent

MUNICIPALITIES = [
    ("Cascavel", "PR"), ("Toledo", "PR"), ("Marechal Cândido Rondon", "PR"),
    ("Palotina", "PR"), ("Umuarama", "PR"), ("Campo Mourão", "PR"),
    ("Londrina", "PR"), ("Maringá", "PR"), ("Ponta Grossa", "PR"),
    ("Guarapuava", "PR"),
]

CULTURES = ["soja", "milho", "trigo", "cana-de-açúcar", "algodão"]

# Parâmetros NDVI por cultura (média, desvio) — baseados em literatura Sentinel-2
NDVI_PARAMS = {
    "soja":           (0.72, 0.10),
    "milho":          (0.68, 0.12),
    "trigo":          (0.65, 0.11),
    "cana-de-açúcar": (0.75, 0.09),
    "algodão":        (0.60, 0.13),
}


def _clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, val))


def generate_ndvi_series(n_properties: int = 200, obs_per_property: int = 12) -> None:
    rows = []

    for i in range(1, n_properties + 1):
        prop_id = f"PR-{i:04d}"
        mun, state = random.choice(MUNICIPALITIES)
        culture = random.choice(CULTURES)
        area_ha = round(random.uniform(50, 3000), 1)

        ndvi_base, ndvi_std_base = NDVI_PARAMS[culture]
        # Talhões em estresse têm NDVI sistematicamente mais baixo
        stress_factor = random.choice([0, 0, 0, -0.15, -0.25])
        ndvi_base += stress_factor

        start_date = date(2023, 1, 1)

        for j in range(obs_per_property):
            obs_date = start_date + timedelta(days=30 * j)
            # Variação sazonal: NDVI cai no inverno (meses 5-8)
            season_adj = -0.08 if obs_date.month in (5, 6, 7, 8) else 0.0
            ndvi_mean = _clamp(
                random.gauss(ndvi_base + season_adj, ndvi_std_base), 0.05, 0.95
            )
            ndvi_std = round(_clamp(random.gauss(0.06, 0.02), 0.01, 0.20), 3)
            evi_mean = round(_clamp(ndvi_mean * 0.87 + random.gauss(0, 0.02), 0.02, 0.85), 3)
            cloud_cover = round(_clamp(random.expovariate(1 / 8), 0, 60), 1)

            rows.append({
                "property_id": prop_id,
                "municipality": mun,
                "state": state,
                "culture": culture,
                "area_ha": area_ha,
                "obs_date": obs_date.isoformat(),
                "ndvi_mean": round(ndvi_mean, 3),
                "ndvi_std": ndvi_std,
                "evi_mean": evi_mean,
                "cloud_cover_pct": cloud_cover,
                "satellite": "Sentinel-2",
            })

    out = DATA_DIR / "ndvi_series.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Gerado: {out} ({len(rows)} registros)")


def generate_climate_data() -> None:
    rows = []
    start_date = date(2023, 1, 1)

    for mun, state in MUNICIPALITIES:
        for month in range(12):
            obs_date = start_date + timedelta(days=30 * month)
            # Parâmetros climáticos do Paraná
            temp_max = round(random.gauss(28 if obs_date.month in (12, 1, 2) else 22, 3), 1)
            temp_min = round(temp_max - random.uniform(8, 14), 1)
            precipitation = round(_clamp(random.gauss(140, 50), 0, 400), 1)
            humidity = round(_clamp(random.gauss(72, 10), 30, 98), 1)

            rows.append({
                "municipality": mun,
                "state": state,
                "obs_date": obs_date.isoformat(),
                "temp_max_c": temp_max,
                "temp_min_c": temp_min,
                "precipitation_mm": precipitation,
                "humidity_pct": humidity,
            })

    out = DATA_DIR / "climate_data.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Gerado: {out} ({len(rows)} registros)")


if __name__ == "__main__":
    generate_ndvi_series()
    generate_climate_data()
    print("Datasets prontos.")
