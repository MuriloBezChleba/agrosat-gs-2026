"""
AgroSat CLI — Inteligência Agrícola por Satélite
Disciplina: Estruturas de Dados | FIAP | Global Solution 2026

Estruturas implementadas:
  - DoublyLinkedList  → observações NDVI por talhão (src/structures/linked_list.py)
  - Stack             → histórico de análises de risco (src/structures/stack.py)
  - Queue             → fila de processamento em lote (src/structures/queue.py)

Algoritmos implementados:
  - Busca binária     → busca por property_id (src/algorithms/search.py)
  - Busca linear      → busca por município   (src/algorithms/search.py)
  - Quick sort        → ordena por NDVI/risco  (src/algorithms/sort.py)
  - Merge sort        → ordena obs por data    (src/algorithms/sort.py)
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from src.utils.logger import setup_logger
from src.data.loader import load_properties, load_climate
from src.analysis.risk import calculate_risk
from src.structures.stack import Stack
from src.structures.queue import Queue
from src.algorithms.search import linear_search, binary_search
from src.algorithms.sort import quick_sort
from src.models.property import Property, AnalysisResult
import src.ui.terminal as ui

logger = setup_logger()


def main() -> None:
    ui.print_header()

    # ── Carregamento de dados ────────────────────────────────────────────────
    try:
        properties = load_properties()
        climate = load_climate()
        ui.info(f"{len(properties)} propriedades carregadas | {len(climate)} registros climáticos")
    except FileNotFoundError:
        ui.error("Dados não encontrados. Execute: python data/generate_dataset.py")
        sys.exit(1)
    except Exception as e:
        ui.error(f"Falha ao carregar dados: {e}")
        logger.exception("Erro no carregamento")
        sys.exit(1)

    # Estado da sessão
    history: Stack = Stack(max_size=20)
    batch_queue: Queue = Queue()
    results: dict[str, AnalysisResult] = {}

    # Índice para busca binária (ordenado por property_id)
    sorted_by_id = sorted(properties, key=lambda p: p.property_id)

    while True:
        ui.print_menu(batch_queue, history)
        choice = ui.prompt("Opção:").upper()

        # ── [1] Listar propriedades ──────────────────────────────────────────
        if choice == "1":
            ui.print_properties_table(properties, results)

        # ── [2] Buscar por ID (busca binária) ────────────────────────────────
        elif choice == "2":
            pid = ui.prompt("ID da propriedade (ex: PR-0042):").upper()
            result = binary_search(sorted_by_id, pid, key=lambda p: p.property_id)
            if result:
                obs_list = result.observations.to_list()
                ui.info(f"Encontrado: {result}")
                ui.print_properties_table([result], results, title=f"Propriedade {pid}")
                ui.info(f"{len(obs_list)} observações satelitais")
            else:
                ui.warn(f"Propriedade '{pid}' não encontrada.")
            logger.info(f"Busca binária por '{pid}': {'encontrado' if result else 'não encontrado'}")

        # ── [3] Buscar por município (busca linear) ──────────────────────────
        elif choice == "3":
            mun = ui.prompt("Município (parcial, sem acento):").lower()
            found = linear_search(
                properties,
                predicate=lambda p: mun in p.municipality.lower()
            )
            if found:
                ui.info(f"{len(found)} propriedade(s) em municípios com '{mun}'")
                ui.print_properties_table(found, results, title=f"Busca: {mun}")
            else:
                ui.warn(f"Nenhuma propriedade em município com '{mun}'.")
            logger.info(f"Busca linear por município '{mun}': {len(found)} resultados")

        # ── [4] Ordenar por NDVI (quick sort) ───────────────────────────────
        elif choice == "4":
            direction = ui.prompt("Ordem? [C]rescente / [D]ecrescente:").upper()
            obs_avg = lambda p: (
                sum(o.ndvi_mean for o in p.observations) / p.observations.size()
                if not p.observations.is_empty() else 0.0
            )
            quick_sort(properties, key=obs_avg)
            if direction == "D":
                properties.reverse()
            ui.info(f"Ordenado por NDVI {'[ASC]' if direction != 'D' else '[DESC]'}")
            ui.print_properties_table(properties, results, title="Ordenado por NDVI médio")
            logger.info(f"Quick sort por NDVI ({direction})")

        # ── [5] Ordenar por risco (quick sort) ──────────────────────────────
        elif choice == "5":
            if not results:
                ui.warn("Nenhuma análise realizada ainda. Use opção [6] primeiro.")
                continue
            direction = ui.prompt("Ordem? [C]rescente / [D]ecrescente:").upper()
            risk_key = lambda p: results[p.property_id].risk_score if p.property_id in results else -1
            analyzed = [p for p in properties if p.property_id in results]
            quick_sort(analyzed, key=risk_key)
            if direction == "D":
                analyzed.reverse()
            ui.info(f"Ordenado por score de risco {'[ASC]' if direction != 'D' else '[DESC]'}")
            ui.print_properties_table(analyzed, results, title="Ordenado por Risco")
            logger.info(f"Quick sort por risco ({direction})")

        # ── [6] Analisar risco individual ────────────────────────────────────
        elif choice == "6":
            pid = ui.prompt("ID da propriedade:").upper()
            prop = binary_search(sorted_by_id, pid, key=lambda p: p.property_id)
            if not prop:
                ui.warn(f"Propriedade '{pid}' não encontrada.")
                continue
            try:
                result = calculate_risk(prop, climate)
                results[pid] = result
                history.push(result)
                ui.print_analysis_result(result)
            except Exception as e:
                ui.error(f"Erro na análise: {e}")
                logger.exception(f"Erro calculando risco para {pid}")

        # ── [7] Enfileirar para lote ─────────────────────────────────────────
        elif choice == "7":
            pids_input = ui.prompt("IDs separados por vírgula (ex: PR-0001,PR-0002):")
            for pid in pids_input.split(","):
                pid = pid.strip().upper()
                if not pid:
                    continue
                prop = binary_search(sorted_by_id, pid, key=lambda p: p.property_id)
                if prop:
                    batch_queue.enqueue(pid)
                    ui.info(f"{pid} enfileirado.")
                else:
                    ui.warn(f"'{pid}' não encontrado — ignorado.")
            ui.print_queue_status(batch_queue)

        # ── [8] Processar fila ───────────────────────────────────────────────
        elif choice == "8":
            if batch_queue.is_empty():
                ui.warn("Fila vazia.")
                continue
            total = batch_queue.size()
            ui.info(f"Processando {total} propriedades da fila...")
            processed = []
            errors = 0
            while not batch_queue.is_empty():
                pid = batch_queue.dequeue()
                prop = binary_search(sorted_by_id, pid, key=lambda p: p.property_id)
                if not prop:
                    ui.warn(f"{pid}: não encontrado na base.")
                    errors += 1
                    continue
                try:
                    result = calculate_risk(prop, climate)
                    results[pid] = result
                    history.push(result)
                    processed.append(result)
                except Exception as e:
                    ui.error(f"{pid}: erro — {e}")
                    errors += 1
                    logger.exception(f"Erro processando {pid} do lote")

            ui.info(f"Lote concluído: {len(processed)} analisadas, {errors} erros.")
            if processed:
                analyzed_props = [p for p in properties if p.property_id in results]
                ui.print_properties_table(
                    analyzed_props, results, title="Resultado do Lote"
                )

        # ── [9] Ver histórico (pilha) ────────────────────────────────────────
        elif choice == "9":
            ui.print_history(history)
            if not history.is_empty():
                sub = ui.prompt("Ver detalhe da última análise? [S/N]:").upper()
                if sub == "S":
                    ui.print_analysis_result(history.peek())

        # ── [E] Exportar ─────────────────────────────────────────────────────
        elif choice == "E":
            if not results:
                ui.warn("Nenhuma análise para exportar.")
                continue
            out_path = Path("logs") / f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                export_data = [
                    {
                        "property_id": r.property_id,
                        "municipality": r.municipality,
                        "analysis_date": r.analysis_date.isoformat(),
                        "risk_score": r.risk_score,
                        "risk_class": r.risk_class,
                        "ndvi_mean": r.ndvi_mean,
                        "ndvi_trend": r.ndvi_trend,
                        "recommendation": r.recommendation,
                    }
                    for r in results.values()
                ]
                out_path.parent.mkdir(exist_ok=True)
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                ui.info(f"Exportado: {out_path} ({len(export_data)} análises)")
            except Exception as e:
                ui.error(f"Falha ao exportar: {e}")
                logger.exception("Erro na exportação")

        # ── [0] Sair ─────────────────────────────────────────────────────────
        elif choice == "0":
            ui.info("Encerrando AgroSat CLI. Até logo!")
            logger.info("Sessão encerrada pelo usuário.")
            break

        else:
            ui.warn("Opção inválida. Use os números do menu.")


if __name__ == "__main__":
    main()
