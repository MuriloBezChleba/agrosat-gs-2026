# AgroSat

## What This Is

AgroSat é uma plataforma SaaS de inteligência agrícola que usa imagens de satélite gratuitas (Sentinel-2/Landsat) e modelos ML/DL para monitorar saúde de lavouras por NDVI, prever produtividade de safras e calcular risco de seca/inundação por propriedade rural. Clientes pagantes: fintechs de crédito rural, cooperativas agrícolas e seguradoras rurais. Entregável da Global Solution 2026 da FIAP — tema Space Economy.

## Core Value

Fintechs, cooperativas e seguradoras tomam decisões de crédito e seguro rural com visibilidade real da saúde de cada talhão via satélite — substituindo visita técnica cara por dado objetivo e automatizado.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Pipeline importa série temporal de NDVI calculada de imagens Sentinel-2 reais via Python
- [ ] Análise estatística descritiva completa (tendência central, dispersão, posicionais, outliers, distribuição)
- [ ] 5 visualizações obrigatórias (histograma, boxplot, barras, scatterplot, heatmap correlação)
- [ ] 5 perguntas de negócio respondidas com evidências estatísticas
- [ ] LSTM treinado para predição de produtividade de safra (t+30, t+60 dias)
- [ ] Random Forest / XGBoost para scoring de risco por propriedade (BAIXO/MÉDIO/ALTO + score 0–100)
- [ ] K-Means para segmentação de perfis de propriedades
- [ ] Notebook Google Colab completo e executável com documentação Markdown
- [ ] Modelo relacional Oracle com 6 tabelas (PROPERTY, CROP_RECORD, SATELLITE_OBS, CLIMATE_DATA, RISK_ANALYSIS, CREDIT_CONTRACT)
- [ ] DDL SQL Oracle válido para criação das 6 tabelas com constraints PK/FK
- [ ] Diagramas Oracle Data Modeler: conceitual (Logical) e lógico-relacional (Relational)
- [ ] Documento Agile: 3 personas, 7+ requisitos por categoria, 12+ User Stories com DoD
- [ ] Vídeo Pitch YouTube (máx 5 min) mostrando problema, oportunidade de mercado, solução
- [ ] Objeto 3D Blender: satélite Sentinel-2 + talhão agrícola com visualização NDVI, 13+ prints

### Out of Scope

- Interface web em tempo real — prazo de 14 dias inviabiliza frontend completo
- Integração real com API Sentinel Hub paga — usar dados via Google Earth Engine gratuito ou dataset Kaggle
- Sistema de recomendação de insumos (fertilizantes, defensivos) — fora do prazo
- Deploy em produção cloud — entrega em Colab
- Processamento de imagens raw Sentinel-2 (.tif) — usar dataset NDVI pré-calculado para agilizar

## Context

**Contexto acadêmico:** Global Solution 2026, FIAP, 2º ano Engenharia de Software. Prazo: 09/06/2026. Grupo de até 5 pessoas.

**Mercado real:**
- Crédito rural Brasil: R$300B+/ano (Plano Safra 2025/2026)
- BACEN Resolução 4.945/2021: obriga bancos a avaliar risco climático em crédito
- Precisão Agriculture global: USD 14B (2025), CAGR 13%/ano
- Clientes pagantes: Agrolend, Traive, cooperativas (Coamo, C.Vale), seguradoras rurais

**Datasets (gratuitos):**
- Sentinel-2 L2A via Google Earth Engine
- INMET/BDMEP (dados climáticos históricos Brasil)
- MapBiomas Coleção 9 (uso do solo)
- IBGE Censo Agropecuário (produtividade histórica)
- Kaggle: "Brazilian Agriculture" datasets como fallback para Colab

**Disciplinas e entregáveis:**
- Data Science: Notebook Colab (estatística NDVI + clima, visualizações, 5 perguntas negócio)
- Agile: PDF (requisitos, personas crédito/cooperativa/produtor, backlog 12+ US, pitch)
- Database Design: PDF Oracle (6 tabelas, DDL, modelos conceitual+lógico)
- AR/VR: PDF Blender (satélite 3D + talhão, 13+ prints)

## Constraints

- **Timeline**: Entrega 09/06/2026 — 14 dias
- **Plataforma**: Google Colab (sem dependências locais pesadas)
- **Banco de Dados**: Oracle 19c (requisito Database Design FIAP)
- **3D**: Blender 4.x (requisito AR/VR FIAP)
- **Dados**: Apenas gratuitos (Google Earth Engine free tier, INMET aberto, Kaggle)
- **Linguagem**: Python 3.11+
- **Entrega**: PDF por disciplina + link Colab + link YouTube

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Tema: inteligência agrícola via satélite | Mercado B2B real (crédito rural R$300B+), dados gratuitos, ML aplicável, Brasil = líder agro mundial | — Pending |
| Dataset principal: NDVI Sentinel-2 + INMET | Gratuitos, dados reais, volume suficiente (50k+ obs), padrão indústria | — Pending |
| Clientes primários: fintechs crédito rural | BACEN obriga avaliação risco climático, dor real, disposição a pagar clara | — Pending |
| Stack ML: sklearn + TensorFlow/Keras + XGBoost | Roda no Colab, bem documentado, cobre CNN/LSTM/RF/XGBoost | — Pending |
| DB: Oracle 19c | Requisito obrigatório disciplina Database Design | — Pending |
| 3D: Blender | Requisito obrigatório disciplina AR/VR | — Pending |

## Evolution

Este documento evolui a cada transição de fase e marco de milestone.

**Após cada transição de fase** (via `/gsd-transition`):
1. Requisitos invalidados? → Mover para Out of Scope com motivo
2. Requisitos validados? → Mover para Validated com referência da fase
3. Novos requisitos emergiram? → Adicionar em Active
4. Decisões para registrar? → Adicionar em Key Decisions

**Após cada milestone** (via `/gsd-complete-milestone`):
1. Revisão completa de todas as seções
2. Core Value check — ainda é a prioridade certa?
3. Auditoria Out of Scope — motivos ainda válidos?

---
*Last updated: 2026-05-26 after pivot to AgroSat (agricultural intelligence via satellite)*
