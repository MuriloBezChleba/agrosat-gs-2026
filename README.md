# AgroSat 🛰️

**Plataforma de Inteligência Agrícola por Satélite**

Startup que transforma imagens do satélite Sentinel-2 em score de risco para fintechs liberarem crédito rural com segurança.

---

## O Problema

Fintechs de crédito rural emprestam **R$300B+/ano** sem visibilidade real de risco por talhão. Quando vem seca, produtor não paga — prejuízo para o banco. Dados que resolvem isso existem e são **gratuitos** (satélite Sentinel-2, ESA) — mas ninguém processou para esses clientes.

## A Solução

Pipeline completo: imagem satelital → NDVI → modelos ML → score de risco por propriedade.

```
Sentinel-2 (foto do satélite)
    ↓
NDVI (índice de saúde da vegetação)
    ↓
LSTM → prediz produtividade (sacas/ha)
XGBoost → score de risco 0–100 (BAIXO/MÉDIO/ALTO)
K-Means → segmenta perfis de propriedade
    ↓
API → fintech, cooperativa, seguradora
```

## Quem Paga

| Cliente | Dor | Produto |
|---|---|---|
| Fintechs crédito rural | Inadimplência por sinistro climático | Score de risco por talhão via API |
| Cooperativas agrícolas | Sem forecast de safra para planejar venda | Predição de produtividade 60–90 dias |
| Seguradoras rurais | Sinistros mal precificados | Scoring de portfólio por região |

## Contexto Regulatório

**BACEN Resolução 4.945/2021** — bancos são obrigados a avaliar risco climático em operações de crédito. AgroSat entrega essa análise automatizada.

---

## Projeto Acadêmico

**Global Solution 2026 — FIAP | 2º ano Engenharia de Software | Tema: Space Economy**

| Disciplina | Entregável |
|---|---|
| Data Science | Notebook Google Colab — análise estatística NDVI por região agrícola |
| Agile Methodology | PDF — personas, requisitos, backlog 12+ US, pitch YouTube |
| Database Design | PDF — modelo Oracle 6 tabelas, DDL, diagramas |
| AR/VR | PDF — satélite Sentinel-2 3D + talhão NDVI no Blender |

**Prazo:** 09/06/2026

---

## Stack

- **Python 3.11+** — pandas, numpy, scikit-learn, TensorFlow/Keras, XGBoost
- **Dados:** Sentinel-2 (ESA Copernicus), INMET, MapBiomas, IBGE — todos gratuitos
- **DB:** Oracle 19c
- **3D:** Blender 4.x
- **Plataforma:** Google Colab

## Como Rodar

```bash
# Clone
git clone https://github.com/MuriloBezChleba/GS.git
cd GS

# Abrir notebooks no Google Colab
# notebooks/01_contextualizacao.ipynb
# notebooks/02_preparacao_dados.ipynb
# notebooks/03_estatistica_descritiva.ipynb
# notebooks/04_visualizacoes.ipynb
# notebooks/05_modelos_ml.ipynb
```

## Planejamento (GSD)

```
.planning/
├── PROJECT.md       # contexto e decisões do projeto
├── REQUIREMENTS.md  # 47 requisitos mapeados
├── ROADMAP.md       # 6 fases com critérios de aceite
├── STATE.md         # estado atual e próximos passos
└── config.json      # configuração GSD
```

---

## Referências

- [Satellites on Fire](https://thenextweb.com/news/satellites-on-fire-wildfire-ai-raises-2-7m) — startup similar levantou $2.7M, Aon como cliente
- [wildfire-risk-forecast](https://github.com/Sivarohitk/wildfire-risk-forecast) — pipeline LightGBM + dados satelitais
- [satellite-image-deep-learning](https://github.com/satellite-image-deep-learning/techniques) — técnicas DL para imagens satelitais
- [ESA Copernicus Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) — fonte dos dados
