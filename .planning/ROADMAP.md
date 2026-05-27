# AstroSentinel — Roadmap

**Project:** AstroSentinel — Plataforma AI/ML de Monitoramento de Detritos Espaciais
**Milestone:** Global Solution 2026 — Entrega 09/06/2026
**Generated:** 2026-05-26
**Granularity:** Standard (6 phases)
**Coverage:** 44/44 v1 requirements mapped

---

## Phases

- [ ] **Phase 1: Data Foundation** — Import TLE data, clean, and prepare the analysis pipeline
- [ ] **Phase 2: Statistical Analysis & Visualizations** — Descriptive stats, 5 business questions, and all 5 required chart types
- [ ] **Phase 3: ML/DL Models** — LSTM trajectory prediction, Autoencoder anomaly detection, Random Forest classifier, DBSCAN clustering
- [ ] **Phase 4: Database Design** — Oracle relational model with 6 tables, DDL scripts, conceptual and logical diagrams
- [ ] **Phase 5: Agile Documentation** — Personas, requirements catalog, product backlog, pitch video
- [ ] **Phase 6: 3D Modeling & Final Delivery** — Blender 3D objects, 13 prints, compiled PDFs, finalized Colab

---

## Phase Details

### Phase 1: Data Foundation
**Goal**: The Colab notebook loads real TLE data from CelesTrak, cleans it, and produces a ready-to-analyze dataset of 1,000+ orbital objects.
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05, DATA-06
**Success Criteria** (what must be TRUE):
  1. Running the notebook cell imports TLE data from a public CelesTrak URL without authentication errors and produces a DataFrame.
  2. Notebook output shows shape, dtypes, and head confirming at least 1,000 rows with columns NORAD_ID, nome, tipo, altitude, inclinacao, eccentricidade, periodo, epoca.
  3. Notebook cells show explicit fillna/dropna calls with Markdown justifying each choice, and a duplicate-removal step with before/after row counts.
  4. A Markdown cell in the notebook explains the problem (space debris), its relevance to the space economy, and the analysis objective.
**Plans**: TBD

### Phase 2: Statistical Analysis & Visualizations
**Goal**: The notebook answers 5 business questions with complete descriptive statistics and all 5 mandatory chart types, each interpreted in writing.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: STATS-01, STATS-02, STATS-03, STATS-04, STATS-05, STATS-06, STATS-07, VIZ-01, VIZ-02, VIZ-03, VIZ-04, VIZ-05, VIZ-06
**Success Criteria** (what must be TRUE):
  1. Notebook cells display mean, median, and mode for each numeric variable; amplitude, variance, std deviation, and coefficient of variation; Q1/Q2/Q3 and percentiles 10/25/50/75/90.
  2. At least one outlier detection cell uses IQR or Z-Score and labels identified outliers in the output.
  3. The notebook contains exactly 5 labeled business question sections, each concluding with a statistical evidence statement tied to computed values.
  4. Five distinct chart cells are present and render: histogram, boxplot, bar chart, scatter plot, heatmap — each with title, axis labels, and a written analytical interpretation below.
  5. A Markdown conclusion cell summarizes key findings, insights, practical applications, and known limitations of the analysis.
**Plans**: TBD

### Phase 3: ML/DL Models
**Goal**: The notebook trains and evaluates four models — LSTM, Autoencoder, Random Forest, DBSCAN — and documents the full ML pipeline from preprocessing to inference.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: ML-01, ML-02, ML-03, ML-04, ML-05, ML-06
**Success Criteria** (what must be TRUE):
  1. LSTM model cell trains on historical TLE sequences and outputs RMSE for t+1h, t+6h, and t+24h prediction horizons.
  2. Autoencoder model cell trains and outputs reconstruction error distribution; a threshold cell flags anomalous objects.
  3. Random Forest model cell outputs a classification report showing precision, recall, and F1 for VERDE/AMARELO/VERMELHO risk classes.
  4. DBSCAN (or K-Means) clustering cell produces a labeled scatter plot of debris density regions by altitude x inclination.
  5. A pipeline summary Markdown documents each step: preprocessing, training, evaluation, and a sample inference call for each model.
**Plans**: TBD

### Phase 4: Database Design
**Goal**: A PDF deliverable presents the complete Oracle relational model — 6 tables with DDL scripts, column specifications, and both conceptual and logical diagrams.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: DB-01, DB-02, DB-03, DB-04, DB-05, DB-06, DB-07
**Success Criteria** (what must be TRUE):
  1. The document lists all 6 required tables (ORBITAL_OBJECT, OBSERVATION, CONJUNCTION, RISK_ALERT, SATELLITE_OP, DECAY_FORECAST), each with a purpose description.
  2. Every column definition shows name, data type, size, NOT NULL constraint where applicable, and PK/FK/UK designation with a description.
  3. Oracle Data Modeler screenshots show a conceptual diagram (entities, attributes, cardinalities) and a logical/relational diagram (tables, PKs, FKs).
  4. DDL SQL script executes without errors on Oracle 19c and creates all 6 tables with correct constraints.
  5. PDF has a cover page (title + team member names and RMs) and a table of contents.
**Plans**: TBD

