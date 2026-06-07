# AgroSat CLI — Python GS Architecture Plan

**Disciplina:** Estruturas de Dados  
**Entrega:** 09/06/2026  
**Tema:** Economia Espacial → Agricultura de Precisão via Satélite  

---

## Conceito

**AgroSat CLI** — aplicação terminal que carrega série temporal de NDVI (Sentinel-2) + dados climáticos, permite busca, ordenação e análise de risco de propriedades rurais via estruturas de dados clássicas implementadas do zero.

O sistema simula o fluxo de um analista de crédito rural:
1. Carrega base de talhões com observações NDVI
2. Busca propriedades por ID ou município
3. Ordena por risco, NDVI ou data
4. Processa fila de análises em lote
5. Consulta histórico de análises (pilha)

---

## Requisitos Obrigatórios → Mapeamento

| Requisito GS | Implementação AgroSat | Arquivo |
|---|---|---|
| **Pilha** | Histórico de análises (últimas 20) — pop reverte para análise anterior | `src/structures/stack.py` |
| **Fila** | Fila de processamento em lote — enqueue propriedades, processa FIFO | `src/structures/queue.py` |
| **Lista Ligada** | Sequência de observações satelitais por talhão (lista duplamente ligada, percorre forward/backward) | `src/structures/linked_list.py` |
| **Busca Binária** | Busca propriedade por ID em lista ordenada — O(log n) | `src/algorithms/search.py` |
| **Busca Linear** | Busca propriedades por município (sem pré-ordenação) | `src/algorithms/search.py` |
| **Quick Sort** | Ordena talhões por NDVI médio ou score de risco | `src/algorithms/sort.py` |
| **Merge Sort** | Ordena observações por data dentro de cada talhão | `src/algorithms/sort.py` |
| **Manipulação de arquivos** | Leitura CSV, escrita de log, exportação de resultados JSON | `src/data/loader.py`, `src/utils/logger.py` |
| **Modularização** | 7 módulos src + main.py + data classes separadas | estrutura de pacotes |
| **Try/except** | Todas leituras de arquivo, parsing de datas, cálculos de risco | disseminado |
| **Logs** | Logging em `logs/agrosat.log` + console colorido | `src/utils/logger.py` |
| **Interface terminal** | Menu interativo com Rich (tabelas, progresso, cores) | `src/ui/terminal.py` |

---

## Estrutura de Arquivos

```
python_gs/
├── main.py                      # Entry point — menu loop principal
├── requirements.txt
├── data/
│   ├── ndvi_series.csv          # ~2.000 obs: property_id, obs_date, ndvi_mean, ndvi_std, culture, municipality
│   └── climate_data.csv         # temp_max, temp_min, precipitation, humidity por município/data
├── src/
│   ├── __init__.py
│   ├── structures/
│   │   ├── __init__.py
│   │   ├── linked_list.py       # DoublyLinkedList[Observation] — traversal bidirecional
│   │   ├── stack.py             # Stack[AnalysisResult] — histórico LIFO
│   │   └── queue.py             # Queue[PropertyId] — fila de processamento FIFO
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── search.py            # linear_search(), binary_search()
│   │   └── sort.py              # quick_sort(), merge_sort()
│   ├── models/
│   │   ├── __init__.py
│   │   └── property.py          # dataclasses: Property, Observation, AnalysisResult
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py            # load_ndvi_csv(), load_climate_csv(), merge_datasets()
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── risk.py              # calculate_risk_score(), classify_risk()
│   └── utils/
│       ├── __init__.py
│       └── logger.py            # setup_logger(), log_operation()
└── logs/
    └── agrosat.log
```

---

## Modelos de Dados

```python
# src/models/property.py

@dataclass
class Observation:
    obs_date: date
    ndvi_mean: float
    ndvi_std: float
    evi_mean: float
    cloud_cover_pct: float
    satellite: str

@dataclass
class Property:
    property_id: str
    municipality: str
    state: str
    area_ha: float
    culture: str
    observations: DoublyLinkedList  # lista ligada de Observation

@dataclass
class AnalysisResult:
    property_id: str
    analysis_date: datetime
    risk_score: float           # 0–100
    risk_class: str             # BAIXO / MÉDIO / ALTO
    ndvi_trend: str             # CRESCENTE / ESTÁVEL / DECLINANTE
    recommendation: str
```

