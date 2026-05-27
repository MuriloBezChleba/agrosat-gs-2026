# AgroSat — Requirements

**Project:** AgroSat — Plataforma de Inteligência Agrícola por Satélite
**Version:** v1 (Global Solution 2026 — Entrega 09/06/2026)
**Generated:** 2026-05-26

---

## v1 Requirements

### DATA — Ingestão e Preparação de Dados

- [ ] **DATA-01**: Notebook importa série temporal de NDVI via Python (CSV ou Google Earth Engine) com campos: property_id, obs_date, ndvi_mean, ndvi_std, evi_mean, cloud_cover_pct, satellite
- [ ] **DATA-02**: Notebook importa dados climáticos INMET: temperatura máx/mín, precipitação, umidade relativa por município/período
- [ ] **DATA-03**: Notebook inspeciona estrutura (dtypes, shape, head, info, describe) dos dois datasets
- [ ] **DATA-04**: Pipeline trata valores ausentes (fillna/dropna com justificativa) e remove duplicatas com contagem before/after
- [ ] **DATA-05**: Pipeline padroniza colunas (snake_case, tipos corretos, datas em datetime) e produz dataset final com 1.000+ registros
- [ ] **DATA-06**: Markdown documenta: problema (risco de crédito rural sem visibilidade de lavoura), relevância, relação com economia espacial (satélite Sentinel-2), objetivo da análise

### STATS — Estatística Descritiva

- [ ] **STATS-01**: Medidas de tendência central para NDVI e variáveis climáticas: média, mediana, moda
- [ ] **STATS-02**: Medidas de dispersão: amplitude, variância, desvio padrão, coeficiente de variação
- [ ] **STATS-03**: Medidas posicionais: Q1, Q2, Q3, percentis (10, 25, 50, 75, 90)
- [ ] **STATS-04**: Análise de outliers com IQR ou Z-Score identificando talhões anômalos (possíveis sinistros)
- [ ] **STATS-05**: Análise de distribuição interpreta: comportamento, assimetria, concentração, anomalias nos dados de NDVI
- [ ] **STATS-06**: Notebook responde mínimo 5 perguntas de negócio com evidências estatísticas
- [ ] **STATS-07**: Conclusão executiva Markdown: achados, insights, aplicações práticas, limitações

### VIZ — Visualizações

- [ ] **VIZ-01**: Histograma de distribuição de NDVI médio por talhão (com interpretação)
- [ ] **VIZ-02**: Boxplot de NDVI por cultura ou por região (com interpretação)
- [ ] **VIZ-03**: Gráfico de barras: top municípios por risco médio ou produtividade (com interpretação)
- [ ] **VIZ-04**: Scatterplot: NDVI vs precipitação acumulada ou temperatura (com interpretação)
- [ ] **VIZ-05**: Heatmap de correlação entre variáveis numéricas (NDVI, clima, produtividade)
- [ ] **VIZ-06**: Todas as visualizações têm título, eixos identificados e interpretação analítica escrita

### ML — Modelos de Machine Learning / Deep Learning

- [ ] **ML-01**: LSTM treinado em série temporal NDVI + clima para predição de produtividade (sacas/ha) em t+30 e t+60 dias, com RMSE reportado
- [ ] **ML-02**: Random Forest ou XGBoost treinado para scoring de risco por propriedade (BAIXO/MÉDIO/ALTO), com precision/recall/F1 reportados
- [ ] **ML-03**: K-Means (k=4–6) segmenta propriedades em clusters por perfil de risco e produtividade, com visualização dos clusters
- [ ] **ML-04**: Cada modelo tem pipeline documentado: pré-processamento → treino → avaliação → exemplo de inferência
- [ ] **ML-05**: Notebook compara métricas dos modelos em tabela resumo

### AGILE — Documentação Ágil

