# AstroSentinel

## What This Is

AstroSentinel é uma plataforma AI/ML de monitoramento em tempo real de detritos espaciais e predição de risco de colisão para operadores de satélites. Usa dados reais de TLE (Two-Line Elements) da CelesTrak/NASA para treinar modelos LSTM, Autoencoder e Random Forest que alertam operadores sobre conjunções perigosas com 72h de antecedência. Entregável da Global Solution 2026 da FIAP — tema Space Economy.

## Core Value

Operadores de satélites recebem alertas preditivos de colisão com detritos espaciais com antecedência suficiente para manobra — transformando reação em prevenção.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Sistema carrega e processa dados TLE reais da CelesTrak/NASA
- [ ] Pipeline de estatística descritiva completa (tendência central, dispersão, outliers, distribuição)
- [ ] Modelo LSTM prediz trajetória orbital (t+1h, t+6h, t+24h)
- [ ] Autoencoder detecta anomalias orbitais (decay anômalo, manobras não declaradas)
- [ ] Random Forest classifica risco de colisão (VERDE/AMARELO/VERMELHO + probabilidade)
- [ ] Clustering DBSCAN identifica regiões de maior densidade de detritos
- [ ] Notebook Google Colab completo e executável com análise descritiva
- [ ] Modelo relacional Oracle com mínimo 6 tabelas (ORBITAL_OBJECT, OBSERVATION, CONJUNCTION, RISK_ALERT, SATELLITE_OP, DECAY_FORECAST)
- [ ] Documento de requisitos Agile: funcionais, não-funcionais, técnicos, regras de negócio (mín. 7 cada)
- [ ] Product Backlog com mínimo 12 Histórias de Usuário e critérios de aceite
- [ ] 3 personas documentadas (engenheira operações, analista política, pesquisador)
- [ ] Pitch em vídeo de até 5 minutos no YouTube
- [ ] 5 perguntas de negócio respondidas com evidências estatísticas
- [ ] Visualizações obrigatórias: histograma, boxplot, barras, scatterplot, heatmap de correlação

### Out of Scope

- Interface web em tempo real — prazo da GS não permite frontend completo
- Integração com Space-Track.org API autenticada — usar datasets públicos CelesTrak
- Sistema de manobra autônoma — fora do escopo acadêmico
- Deploy em produção / cloud — entrega local/Colab

## Context

**Contexto acadêmico:** Global Solution 2026, FIAP, 2º ano Engenharia de Software. Prazo: 09/06/2026. Grupo de até 5 pessoas. Entrega em PDF + links.

**Disciplinas e entregáveis:**
- Data Science: Notebook Google Colab (estatística descritiva, Python, visualizações, 5+ perguntas negócio)
- Agile Methodology: PDF (requisitos, personas, backlog 12+ US, pitch vídeo 5min YouTube)
- Database Design: PDF (DDL Oracle, modelos conceitual+lógico Oracle Data Modeler, mín. 5 tabelas)
- AR/VR: PDF (13+ prints Blender, objetos 3D tema viagens espaciais)

**Datasets disponíveis:**
- CelesTrak TLE data (público, sem autenticação)
- ESA DISCOS Space Debris Statistics
- NASA CNEOS NEO Close Approaches
- NASA Open Data Portal

**Referências GitHub:**
- SpaceTrash (ML para LEO debris)
- AstroCleanAI (YOLOv5 + XGBoost)
- Satellite Telemetry Anomaly Detection (autoencoders)
- NASA GIBS ML (imagens satelitais)

## Constraints

- **Timeline**: Entrega 09/06/2026 — ~14 dias
- **Plataforma Data Science**: Google Colab (sem dependências locais pesadas)
- **Banco de Dados**: Oracle 19c (requisito Database Design FIAP)
- **3D**: Blender 4.x (requisito AR/VR FIAP)
- **Dados**: Apenas datasets públicos (sem API keys pagas)
- **Linguagem código**: Python 3.11+
- **Formato entrega**: PDF para disciplinas + link Colab + link YouTube

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Tema: detritos espaciais | Conecta todos os entregáveis, dados NASA públicos disponíveis, ML aplicável | — Pending |
| Stack ML: sklearn + TensorFlow/Keras | Roda no Colab sem configuração, bem documentado, equipe familiarizada | — Pending |
| DB: Oracle 19c | Requisito obrigatório da disciplina Database Design | — Pending |
| 3D: Blender | Requisito obrigatório da disciplina AR/VR | — Pending |
| Dados: CelesTrak TLE público | Sem autenticação, atualizado diariamente, formato padrão da indústria | — Pending |

## Evolution

Este documento evolui a cada transição de fase e marco de milestone.

**Após cada transição de fase** (via `/gsd-transition`):
1. Requisitos invalidados? → Mover para Out of Scope com motivo
2. Requisitos validados? → Mover para Validated com referência da fase
3. Novos requisitos emergiram? → Adicionar em Active
4. Decisões para registrar? → Adicionar em Key Decisions
5. "What This Is" ainda preciso? → Atualizar se derivou

**Após cada milestone** (via `/gsd-complete-milestone`):
1. Revisão completa de todas as seções
2. Core Value check — ainda é a prioridade certa?
3. Auditoria de Out of Scope — motivos ainda válidos?
4. Atualizar Context com estado atual

---
*Last updated: 2026-05-26 after initialization*
