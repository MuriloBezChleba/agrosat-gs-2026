# AgroSat — Project State

**Project:** AgroSat — Plataforma de Inteligência Agrícola por Satélite
**Milestone:** Global Solution 2026
**Last Updated:** 2026-05-26

---

## Project Reference

**Core Value:** Fintechs, cooperativas e seguradoras tomam decisões de crédito e seguro rural com visibilidade real da saúde de cada talhão via satélite — substituindo visita técnica cara por dado objetivo.

**Deadline:** 09/06/2026 (~14 dias a partir de 2026-05-26)

**Clientes pagantes:** Fintechs crédito rural (Agrolend, Traive) | Cooperativas (Coamo, C.Vale) | Seguradoras rurais

---

## Current Position

**Current Phase:** Phase 1 — Data Foundation
**Status:** Not started — ready to plan

**Progress:**
```
Phase 1 [          ] 0%   Data Foundation
Phase 2 [          ] 0%   Statistical Analysis & Visualizations
Phase 3 [          ] 0%   ML/DL Models
Phase 4 [          ] 0%   Database Design
Phase 5 [          ] 0%   Agile Documentation
Phase 6 [          ] 0%   3D Modeling & Final Delivery
```

**Overall:** 0/6 phases complete

---

## Phase Summary

| Phase | Name | Requirements | Dependency | Status |
|-------|------|--------------|------------|--------|
| 1 | Data Foundation | DATA-01..06 (6) | None | Not started |
| 2 | Statistical Analysis & Viz | STATS-01..07, VIZ-01..06 (13) | Phase 1 | Not started |
| 3 | ML/DL Models | ML-01..05 (5) | Phase 1 | Not started |
| 4 | Database Design | DB-01..07 (7) | Phase 1 | Not started |
| 5 | Agile Documentation | AGILE-01..09 (9) | **None** ← paralelo | Not started |
| 6 | 3D & Final Delivery | ARVR-01..05, DOCS-01..04 (9) | All | Not started |

---

## Key Decisions

| Decision | Rationale | Phase |
|----------|-----------|-------|
| Pivot: AstroSentinel → AgroSat | Crédito rural B2B tem mercado real (R$300B+), dados gratuitos, dor clara | Init |
| Phase 5 (Agile) independente | Documentação Agile não depende de código — pode rodar em paralelo | All |
| Dataset: NDVI Sentinel-2 pré-calculado | Evita processamento raw .tif (lento no Colab), mantém dados reais | Phase 1 |
| Clientes primários: fintechs | BACEN 4.945/2021 obriga avaliação risco climático em crédito rural | All |

## Active Todos

- [ ] Iniciar Phase 1: encontrar dataset NDVI no Kaggle ou Google Earth Engine e abrir Colab
- [ ] Phase 5 pode começar AGORA em paralelo (sem dependência técnica)
- [ ] Definir composição da equipe e atribuir fases por membro

## Open Questions

- Dataset NDVI: usar Kaggle ("Brazil Agriculture") ou Google Earth Engine?
- Região foco: Paraná (soja/milho) ou Mato Grosso? → Mato Grosso tem mais volume de dados
- Quantos membros na equipe e quem faz qual fase?

---

## Session Continuity

**Last session:** Projeto inicializado 2026-05-26. Pivotado de AstroSentinel (detritos espaciais) para AgroSat (inteligência agrícola) após feedback de valor de negócio. CLAUDE.md, PROJECT.md, REQUIREMENTS.md, ROADMAP.md todos atualizados.

**Next action:** `/gsd-plan-phase 1` para planejar Data Foundation OU `/gsd-plan-phase 5` para Agile docs (pode começar imediatamente em paralelo).

---

*Atualizado a cada transição de fase. Não editar manualmente exceto Key Decisions e Active Todos.*
