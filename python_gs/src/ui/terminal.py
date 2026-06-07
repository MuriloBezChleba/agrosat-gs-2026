"""
Interface terminal do AgroSat CLI.
Usa Rich para tabelas, painéis e cores. Fallback para print() se Rich ausente.
"""

from __future__ import annotations
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    _RICH = True
    console = Console()
except ImportError:
    _RICH = False
    console = None  # type: ignore

from src.models.property import AnalysisResult, Property
from src.structures.stack import Stack
from src.structures.queue import Queue


# ── Cores por classe de risco ────────────────────────────────────────────────

_RISK_COLOR = {
    "BAIXO": "green",
    "MÉDIO": "yellow",
    "ALTO":  "red",
}

_RISK_EMOJI = {
    "BAIXO": "[green]*[/green]",
    "MÉDIO": "[yellow]*[/yellow]",
    "ALTO":  "[red]*[/red]",
}


# ── Cabeçalho ────────────────────────────────────────────────────────────────

def print_header() -> None:
    banner = (
        "   ___   ___  ____  ____  _____   __  ____\n"
        "  / _ | / _ |/ __ \\/ __ \\/ __/ | / / / _/\n"
        " / __ |/ __, / /_/ / /_/ /\\ \\ | |/ /_\\ \\ \n"
        "/_/ |_/_/ |_/\\____/\\____/___/ |___//___/ \n"
        "  Inteligencia Agricola por Satelite  |  Sentinel-2 / INMET"
    )
    if _RICH:
        console.print(Panel(banner, style="bold cyan", expand=False))
    else:
        print("=" * 60)
        print("  AGROSAT — Inteligência Agrícola por Satélite")
        print("=" * 60)


# ── Menu principal ───────────────────────────────────────────────────────────

def print_menu(queue: Queue, stack: Stack) -> None:
    menu = (
        "\n[bold cyan]MENU PRINCIPAL[/bold cyan]\n"
        f"  [1] Listar propriedades        [dim](total carregado)[/dim]\n"
        f"  [2] Buscar por ID              [dim](busca binária)[/dim]\n"
        f"  [3] Buscar por município       [dim](busca linear)[/dim]\n"
        f"  [4] Ordenar por NDVI           [dim](quick sort)[/dim]\n"
        f"  [5] Ordenar por risco          [dim](quick sort)[/dim]\n"
        f"  [6] Analisar risco             [dim](análise individual)[/dim]\n"
        f"  [7] Enfileirar para lote       [dim](fila: {queue.size()} aguardando)[/dim]\n"
        f"  [8] Processar fila             [dim](processa todos da fila)[/dim]\n"
        f"  [9] Ver histórico              [dim](pilha: {stack.size()} análises)[/dim]\n"
        f"  [E] Exportar resultados        [dim](JSON)[/dim]\n"
        f"  [0] Sair\n"
    )
    if _RICH:
        console.print(Panel(menu, title="AgroSat CLI", border_style="cyan"))
    else:
        print(menu.replace("[bold cyan]", "").replace("[/bold cyan]", "")
              .replace("[dim]", "").replace("[/dim]", "")
              .replace("[green]", "").replace("[/green]", "")
              .replace("[yellow]", "").replace("[/yellow]", "")
              .replace("[red]", "").replace("[/red]", ""))


# ── Tabelas ──────────────────────────────────────────────────────────────────

