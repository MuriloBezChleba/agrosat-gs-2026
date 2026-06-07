# AgroSat — Roadmap

**Project:** AgroSat — Plataforma de Inteligência Agrícola por Satélite
**Milestone:** Global Solution 2026 — Entrega 09/06/2026
**Generated:** 2026-05-26 (updated after pivot from AstroSentinel)
**Granularity:** Standard (6 phases + Python GS)
**Coverage:** 47/47 v1 requirements mapped + Python GS arquitetado

---

## Phases

- [ ] **Phase 1: Data Foundation** — Importar NDVI + clima, limpar, preparar dataset analítico
- [ ] **Phase 2: Statistical Analysis & Visualizations** — Estatística descritiva completa, 5 perguntas de negócio, 5 tipos de gráfico
- [ ] **Phase 3: ML/DL Models** — LSTM produtividade, XGBoost risco, K-Means segmentação
- [ ] **Phase 4: Database Design** — Modelo Oracle 6 tabelas, DDL, diagramas conceitual e lógico
- [ ] **Phase 5: Agile Documentation** — Personas, requisitos, backlog 12+ US, pitch video
- [ ] **Phase 6: 3D Modeling & Final Delivery** — Blender satélite + talhão, 13+ prints, PDFs finais
- [ ] **Phase 7: Python GS (Estruturas de Dados)** — AgroSat CLI: pilha + fila + lista ligada + busca + ordenação + terminal Rich

---

## Phase Details

### Phase 1: Data Foundation
**Goal:** Notebook Colab carrega série temporal NDVI (Sentinel-2) + dados climáticos INMET, limpa e produz dataset analítico com 1.000+ registros pronto para análise.
**Mode:** mvp
**Depends on:** Nothing (first phase)
**Requirements:** DATA-01, DATA-02, DATA-03, DATA-04, DATA-05, DATA-06
**Success Criteria:**
  1. Célula importa dados NDVI de fonte pública (GEE ou Kaggle) sem erro e produz DataFrame com shape confirmado no output.
  2. Output confirma 1.000+ linhas com colunas: property_id, obs_date, ndvi_mean, ndvi_std, evi_mean, cloud_cover_pct, satellite.
  3. Células de fillna/dropna mostram justificativa em Markdown; célula de deduplicação mostra contagem before/after.
  4. Célula Markdown explica o problema (crédito rural sem visibilidade), relevância, conexão com economia espacial (satélite), objetivo.
**Plans:** TBD

### Phase 2: Statistical Analysis & Visualizations
**Goal:** Notebook responde 5 perguntas de negócio com estatística descritiva completa e 5 tipos de gráfico obrigatórios, cada um interpretado em texto.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** STATS-01, STATS-02, STATS-03, STATS-04, STATS-05, STATS-06, STATS-07, VIZ-01, VIZ-02, VIZ-03, VIZ-04, VIZ-05, VIZ-06
**Success Criteria:**
  1. Células calculam e exibem média/mediana/moda, amplitude/variância/desvio padrão/CV, Q1/Q2/Q3 e percentis 10/25/50/75/90 para NDVI e variáveis climáticas.
  2. Célula de outliers usa IQR ou Z-Score e identifica talhões com NDVI anômalo (possíveis sinistros).
  3. 5 seções de perguntas de negócio, cada uma conclui com evidência estatística citando valor calculado (ex: "o desvio padrão de 0.23 indica...").
  4. 5 gráficos distintos renderizam: histograma NDVI, boxplot por cultura, barras por município, scatter NDVI×precipitação, heatmap correlação — cada um com título, eixos e interpretação escrita abaixo.
  5. Célula Markdown de conclusão resume achados principais, insights, aplicações práticas e limitações.
**Plans:** TBD

### Phase 3: ML/DL Models
**Goal:** Notebook treina e avalia 3 modelos — LSTM (produtividade), XGBoost (risco), K-Means (segmentação) — com métricas e pipeline documentado.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** ML-01, ML-02, ML-03, ML-04, ML-05
**Success Criteria:**
  1. LSTM treina em séries temporais NDVI+clima e reporta RMSE para t+30 e t+60 dias de produtividade.
  2. XGBoost treina classificador de risco (BAIXO/MÉDIO/ALTO) e exibe classification report com precision/recall/F1 por classe.
  3. K-Means (k=4–6) produz scatter plot colorido de clusters de propriedades por perfil de risco/produtividade.
  4. Cada modelo tem seção Markdown documentando: pré-processamento, treino, avaliação, exemplo de inferência.
  5. Tabela resumo compara métricas dos 3 modelos.
