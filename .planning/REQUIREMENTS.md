# AstroSentinel — Requirements

**Project:** AstroSentinel — Plataforma AI/ML de Monitoramento de Detritos Espaciais
**Version:** v1 (Global Solution 2026 — Entrega 09/06/2026)
**Generated:** 2026-05-26

---

## v1 Requirements

### DATA — Ingestão e Preparação de Dados

- [ ] **DATA-01**: Sistema importa dados TLE públicos da CelesTrak (arquivo .txt ou .csv) via Python
- [ ] **DATA-02**: Notebook inspeciona estrutura dos dados (dtypes, shape, head, info)
- [ ] **DATA-03**: Pipeline identifica e trata valores ausentes (fillna / dropna com justificativa)
- [ ] **DATA-04**: Pipeline remove linhas duplicadas e padroniza colunas (snake_case, tipos corretos)
- [ ] **DATA-05**: Dataset final contém mínimo 1.000 registros de objetos orbitais com campos: NORAD_ID, nome, tipo, altitude (km), inclinação (deg), eccentricidade, período (min), época
- [ ] **DATA-06**: Notebook documenta em Markdown: problema escolhido, relevância, relação com economia espacial, objetivo da análise

### STATS — Estatística Descritiva

- [ ] **STATS-01**: Medidas de tendência central calculadas para variáveis numéricas: média, mediana, moda
- [ ] **STATS-02**: Medidas de dispersão calculadas: amplitude, variância, desvio padrão, coeficiente de variação
- [ ] **STATS-03**: Medidas posicionais calculadas: Q1, Q2, Q3, percentis (10, 25, 50, 75, 90)
- [ ] **STATS-04**: Análise de outliers aplicada com mínimo 1 método: IQR ou Z-Score
- [ ] **STATS-05**: Análise de distribuição interpreta: comportamento das distribuições, assimetria, concentração, anomalias
- [ ] **STATS-06**: Notebook responde mínimo 5 perguntas de negócio sustentadas por evidências estatísticas
- [ ] **STATS-07**: Conclusão executiva em Markdown: principais achados, insights, aplicações práticas, limitações

### VIZ — Visualizações

- [ ] **VIZ-01**: Histograma construído e interpretado (título, eixos, análise escrita)
- [ ] **VIZ-02**: Boxplot construído e interpretado
- [ ] **VIZ-03**: Gráfico de barras construído e interpretado
- [ ] **VIZ-04**: Scatterplot construído e interpretado
- [ ] **VIZ-05**: Heatmap de correlação construído e interpretado
- [ ] **VIZ-06**: Todas as visualizações têm título, identificação adequada dos eixos e interpretação analítica escrita

### ML — Modelos de Machine Learning / Deep Learning

- [ ] **ML-01**: Modelo LSTM treinado para predição de trajetória orbital (t+1h, t+6h, t+24h) com dados TLE históricos
- [ ] **ML-02**: Autoencoder treinado para detecção de anomalias em parâmetros orbitais (decay anômalo)
- [ ] **ML-03**: Random Forest treinado para classificação de risco de colisão (VERDE/AMARELO/VERMELHO + probabilidade)
- [ ] **ML-04**: Clustering DBSCAN ou K-Means identifica regiões de alta densidade de detritos por altitude × inclinação
- [ ] **ML-05**: Cada modelo apresenta métricas de avaliação (RMSE para LSTM, precision/recall/F1 para RF, reconstruction error para Autoencoder)
- [ ] **ML-06**: Notebook documenta pipeline completo: pré-processamento → treino → avaliação → inferência

### AGILE — Documentação Ágil (Metodologia Ágil)