def print_properties_table(
    properties: list[Property],
    results: dict[str, AnalysisResult],
    title: str = "Propriedades Rurais",
    limit: int = 30,
) -> None:
    subset = properties[:limit]

    if _RICH:
        table = Table(title=title, box=box.ROUNDED, show_lines=False)
        table.add_column("ID",          style="cyan",   no_wrap=True)
        table.add_column("Município",   style="white")
        table.add_column("UF",          justify="center")
        table.add_column("Cultura",     style="green")
        table.add_column("Área (ha)",   justify="right")
        table.add_column("Obs.",        justify="center")
        table.add_column("NDVI médio",  justify="right")
        table.add_column("Risco",       justify="center")

        for p in subset:
            obs_list = p.observations.to_list()
            ndvi_avg = (
                f"{sum(o.ndvi_mean for o in obs_list) / len(obs_list):.3f}"
                if obs_list else "—"
            )
            r = results.get(p.property_id)
            if r:
                color = _RISK_COLOR.get(r.risk_class, "white")
                risco_cell = f"[{color}]{r.risk_class} ({r.risk_score:.0f})[/{color}]"
            else:
                risco_cell = "[dim]—[/dim]"

            table.add_row(
                p.property_id, p.municipality, p.state, p.culture,
                f"{p.area_ha:,.0f}", str(len(obs_list)), ndvi_avg, risco_cell,
            )

        if len(properties) > limit:
            table.caption = f"Mostrando {limit} de {len(properties)} propriedades"
        console.print(table)
    else:
        print(f"\n{'ID':<10} {'Município':<28} {'UF':3} {'Cultura':<12} {'Área':>8} {'Obs':>4} {'NDVI':>7} {'Risco'}")
        print("-" * 90)
        for p in subset:
            obs_list = p.observations.to_list()
            ndvi_avg = (
                f"{sum(o.ndvi_mean for o in obs_list) / len(obs_list):.3f}"
                if obs_list else "—"
            )
            r = results.get(p.property_id)
            risco = f"{r.risk_class} ({r.risk_score:.0f})" if r else "—"
            print(f"{p.property_id:<10} {p.municipality:<28} {p.state:3} {p.culture:<12} {p.area_ha:>8,.0f} {len(obs_list):>4} {ndvi_avg:>7} {risco}")


def print_analysis_result(result: AnalysisResult) -> None:
    color = _RISK_COLOR.get(result.risk_class, "white")
    content = (
        f"  Propriedade : [cyan]{result.property_id}[/cyan]\n"
        f"  Município   : {result.municipality}\n"
        f"  Data análise: {result.analysis_date.strftime('%d/%m/%Y %H:%M')}\n"
        f"  NDVI médio  : {result.ndvi_mean:.3f}\n"
        f"  Tendência   : {result.ndvi_trend}\n"
        f"  Score risco : [{color}]{result.risk_score:.1f}/100[/{color}]\n"
        f"  Classe risco: [{color}]{result.risk_class}[/{color}]\n"
        f"  Recomendação: [italic]{result.recommendation}[/italic]"
    )
    if _RICH:
        console.print(Panel(content, title=f"[bold]Análise de Risco — {result.property_id}[/bold]",
                            border_style=color))
    else:
        print(f"\n=== Análise de Risco: {result.property_id} ===")
        print(content.replace("[cyan]", "").replace("[/cyan]", "")
              .replace("[green]", "").replace("[/green]", "")
              .replace("[yellow]", "").replace("[/yellow]", "")
              .replace("[red]", "").replace("[/red]", "")
              .replace("[italic]", "").replace("[/italic]", "")
              .replace("[bold]", "").replace("[/bold]", "")
              .replace("[dim]", "").replace("[/dim]", ""))


def print_history(stack: Stack) -> None:
    items = stack.to_list()
    if not items:
        _print("Histórico vazio.")
        return
    _print(f"\nHistórico de análises ({len(items)} entradas, mais recente por último):\n")
    for i, r in enumerate(items, 1):
        color = _RISK_COLOR.get(r.risk_class, "white")
        line = f"  {i:>2}. {r.property_id:<10} [{color}]{r.risk_class:<6}[/{color}] score={r.risk_score:.0f}  {r.analysis_date.strftime('%d/%m %H:%M')}"
        if _RICH:
            console.print(line)
        else:
            print(line.replace("[green]", "").replace("[/green]", "")
                  .replace("[yellow]", "").replace("[/yellow]", "")
                  .replace("[red]", "").replace("[/red]", ""))


def print_queue_status(queue: Queue) -> None:
    items = queue.to_list()
    if not items:
        _print("Fila vazia.")
        return
    ids = ", ".join(items)
    _print(f"Fila ({queue.size()} itens): {ids}")


def _print(msg: str) -> None:
    if _RICH:
        console.print(msg)
    else:
        print(msg)


def prompt(text: str) -> str:
    if _RICH:
        return console.input(f"[bold yellow]{text}[/bold yellow] ").strip()
    return input(text).strip()


def info(msg: str) -> None:
    if _RICH:
        console.print(f"[green][OK][/green] {msg}")
    else:
        print(f"[OK] {msg}")


def warn(msg: str) -> None:
    if _RICH:
        console.print(f"[yellow][!][/yellow]  {msg}")
    else:
        print(f"[AVISO] {msg}")


def error(msg: str) -> None:
    if _RICH:
        console.print(f"[red][x][/red]  {msg}")
    else:
        print(f"[ERRO] {msg}")