---

## Estruturas de Dados — Implementação

### DoublyLinkedList (src/structures/linked_list.py)

Armazena observações NDVI de um talhão em ordem cronológica. Cada nó aponta para anterior e próximo, permitindo percorrer da mais antiga à mais recente (ou inverso).

```
[obs jan] ↔ [obs fev] ↔ [obs mar] ↔ [obs abr] ↔ None
```

Operações:
- `append(obs)` — adiciona observação mais recente no final
- `prepend(obs)` — adiciona no início
- `remove(obs_date)` — remove por data
- `find(obs_date)` — retorna nó por data
- `to_list()` — converte para list[Observation]
- `__iter__` — permite `for obs in property.observations`

### Stack (src/structures/stack.py)

Armazena últimas 20 análises de risco. Analista consulta histórico sem perder análise atual.

```
[análise 5 ← topo]
[análise 4]
[análise 3]
[análise 2]
[análise 1 ← base]
```

Operações:
- `push(result: AnalysisResult)` — adiciona análise (descarta oldest se size > 20)
- `pop() -> AnalysisResult` — remove e retorna última análise
- `peek() -> AnalysisResult` — consulta sem remover
- `is_empty()`, `size()`

### Queue (src/structures/queue.py)

Fila de processamento em lote — usuário enfileira N propriedades, sistema processa em ordem.

```
[P-001] → [P-002] → [P-003] → [P-004]
 front                           rear
```

Operações:
- `enqueue(property_id: str)` — adiciona no rear
- `dequeue() -> str` — remove do front
- `peek_front() -> str` — consulta sem remover
- `is_empty()`, `size()`

---

## Algoritmos

### search.py

```python
def linear_search(properties: list[Property], municipality: str) -> list[Property]:
    """Busca por município — percorre toda lista. O(n)."""
    ...

def binary_search(sorted_properties: list[Property], property_id: str) -> Property | None:
    """Busca por ID em lista ordenada. O(log n). Requer quick_sort() primeiro."""
    ...
```

### sort.py

```python
def quick_sort(items: list, key: Callable, low: int = 0, high: int = None) -> list:
    """Quick sort in-place por chave genérica (ndvi_mean, risk_score, etc.)."""
    ...

def merge_sort(items: list, key: Callable) -> list:
    """Merge sort — ordena observações por data dentro de um talhão."""
    ...
```

---

## Fluxo Principal (main.py)

```
┌─────────────────────────────────────────────┐
│               AgroSat CLI                   │
│       Inteligência Agrícola por Satélite    │
└─────────────────────────────────────────────┘

[1] Carregar dados (CSV → lista de Property com LinkedList de obs)
[2] Buscar propriedade por ID       ← binary_search
[3] Buscar propriedades por município ← linear_search
[4] Ordenar talhões por NDVI        ← quick_sort
[5] Ordenar talhões por risco       ← quick_sort
[6] Analisar risco de propriedade   ← push resultado na Stack
[7] Processar fila em lote          ← Queue → risk.py → Stack
[8] Ver histórico de análises       ← Stack.peek/pop
[9] Exportar resultados (JSON/CSV)
[0] Sair
```

---

## Dataset

**ndvi_series.csv** — 2.000+ linhas sintéticas mas realistas, geradas com `numpy` uma vez e salvas:

```
property_id,municipality,state,culture,area_ha,obs_date,ndvi_mean,ndvi_std,evi_mean,cloud_cover_pct,satellite
PR-0001,Cascavel,PR,soja,1250.5,2023-01-15,0.72,0.08,0.65,5.2,Sentinel-2
PR-0001,Cascavel,PR,soja,1250.5,2023-02-15,0.68,0.11,0.61,12.0,Sentinel-2
...
```

200 propriedades × 10 obs = 2.000 registros. Representa safra 2023/2024 no Paraná.

**climate_data.csv** — temperatura e precipitação por município/data (join com NDVI por município+data).