- [ ] **AGILE-01**: Documento apresenta nome do projeto, composição da equipe (nome + RM), descrição do desafio e solução proposta
- [ ] **AGILE-02**: Público-alvo definido com estimativas de impacto fundamentadas em dados de mercado/estatísticas
- [ ] **AGILE-03**: Mínimo 3 personas documentadas com nome, idade, organização, dores e ganhos
- [ ] **AGILE-04**: Mínimo 7 Requisitos Funcionais documentados (formato: O sistema deve...)
- [ ] **AGILE-05**: Mínimo 7 Requisitos Não-Funcionais documentados (desempenho, segurança, usabilidade, etc.)
- [ ] **AGILE-06**: Mínimo 7 Requisitos Técnicos documentados (stack, protocolos, padrões)
- [ ] **AGILE-07**: Mínimo 7 Regras de Negócio documentadas
- [ ] **AGILE-08**: Product Backlog com Épicos, mínimo 12 Histórias de Usuário e Definition of Done para cada
- [ ] **AGILE-09**: Vídeo Pitch de até 5 minutos no YouTube (privado com link) mostrando problema, oportunidade, solução com esboços de telas

### DB — Banco de Dados (Database Design)

- [ ] **DB-01**: Modelo relacional contém mínimo 6 tabelas: ORBITAL_OBJECT, OBSERVATION, CONJUNCTION, RISK_ALERT, SATELLITE_OP, DECAY_FORECAST
- [ ] **DB-02**: Cada tabela tem descrição do significado e objetivo
- [ ] **DB-03**: Cada coluna tem: nome, tipo, tamanho, NOT NULL onde aplicável, PK/FK/UK indicados, descrição
- [ ] **DB-04**: Diagrama conceitual (entidades) criado no Oracle Data Modeler (aba Logical) com entidades, atributos, relacionamentos e cardinalidades
- [ ] **DB-05**: Diagrama lógico-relacional criado no Oracle Data Modeler (aba Relational) com tabelas, PKs, FKs, relacionamentos, cardinalidades
- [ ] **DB-06**: Scripts DDL SQL Oracle válidos para criação das tabelas
- [ ] **DB-07**: Documento PDF contém capa (título + integrantes), sumário, objetivo e todos os itens acima

### ARVR — Modelagem 3D (AR/VR)

- [ ] **ARVR-01**: Mínimo 1 objeto 3D modelado no Blender com tema "Viagens Espaciais" (satélite, debris, nave, estação)
- [ ] **ARVR-02**: Mínimo 13 prints do objeto 3D com legendas explicativas
- [ ] **ARVR-03**: Documento PDF com design e layout bem trabalhado
- [ ] **ARVR-04**: Objetos demonstram complexidade técnica (não apenas primitivas básicas)
- [ ] **ARVR-05**: Representação coerente com o tema espacial (placas solares, antenas, estruturas orbitais)

### DOCS — Documentação e Entrega

- [ ] **DOCS-01**: Notebook Google Colab totalmente funcional com permissão "qualquer pessoa com link pode visualizar"
- [ ] **DOCS-02**: Todos os membros da equipe identificados (nome completo + RM) em todos os entregáveis
- [ ] **DOCS-03**: Arquivos PDF entregues dentro do prazo (09/06/2026 às 23h59) via Teams/Portal do Aluno
- [ ] **DOCS-04**: README do repositório GitHub documenta estrutura do projeto e instruções de execução

---

## v2 Requirements (Deferred)

- Interface web dashboard em tempo real (React + WebSockets)
- Integração com Space-Track.org API autenticada para CDM (Conjunction Data Messages)
- Sistema de notificação push/email para operadores
- Deploy em cloud (AWS/GCP) com pipeline automatizado
- Modelo de language para geração automática de relatórios (LLM)

---

## Out of Scope

- Frontend web completo — prazo de 14 dias inviabiliza; Colab é suficiente para demonstração
- API REST em produção — fora do escopo acadêmico desta GS
- Dados de satélites militares/classificados — usar apenas fontes públicas
- Manobra autônoma de satélites — fora do escopo ético e técnico
- Integração com sistemas de controle de missão reais — risco operacional

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| DATA-01 to DATA-06 | Phase 1 | Pending |
| STATS-01 to STATS-07 | Phase 2 | Pending |
| VIZ-01 to VIZ-06 | Phase 2 | Pending |
| ML-01 to ML-06 | Phase 3 | Pending |
| DB-01 to DB-07 | Phase 4 | Pending |
| AGILE-01 to AGILE-09 | Phase 5 | Pending |
| ARVR-01 to ARVR-05 | Phase 6 | Pending |
| DOCS-01 to DOCS-04 | All Phases | Pending |
