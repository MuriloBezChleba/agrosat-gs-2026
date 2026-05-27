# AgroSat — Plataforma de Inteligência Agrícola por Satélite

## Visão do Projeto

**AgroSat** é uma plataforma SaaS de inteligência agrícola que usa imagens de satélite gratuitas (Sentinel-2/Landsat) e modelos de ML/DL para monitorar saúde de lavouras, prever produtividade de safras e calcular risco de seca/inundação por propriedade rural. Entrega valor direto para fintechs de crédito rural, cooperativas agrícolas e seguradoras.

**Problema**: Fintechs de crédito rural emprestam R$300B+/ano sem visibilidade real de risco por talhão. Seguradoras pagam bilhões em sinistros que poderiam ser precificados melhor. Cooperativas não têm forecast de safra antecipado. Dados de satélite que resolvem isso existem e são GRATUITOS — mas ninguém processou para esses clientes.

**Diferencial**: Pipeline completo de NDVI → LSTM → Random Forest rodando em dados reais do Sentinel-2/INMET — open-source, reprodutível no Colab, pronto para integração via API.

---

## Tema Global Solution 2026 — Space Economy

AgroSat usa tecnologia espacial (imagens de satélite) para impacto econômico real no agronegócio brasileiro. Cobre todos os entregáveis da GS:

| Disciplina | Entregável | Como se aplica |
|---|---|---|
| Data Science | Notebook Google Colab | Análise estatística descritiva de dados NDVI (Sentinel-2) + clima (INMET) por região agrícola brasileira |
| Agile Methodology | Documento PDF + Pitch | Product Backlog, personas (produtor rural, analista de crédito, gestor de cooperativa), requisitos da plataforma |
| Database Design | Modelo relacional Oracle | DB de propriedades rurais, observações satelitais, análises de risco, contratos de crédito |
| AR/VR | Objetos 3D Blender | Satélite Sentinel-2, talhão 3D com visualização de NDVI, drone de monitoramento |
| Network Architect | Infraestrutura | Pipeline de ingestão de imagens Sentinel-2 + API de alertas para clientes |

---

## Mercado e Modelo de Negócio

### Mercado Endereçável
- Crédito rural Brasil: **R$300B+/ano** (Plano Safra 2025/2026)
- Prêmios seguros rurais: **R$16B+/ano** (Susep 2024)
- Mercado global precision agriculture: **USD 14B** (2025), crescendo 13%/ano
- Regulação BACEN 4.945/2021: bancos DEVEM avaliar risco climático em crédito

### Clientes (quem paga)
| Segmento | Dor | Disposição a pagar |
|---|---|---|
| Fintechs crédito rural (Agrolend, Traive, CreditAgro) | Risco de inadimplência por sinistro climático sem visibilidade antecipada | API por consulta (R$0,50–R$5 por análise de talhão) |
| Cooperativas agrícolas (Coamo, C.Vale, Cocamar) | Não têm forecast de safra dos cooperados para planejar captação e venda | SaaS (R$2–R$5/ha/safra) |
| Seguradoras rurais (Allianz, Swiss Re, IRB) | Scoring de risco impreciso → sinistros mal precificados | SaaS por portfólio (R$15–R$50k/mês) |
| Tradings (Cargill, Bunge, ADM) | Incerteza de volume de safra para hedge de commodities | Relatório por região (R$5k–R$20k/trimestre) |

---

## Stack Técnica

- **Linguagem**: Python 3.11+
- **Satellite**: sentinelsat, rasterio, earthengine-api (Google Earth Engine)
- **ML/DL**: scikit-learn, TensorFlow/Keras, XGBoost, LightGBM
- **Análise**: pandas, numpy, matplotlib, seaborn, plotly, geopandas
- **Índices vegetação**: NDVI, EVI, SAVI (calculados via bandas Sentinel-2)
- **DB**: Oracle 19c (GS) / SQLite (dev)
- **3D**: Blender 4.x (AR/VR deliverable)
- **Plataforma**: Google Colab (Data Science deliverable)

---

## Modelos AI/ML

### 1. Saúde da Lavoura — NDVI via Sentinel-2 (CV/Índice)
- Input: Bandas B4 (vermelho) e B8 (NIR) do Sentinel-2
- Output: Mapa NDVI por talhão (0 a 1 — quanto maior, mais saudável)
- Análise estatística: distribuição do NDVI por cultura, outliers, tendência temporal

