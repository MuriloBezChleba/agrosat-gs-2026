# AstroSentinel — Plataforma de Monitoramento Inteligente de Detritos Espaciais

## Visão do Projeto

**AstroSentinel** é uma plataforma AI/ML de monitoramento em tempo real de detritos espaciais e predição de risco de colisão para operadores de satélites. Usa dados reais de TLE (Two-Line Elements) da CelesTrak/NASA para treinar modelos preditivos que alertam operadores sobre conjunções perigosas antes que ocorram.

**Problema**: Existem >27.000 detritos rastreáveis em órbita. Colisões destroem satélites ativos (economia espacial estimada em USD 469 bi até 2030). Ferramentas atuais são reativas; AstroSentinel é preditivo.

**Diferencial**: Combinação de LSTM (trajetória) + Autoencoder (anomalia orbital) + Random Forest (risco) + dashboard em tempo real — tudo open-source e baseado em dados públicos da NASA.

---

## Tema Global Solution 2026 — Space Economy

AstroSentinel cobre todos os entregáveis da GS deste semestre:

| Disciplina | Entregável | Como se aplica |
|---|---|---|
| Data Science | Notebook Google Colab | Análise estatística descritiva de dados orbitais (NASA/Celestrak) |
| Agile Methodology | Documento + Pitch | Product Backlog, personas, requisitos da plataforma |
| Database Design | Modelo relacional Oracle Data Modeler | DB de objetos orbitais, observações, alertas |
| AR/VR | Objetos 3D Blender | Satélite, detritos, painel solar, anel orbital |
| Network Architect | Infraestrutura | Pipeline de ingestão de dados de estações terrestres |

---

## Stack Técnica

- **Linguagem**: Python 3.11+
- **ML/DL**: scikit-learn, TensorFlow/Keras, XGBoost
- **Dados**: NASA Open Data, CelesTrak TLE, Space-Track.org
- **Análise**: pandas, numpy, matplotlib, seaborn, plotly
- **Orbital**: skyfield, sgp4
- **DB**: Oracle (GS) / SQLite (dev)
- **3D**: Blender 4.x (AR/VR deliverable)

---

## Modelos AI/ML

