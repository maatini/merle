"""
Merle CLI - Der offizielle Einstiegspunkt für neue RPA-Bots.

Beispiele:
    merle new-bot invoice_processor --playwright --description "..."
    merle new-bot high_volume_scraper --playwright --browser-engine lightpanda
    merle new-bot high_volume_scraper --lightpanda   # Shortcut
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
import typer

# Copier programmatisch aufrufen
try:
    from copier import run_copy
except ImportError:
    run_copy = None  # type: ignore

app = typer.Typer(
    name="merle",
    help="Merle RPA Framework - Developer Experience Tools",
    add_completion=False,
)
console = Console()


def _get_template_path() -> Path:
    """Ermittelt den Pfad zum Copier-Template relativ zur CLI."""
    # Annahme: tools/merle/ liegt im Root des Merle-Repos
    # In Produktion wird das Template über den installierten Pfad gefunden
    current = Path(__file__).resolve()
    # tools/merle/main.py → templates/bot
    return current.parent.parent.parent / "templates" / "bot"


@app.command()
def new_bot(
    name: str = typer.Argument(..., help="Name des neuen Bots (snake_case)"),
    description: str | None = typer.Option(None, "--description", "-d", help="Kurzbeschreibung"),
    playwright: bool = typer.Option(False, "--playwright", help="Playwright einbinden"),
    browser_engine: str = typer.Option(
        "chromium",
        "--browser-engine",
        help="Browser-Engine: chromium (Default) oder lightpanda",
        show_default=True,
    ),
    lightpanda: bool = typer.Option(False, "--lightpanda", help="Shortcut: --browser-engine lightpanda"),
    pandas: bool = typer.Option(False, "--pandas", help="pandas + openpyxl einbinden"),
    uipath: bool = typer.Option(False, "--uipath", help="UiPath Orchestrator Client"),
    use_basebot: bool = typer.Option(True, "--basebot/--no-basebot", help="BaseBot-Klasse verwenden"),
    location: str = typer.Option("python_bots", help="Zielverzeichnis (python_bots oder standalone)"),
) -> None:
    """Erzeugt einen neuen, voll konformen Merle Python-Bot."""

    template_path = _get_template_path()

    if not template_path.exists():
        console.print(
            "[red]Fehler:[/red] Copier-Template nicht gefunden unter "
            f"{template_path}\n"
            "Stelle sicher, dass du im Merle-Repository arbeitest oder das Template installiert ist."
        )
        raise typer.Exit(1)

    # Lightpanda-Shortcut verarbeiten
    effective_engine = "lightpanda" if lightpanda else browser_engine
    if effective_engine not in ("chromium", "lightpanda"):
        console.print(f"[red]Ungültige Browser-Engine:[/red] {effective_engine}. Erlaubt: chromium, lightpanda")
        raise typer.Exit(1)

    answers = {
        "bot_name": name,
        "bot_description": description or f"Automatisiert den Prozess '{name}'",
        "include_playwright": playwright or (effective_engine == "lightpanda"),
        "browser_engine": effective_engine,
        "include_pandas": pandas,
        "include_uipath_orchestrator": uipath,
        "use_base_bot_class": use_basebot,
        "location": location,
    }

    target_dir = Path(location) / name

    console.print(
        Panel.fit(
            f"[bold green]Merle[/bold green] erzeugt neuen Bot: [bold]{name}[/bold]\nZiel: [cyan]{target_dir}[/cyan]",
            title="🚀 Merle Bot Generator",
        )
    )

    try:
        run_copy(
            str(template_path),
            str(target_dir),
            data=answers,
            overwrite=False,
            unsafe=True,  # erlaubt Post-Hooks
        )
    except Exception as exc:
        console.print(f"[red]Fehler bei der Generierung:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print("\n[bold green]✅ Fertig![/bold green]")
    console.print(f"\nNächste Schritte:\n  cd {target_dir}\n  uv sync --group dev\n  uv run python main.py")


@app.command()
def version() -> None:
    """Zeigt die aktuelle Merle CLI Version."""
    console.print("merle CLI v0.1.0 (Phase 1 - Copier-basiert)")


if __name__ == "__main__":
    app()