### 2. Predição de Produtividade (LSTM)
- Input: Série temporal de NDVI (30–60 dias) + variáveis climáticas (temperatura, precipitação, umidade)
- Output: Estimativa de produtividade (sacas/ha) para t+30, t+60 dias
- Referência: [wildfire-risk-forecast](https://github.com/Sivarohitk/wildfire-risk-forecast) — mesmo padrão temporal

### 3. Scoring de Risco (Random Forest / XGBoost)
- Input: NDVI médio, desvio padrão, precipitação acumulada, temperatura máxima, histórico de sinistros
- Output: Score de risco 0–100 + classe (BAIXO/MÉDIO/ALTO) por propriedade
- Usado por fintechs e seguradoras no processo de crédito/underwriting

### 4. Segmentação de Perfis (K-Means)
- Input: Variáveis orbitais: NDVI médio da safra, variabilidade, área plantada, altitude, bioma
- Output: Clusters de propriedades similares (4–6 grupos) para personalização de produtos

---

## Datasets (todos gratuitos)

| Dataset | Fonte | Uso |
|---|---|---|
| Imagens Sentinel-2 L2A | ESA Copernicus (via Google Earth Engine) | Cálculo NDVI, classificação de cultura |
| Landsat 8/9 OLI | NASA EarthData | NDVI histórico, séries longas |
| BDMEP/INMET | INMET Brasil | Temperatura, precipitação, umidade relativa |
| MapBiomas Coleção 9 | MapBiomas (ESALQ/INPE) | Classificação uso do solo, identificação de cultura |
| IBGE Censo Agropecuário | IBGE | Área plantada, produtividade histórica por município |
| PRODES/DETER | INPE | Desmatamento (risco regulatório) |

**Dataset principal para o notebook**: Índices NDVI calculados de imagens Sentinel-2 para região agrícola do Paraná/Mato Grosso + dados INMET de 3–5 anos = 50.000+ registros de observações por talhão.

---

## Estrutura do Repositório

```
agrosat/
├── data/                          # datasets brutos e processados
│   ├── raw/
│   │   ├── sentinel2/             # imagens .tif por tile
│   │   ├── inmet/                 # série histórica de clima
│   │   └── mapbiomas/             # shapefile de uso do solo
│   └── processed/
│       ├── ndvi_series.csv        # série temporal NDVI por talhão
│       └── risk_dataset.csv       # dataset para modelos ML
├── notebooks/                     # Google Colab notebooks (Data Science)
│   ├── 01_contextualizacao.ipynb
│   ├── 02_preparacao_dados.ipynb
│   ├── 03_estatistica_descritiva.ipynb
│   ├── 04_visualizacoes.ipynb
│   ├── 05_modelos_ml.ipynb
│   └── 06_perguntas_negocio.ipynb
├── src/
│   ├── ingestion/                 # coleta Sentinel-2 e INMET
│   ├── ndvi/                      # cálculo de índices vegetação
│   ├── models/                    # LSTM, RF, XGBoost, K-Means
│   └── utils/
├── database/                      # scripts SQL Oracle (Database Design)
│   ├── ddl/
│   │   └── agrosat_schema.sql
│   └── dml/
├── docs/                          # documentação Agile, requisitos
│   ├── product_backlog.md
│   ├── personas.md
│   └── requisitos.md
└── blender/                       # arquivos .blend (AR/VR)
    └── satellite_talhao.blend
```

---

## Personas

### 1. Analista de Crédito Rural
**Nome**: João Ribeiro | **Idade**: 31 | **Organização**: Fintech de crédito rural (Agrolend)
**Dor**: Aprova crédito olhando só para histórico financeiro; não sabe se a lavoura está saudável; inadimplência dispara quando tem seca
**Ganho com AgroSat**: Score de risco por talhão integrado ao processo de análise → reduz inadimplência em 15–25%

### 2. Gestora de Cooperativa
**Nome**: Ana Paula Mendes | **Idade**: 44 | **Organização**: Cooperativa agrícola (C.Vale)
**Dor**: Não sabe quanto vão colher os cooperados até 30 dias antes da safra → não consegue travar preço de venda, perde margem
**Ganho com AgroSat**: Forecast de safra com 60–90 dias de antecedência → hedge eficiente, planejamento de armazenagem

### 3. Produtor Rural
**Nome**: Carlos Motta | **Idade**: 52 | **Organização**: Fazenda própria (2.000 ha, soja/milho, MT)
**Dor**: Contrata seguro sem saber se está pagando preço justo; não monitora estresse hídrico em tempo real; depende de visita técnica cara
**Ganho com AgroSat**: App mostra saúde da lavoura por talhão, alerta precoce de estresse hídrico, comparação com vizinhos

---

## Banco de Dados — Entidades Principais

```sql
-- 6 tabelas obrigatórias (Database Design)
PROPERTY        (id, owner_id, area_ha, biome, municipality, state, lat, lon)
CROP_RECORD     (id, property_id, crop_type, planting_date, harvest_date, expected_yield_bags_ha)
SATELLITE_OBS   (id, property_id, obs_date, satellite, ndvi_mean, ndvi_std, evi_mean, cloud_cover_pct)
CLIMATE_DATA    (id, municipality, obs_date, temp_max_c, temp_min_c, precipitation_mm, humidity_pct)
RISK_ANALYSIS   (id, property_id, analysis_date, risk_score, risk_class, predicted_yield, model_version)
CREDIT_CONTRACT (id, property_id, creditor, amount_brl, interest_rate, term_months, risk_analysis_id)
```

---

## Referências GitHub

- [wildfire-risk-forecast](https://github.com/Sivarohitk/wildfire-risk-forecast) — pipeline LightGBM + Streamlit com dados NASA (padrão similar)
- [FlameForecast](https://github.com/jbric16/FlameForecast_Project) — CNN + LSTM para dados satelitais NASA
- [nasa-wildfires](https://github.com/datadesk/nasa-wildfires) — ingestão dados NASA FIRMS (mesmo padrão de API)
- [satellite-image-deep-learning](https://github.com/satellite-image-deep-learning/techniques) — técnicas DL para imagens satelitais

---

## Regras de Desenvolvimento

- Todo código Python deve rodar no Google Colab sem dependências locais pesadas
- Notebooks têm células Markdown entre cada seção (requisito Data Science)
- SQL compatível com Oracle 19c (requisito Database Design)
- Commits em inglês, comentários em português
- Dados reais: usar série NDVI calculada de Sentinel-2 real ou dataset Kaggle equivalente

---

## Entrega e Prazos

- **Data limite**: 09/06/2026 (23h59)
- **Data Science**: Google Colab público + executável
- **Agile**: PDF com documento + link YouTube pitch (máx 5 min)
- **Database**: PDF com DDL + Oracle Data Modeler (conceitual + lógico)
- **AR/VR**: PDF com 13+ prints Blender com legendas

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