- [ ] **AGILE-01**: Documento apresenta nome (AgroSat), equipe (nome + RM), desafio (crédito rural sem visibilidade de risco) e solução proposta
- [ ] **AGILE-02**: Público-alvo com estimativas: mercado crédito rural R$300B+, CAGR precision agriculture 13%, impacto BACEN 4.945/2021
- [ ] **AGILE-03**: 3 personas: analista crédito (fintech), gestora cooperativa, produtor rural — com dores e ganhos
- [ ] **AGILE-04**: Mínimo 7 Requisitos Funcionais (O sistema deve...)
- [ ] **AGILE-05**: Mínimo 7 Requisitos Não-Funcionais (disponibilidade, latência, segurança, etc.)
- [ ] **AGILE-06**: Mínimo 7 Requisitos Técnicos (stack, protocolos, integrações)
- [ ] **AGILE-07**: Mínimo 7 Regras de Negócio
- [ ] **AGILE-08**: Product Backlog: Épicos + mínimo 12 Histórias de Usuário com Definition of Done
- [ ] **AGILE-09**: Vídeo Pitch YouTube ≤5min: problema, mercado, solução com esboços de telas

### DB — Banco de Dados

- [ ] **DB-01**: 6 tabelas: PROPERTY, CROP_RECORD, SATELLITE_OBS, CLIMATE_DATA, RISK_ANALYSIS, CREDIT_CONTRACT
- [ ] **DB-02**: Cada tabela tem descrição de significado e objetivo
- [ ] **DB-03**: Cada coluna: nome, tipo, tamanho, NOT NULL, PK/FK/UK, descrição
- [ ] **DB-04**: Diagrama conceitual Oracle Data Modeler (aba Logical): entidades, atributos, relacionamentos, cardinalidades
- [ ] **DB-05**: Diagrama lógico-relacional Oracle Data Modeler (aba Relational): tabelas, PKs, FKs, cardinalidades
- [ ] **DB-06**: DDL SQL Oracle 19c válido para todas as 6 tabelas
- [ ] **DB-07**: PDF com capa (título + nomes + RMs), sumário, objetivo, todos os itens acima

### ARVR — Modelagem 3D

- [ ] **ARVR-01**: Objeto 3D Blender: satélite Sentinel-2 com painéis solares e antenas
- [ ] **ARVR-02**: Objeto 3D Blender: talhão agrícola 3D com heatmap de NDVI aplicado como textura
- [ ] **ARVR-03**: Mínimo 13 prints com legendas explicativas
- [ ] **ARVR-04**: PDF com design/layout trabalhado
- [ ] **ARVR-05**: Objetos com complexidade técnica além de primitivas básicas

### DOCS — Documentação e Entrega

- [ ] **DOCS-01**: Colab público ("qualquer pessoa com link") e executável end-to-end
- [ ] **DOCS-02**: Todos os membros identificados (nome + RM) em todos entregáveis
- [ ] **DOCS-03**: PDFs entregues até 09/06/2026 23h59 via Teams/Portal do Aluno
- [ ] **DOCS-04**: README GitHub documenta estrutura do projeto e como rodar

---

## v2 Requirements (Deferred)

- Dashboard web em tempo real (React + MapLibre GL para mapas)
- API REST com autenticação (JWT) para integração com sistemas de crédito
- Integração Sentinel Hub paga para processamento de imagens raw
- Deploy cloud AWS/GCP com pipeline automatizado
- Alertas WhatsApp/SMS para produtores via Twilio

---

## Out of Scope

- Frontend web completo — prazo inviabiliza; Colab suficiente para demo
- API REST em produção — fora do escopo acadêmico
- Processamento raw de imagens Sentinel-2 (.tif) — usar NDVI pré-calculado
- Integração com sistemas bancários reais (BACEN, Open Finance) — risco e compliance
- Recomendação de insumos/defensivos — requer agrônomo certificado

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| DATA-01..06 | Phase 1 — Data Foundation | Pending |
| STATS-01..07 | Phase 2 — Statistical Analysis | Pending |
| VIZ-01..06 | Phase 2 — Statistical Analysis | Pending |
| ML-01..05 | Phase 3 — ML Models | Pending |
| DB-01..07 | Phase 4 — Database Design | Pending |
| AGILE-01..09 | Phase 5 — Agile Documentation | Pending |
| ARVR-01..05 | Phase 6 — 3D & Final Delivery | Pending |
| DOCS-01..04 | Phase 6 — 3D & Final Delivery | Pending |