### Phase 5: Agile Documentation
**Goal**: A PDF deliverable presents the complete Agile artifact set — personas, full requirements catalog, product backlog with 12+ user stories, and a YouTube pitch video.
**Mode:** mvp
**Depends on**: Nothing (can run in parallel with Phases 1-4)
**Requirements**: AGILE-01, AGILE-02, AGILE-03, AGILE-04, AGILE-05, AGILE-06, AGILE-07, AGILE-08, AGILE-09
**Success Criteria** (what must be TRUE):
  1. Document contains project name, all team members (name + RM), challenge description, and proposed solution in the opening section.
  2. Three personas are documented with name, age, organization, pains, and gains for each (operations engineer, policy analyst, researcher).
  3. Requirements section lists at least 7 Functional Requirements, 7 Non-Functional Requirements, 7 Technical Requirements, and 7 Business Rules, each in the specified format.
  4. Product Backlog section contains Epics and at least 12 User Stories with Definition of Done for each story.
  5. A YouTube video (up to 5 minutes, accessible via private link) shows problem, market opportunity, proposed solution, and screen sketches.
**Plans**: TBD

### Phase 6: 3D Modeling & Final Delivery
**Goal**: The Blender 3D model deliverable is complete and all PDFs are compiled, submitted, and the Colab link is finalized for submission by 09/06/2026.
**Mode:** mvp
**Depends on**: Phases 1, 2, 3, 4, 5
**Requirements**: ARVR-01, ARVR-02, ARVR-03, ARVR-04, ARVR-05, DOCS-01, DOCS-02, DOCS-03, DOCS-04
**Success Criteria** (what must be TRUE):
  1. Blender file contains at least 1 space-themed 3D object (satellite, debris, spacecraft, or station) that goes beyond basic primitives and includes elements like solar panels, antennae, or orbital structures.
  2. PDF document contains at least 13 captioned screenshots of the Blender model from different angles and construction stages.
  3. Colab notebook is set to "Anyone with the link can view" and all cells execute end-to-end without errors.
  4. All PDF deliverables (Database Design, Agile, AR/VR) include full team identification (name + RM) on the cover or first page.
  5. All files are submitted via Teams/Portal do Aluno before 09/06/2026 23h59, and the GitHub README documents project structure and execution instructions.
**Plans**: TBD
**UI hint**: yes

---

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Data Foundation | 0/? | Not started | - |
| 2. Statistical Analysis & Visualizations | 0/? | Not started | - |
| 3. ML/DL Models | 0/? | Not started | - |
| 4. Database Design | 0/? | Not started | - |
| 5. Agile Documentation | 0/? | Not started | - |
| 6. 3D Modeling & Final Delivery | 0/? | Not started | - |

---

## Coverage Map

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Pending |
| DATA-02 | Phase 1 | Pending |
| DATA-03 | Phase 1 | Pending |
| DATA-04 | Phase 1 | Pending |
| DATA-05 | Phase 1 | Pending |
| DATA-06 | Phase 1 | Pending |
| STATS-01 | Phase 2 | Pending |
| STATS-02 | Phase 2 | Pending |
| STATS-03 | Phase 2 | Pending |
| STATS-04 | Phase 2 | Pending |
| STATS-05 | Phase 2 | Pending |
| STATS-06 | Phase 2 | Pending |
| STATS-07 | Phase 2 | Pending |
| VIZ-01 | Phase 2 | Pending |
| VIZ-02 | Phase 2 | Pending |
| VIZ-03 | Phase 2 | Pending |
| VIZ-04 | Phase 2 | Pending |
| VIZ-05 | Phase 2 | Pending |
| VIZ-06 | Phase 2 | Pending |
| ML-01 | Phase 3 | Pending |
| ML-02 | Phase 3 | Pending |
| ML-03 | Phase 3 | Pending |
| ML-04 | Phase 3 | Pending |
| ML-05 | Phase 3 | Pending |
| ML-06 | Phase 3 | Pending |
| DB-01 | Phase 4 | Pending |
| DB-02 | Phase 4 | Pending |
| DB-03 | Phase 4 | Pending |
| DB-04 | Phase 4 | Pending |
| DB-05 | Phase 4 | Pending |
| DB-06 | Phase 4 | Pending |
| DB-07 | Phase 4 | Pending |
| AGILE-01 | Phase 5 | Pending |
| AGILE-02 | Phase 5 | Pending |
| AGILE-03 | Phase 5 | Pending |
| AGILE-04 | Phase 5 | Pending |
| AGILE-05 | Phase 5 | Pending |
| AGILE-06 | Phase 5 | Pending |
| AGILE-07 | Phase 5 | Pending |
| AGILE-08 | Phase 5 | Pending |
| AGILE-09 | Phase 5 | Pending |
| ARVR-01 | Phase 6 | Pending |
| ARVR-02 | Phase 6 | Pending |
| ARVR-03 | Phase 6 | Pending |
| ARVR-04 | Phase 6 | Pending |
| ARVR-05 | Phase 6 | Pending |
| DOCS-01 | Phase 6 | Pending |
| DOCS-02 | Phase 6 | Pending |
| DOCS-03 | Phase 6 | Pending |
| DOCS-04 | Phase 6 | Pending |

**Total: 49/49 requirements mapped** (DATA: 6, STATS: 7, VIZ: 6, ML: 6, DB: 7, AGILE: 9, ARVR: 5, DOCS: 4)

---

*Last updated: 2026-05-26 after roadmap initialization*