**Plans:** TBD

### Phase 4: Database Design
**Goal:** PDF entregável apresenta modelo Oracle relacional completo — 6 tabelas, DDL, especificação de colunas, diagramas conceitual e lógico.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** DB-01, DB-02, DB-03, DB-04, DB-05, DB-06, DB-07
**Success Criteria:**
  1. Documento lista 6 tabelas (PROPERTY, CROP_RECORD, SATELLITE_OBS, CLIMATE_DATA, RISK_ANALYSIS, CREDIT_CONTRACT) cada com descrição.
  2. Toda coluna tem: nome, tipo Oracle, tamanho, NOT NULL onde aplicável, PK/FK/UK indicados, descrição.
  3. Screenshots Oracle Data Modeler mostram diagrama conceitual (Logical) e lógico-relacional (Relational) com cardinalidades.
  4. DDL SQL executa sem erros no Oracle 19c e cria as 6 tabelas com constraints corretos.
  5. PDF tem capa (título + nomes + RMs) e sumário.
**Plans:** TBD

### Phase 5: Agile Documentation
**Goal:** PDF apresenta conjunto Agile completo — personas, 7+ requisitos por categoria, backlog 12+ US com DoD, vídeo pitch no YouTube.
**Mode:** mvp
**Depends on:** Nothing (pode rodar em paralelo com Phases 1-4)
**Requirements:** AGILE-01, AGILE-02, AGILE-03, AGILE-04, AGILE-05, AGILE-06, AGILE-07, AGILE-08, AGILE-09
**Success Criteria:**
  1. Seção de abertura: nome AgroSat, todos os membros (nome + RM), desafio de crédito rural, solução.
  2. Público-alvo com dados: mercado crédito rural R$300B+, CAGR 13%, impacto BACEN 4.945/2021.
  3. 3 personas documentadas: analista crédito (fintech), gestora cooperativa, produtor rural — cada com nome, idade, org, dores, ganhos.
  4. Mínimo 7 de cada: Requisitos Funcionais, Não-Funcionais, Técnicos e Regras de Negócio.
  5. Product Backlog com Épicos e 12+ Histórias de Usuário com Definition of Done.
  6. Vídeo YouTube ≤5min (link privado acessível) com problema, oportunidade, solução e esboços de tela.
**Plans:** TBD

### Phase 6: 3D Modeling & Final Delivery
**Goal:** Blender entregável completo (satélite + talhão 3D, 13+ prints) e todos os PDFs compilados, links finalizados e submetidos até 09/06/2026.
**Mode:** mvp
**Depends on:** Phases 1, 2, 3, 4, 5
**Requirements:** ARVR-01, ARVR-02, ARVR-03, ARVR-04, ARVR-05, DOCS-01, DOCS-02, DOCS-03, DOCS-04
**Success Criteria:**
  1. Blender: satélite Sentinel-2 3D com painéis solares, antenas, complexidade além de primitivas básicas.
  2. Blender: talhão agrícola 3D com heatmap NDVI aplicado como textura (verde/amarelo/vermelho).
  3. PDF AR/VR contém 13+ prints de ângulos variados com legendas explicativas.
  4. Colab configurado como "qualquer pessoa com link pode visualizar" e executa end-to-end sem erros.
  5. Todos os PDFs entregues via Teams/Portal antes de 09/06/2026 23h59 com nome+RM de todos os membros.
**Plans:** TBD

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
| 7. Python GS — AgroSat CLI | 1/4 fases (arquitetado) | Planejado | - |

---

## Coverage Map

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01..06 | Phase 1 | Pending |
| STATS-01..07 | Phase 2 | Pending |
| VIZ-01..06 | Phase 2 | Pending |
| ML-01..05 | Phase 3 | Pending |
| DB-01..07 | Phase 4 | Pending |
| AGILE-01..09 | Phase 5 | Pending |
| ARVR-01..05 | Phase 6 | Pending |
| DOCS-01..04 | Phase 6 | Pending |

**Total: 47/47 requirements mapped**

---

*Last updated: 2026-05-26 after pivot to AgroSat (agricultural satellite intelligence)*