### 1. Predição de Trajetória (LSTM)
- Input: histórico TLE de 30 dias (posição, velocidade, parâmetros orbitais)
- Output: posição prevista em t+1h, t+6h, t+24h
- Referência: [Space-Debris LSTM](https://github.com/KVB02/Space-Debris-Detection-Tracking-and-Impact-Analysis)

### 2. Detecção de Anomalia Orbital (Autoencoder)
- Input: série temporal de parâmetros keplerianos
- Output: score de anomalia (decay anômalo, manobra não declarada)
- Referência: [Satellite Telemetry Anomaly Detection](https://github.com/sapols/Satellite-Telemetry-Anomaly-Detection)

### 3. Classificação de Risco de Colisão (Random Forest)
- Input: distância mínima de aproximação (Miss Distance), velocidade relativa, incerteza orbital
- Output: classe de risco (VERDE/AMARELO/VERMELHO) + probabilidade
- Referência: [SpaceTrash ML](https://github.com/Apliz/SpaceTrash)

### 4. Análise de Cluster de Detritos (DBSCAN/K-Means)
- Input: coordenadas orbitais (altitude × inclinação × RAAN)
- Output: clusters de regiões de maior densidade de detritos
- Usado na análise descritiva (Data Science deliverable)

---

## Datasets

| Dataset | Fonte | Uso |
|---|---|---|
| TLE Historical Data | CelesTrak | Treino LSTM, análise orbital |
| Space Debris Statistics | ESA DISCOS | Estatística descritiva |
| Conjunction Data Messages | Space-Track.org | Treino classificador de risco |
| NEO Close Approaches | NASA CNEOS | Análise de objetos próximos |
| SATCAT (Satellite Catalog) | CelesTrak | Base de dados de objetos rastreados |

---

## Estrutura do Repositório

```
astrosentinel/
├── data/                    # datasets brutos e processados
│   ├── raw/
│   └── processed/
├── notebooks/               # Google Colab notebooks (Data Science)
│   ├── 01_eda_estatistica_descritiva.ipynb
│   ├── 02_preparacao_dados.ipynb
│   └── 03_modelos_ml.ipynb
├── src/
│   ├── ingestion/           # coleta TLE e dados NASA
│   ├── models/              # LSTM, Autoencoder, RF
│   ├── api/                 # endpoints REST (futuro)
│   └── utils/
├── database/                # scripts SQL Oracle (Database Design)
│   ├── ddl/
│   └── dml/
├── docs/                    # documentação Agile, requisitos
│   ├── product_backlog.md
│   ├── personas.md
│   └── requisitos.md
└── blender/                 # arquivos .blend (AR/VR)
```

---

## Personas

### 1. Engenheira de Operações de Satélite
**Nome**: Dra. Ana Ferreira | **Idade**: 34 | **Organização**: Operadora privada de constelação LEO
**Dor**: Recebe alertas de conjunção genéricos com 24h de antecedência; janela de manobra insuficiente
**Ganho com AstroSentinel**: Alertas com 72h de antecedência + probabilidade de colisão + janela de manobra sugerida

### 2. Analista de Política Espacial
**Nome**: Carlos Mendez | **Idade**: 45 | **Organização**: Agência espacial governamental
**Dor**: Sem visibilidade sobre densidade de detritos por região orbital; difícil justificar regulação
**Ganho com AstroSentinel**: Relatórios estatísticos regionais + tendências de crescimento de detritos

### 3. Pesquisador de Sustentabilidade Orbital
**Nome**: Prof. Li Wei | **Idade**: 52 | **Organização**: Universidade
**Dor**: Dados de TLE fragmentados em fontes diferentes; análise manual demorada
**Ganho com AstroSentinel**: API unificada + notebooks prontos + datasets limpos

---

## Banco de Dados — Entidades Principais

```
ORBITAL_OBJECT (id, norad_id, name, type, launch_date, status, country_code)
OBSERVATION    (id, object_id, epoch, tle_line1, tle_line2, altitude_km, inclination_deg)
CONJUNCTION    (id, primary_id, secondary_id, tca_time, miss_distance_km, collision_prob)
RISK_ALERT     (id, conjunction_id, severity, generated_at, acknowledged, operator_notified)
SATELLITE_OP   (id, name, country, contact_email, satellites_count)
DECAY_FORECAST (id, object_id, predicted_reentry, confidence_pct, model_version)
```

---

## Referências GitHub

- [awesome-space](https://github.com/orbitalindex/awesome-space) — curadoria de recursos espaciais
- [SpaceTrash](https://github.com/Apliz/SpaceTrash) — ML para detritos LEO
- [AstroCleanAI](https://github.com/Izzah-Khursheed/AstroCleanAI) — YOLOv5 + XGBoost para detritos
- [Satellite Telemetry Anomaly Detection](https://github.com/sapols/Satellite-Telemetry-Anomaly-Detection) — autoencoders para telemetria
- [NASA GIBS ML](https://github.com/nasa-gibs/gibs-ml) — ML para imagens satelitais NASA
- [Space-Debris LSTM](https://github.com/KVB02/Space-Debris-Detection-Tracking-and-Impact-Analysis) — LSTM + GBDT para trajetória

---

## Regras de Desenvolvimento

- Todo código Python deve ser executável no Google Colab (sem dependências locais pesadas)
- Notebooks devem ter células Markdown explicativas entre cada seção (requisito Data Science)
- SQL deve ser compatível com Oracle 19c (requisito Database Design)
- Commits em inglês, código comentado em português (equipe PT-BR)
- Usar dados públicos reais — sem dados sintéticos puros (mínimo: dataset real + enriquecimento)

---

## Entrega e Prazos

- **Data limite**: 09/06/2026
- **Data Science**: Google Colab, link público com execução disponível
- **Agile**: PDF com documento completo + link YouTube do pitch (máx 5 min)
- **Database**: PDF com DDL + modelos Oracle Data Modeler (conceitual + lógico)
- **AR/VR**: PDF com 13+ prints Blender, cada um com legenda
- **Network**: (aguardando briefing completo)

---

## Critérios de Avaliação Consolidados

### Data Science (10 pts)
Contextualização • Preparação dados • Tendência central • Dispersão • Posicionais/outliers • Distribuição • Visualizações • Perguntas negócio • Organização

### Agile (100 pts)
Apresentação projeto • Público-alvo com dados mercado • Personas • Requisitos (min 7 cada categoria) • Product Backlog (min 12 US) • Pitch 5min

### Database (10 pts)
Apresentação • Tabelas (min 5) • Colunas com tipos/constraints • Modelo conceitual • Modelo lógico-relacional

### AR/VR (100 pts)
Qualidade modelagem • Organização/boas práticas • Aplicação do tema