Script de geração incluso em `data/generate_dataset.py` para reproducibilidade.

---

## Análise de Risco (src/analysis/risk.py)

Score 0–100 baseado em:
- NDVI médio últimos 30 dias (peso 40%)
- Tendência NDVI (crescente/declinante) (peso 25%)
- Precipitação acumulada vs. normal histórica (peso 20%)
- Cobertura de nuvens (qualidade dos dados) (peso 15%)

Classificação:
- 0–33 → ALTO risco (vermelho)
- 34–66 → MÉDIO risco (amarelo)
- 67–100 → BAIXO risco (verde)

---

## Tratamento de Erros

```python
# Padrão em todo o código
try:
    df = pd.read_csv(filepath)
except FileNotFoundError:
    logger.error(f"Arquivo não encontrado: {filepath}")
    raise SystemExit(1)
except pd.errors.EmptyDataError:
    logger.warning("Arquivo CSV vazio — usando dados de exemplo")
    df = generate_sample_data()
```

Todos os erros vão para `logs/agrosat.log` com timestamp + nível + mensagem.

---

## Interface Terminal

Usa `rich` para:
- Tabelas de propriedades com cores por risco (verde/amarelo/vermelho)
- Progress bar durante carregamento e processamento em lote
- Panel com resultado de análise individual
- Cabeçalho com banner ASCII do AgroSat

Fallback: se `rich` não instalado, usa `print()` puro (graceful degradation).

---

## requirements.txt

```
pandas>=2.0.0
numpy>=1.24.0
rich>=13.0.0
```

Sem dependências pesadas. Roda sem GPU, sem GEE, sem API keys.

---

## Critérios de Avaliação → Cobertura

| Critério | Como atende | Arquivo |
|---|---|---|
| Pilha implementada | Stack com push/pop/peek, histórico de análises | `src/structures/stack.py` |
| Fila implementada | Queue com enqueue/dequeue, fila de lote | `src/structures/queue.py` |
| Lista ligada | DoublyLinkedList de observações por talhão | `src/structures/linked_list.py` |
| Busca | Binary search (por ID) + linear search (por município) | `src/algorithms/search.py` |
| Ordenação | Quick sort (risco/NDVI) + merge sort (obs por data) | `src/algorithms/sort.py` |
| Manipulação de arquivo | Leitura CSV, log em arquivo, exportação JSON | `loader.py`, `logger.py` |
| Modularização | 7 pacotes src com responsabilidades claras | `src/` |
| Try/except | Em todos I/O e operações de risco | disseminado |
| Logs | `logging` Python → arquivo + console | `src/utils/logger.py` |
| Interface terminal | Menu Rich com tabelas e cores | `src/ui/terminal.py` |
| Dados reais | CSV gerado de distribuições NDVI reais do Sentinel-2 | `data/` |
| Tema espaço | Sentinel-2, NDVI, economia espacial, crédito rural | contexto |

---

## Plano de Execução

### Fase A — Estruturas e Algoritmos (implementar primeiro, independente de dados)
1. `src/models/property.py` — dataclasses
2. `src/structures/linked_list.py` — DoublyLinkedList
3. `src/structures/stack.py` — Stack
4. `src/structures/queue.py` — Queue
5. `src/algorithms/search.py` — linear + binary
6. `src/algorithms/sort.py` — quick + merge

### Fase B — Dados e Análise
7. `data/generate_dataset.py` — gera CSVs realistas
8. `src/data/loader.py` — leitura, limpeza, construção das LinkedLists
9. `src/analysis/risk.py` — scoring de risco
10. `src/utils/logger.py` — setup_logger

### Fase C — Interface e Integração
11. `src/ui/terminal.py` — menu Rich
12. `main.py` — loop principal, conecta tudo
13. `requirements.txt` — dependências mínimas

### Fase D — Validação
14. Testar todos os caminhos do menu
15. Testar busca, ordenação, fila, pilha com dados reais
16. Verificar logs gerados
17. Testar com arquivo CSV ausente (tratamento de erro)

---

*Criado: 2026-06-06 | Disciplina: Estruturas de Dados | AgroSat GS 2026*
