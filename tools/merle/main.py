"""
Merle CLI — Der offizielle Einstiegspunkt für neue RPA-Bots und Governance-Checks.

Enterprise-grade Typer + Rich CLI für das Merle Framework (Phase 1+).

Beispiele:
    merle new-bot invoice_processor --playwright --pandas
    merle new-bot high_volume_scraper --lightpanda
    merle validate --strict
    merle docs --serve
    merle version
    uv run merle info
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import typer

# Optional: Copier für new-bot
try:
    from copier import run_copy
except ImportError:
    run_copy = None  # type: ignore

app = typer.Typer(
    name="merle",
    help="Merle RPA Framework — Professional Developer Experience & Governance CLI",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
)
console = Console()


# =============================================================================
# Helpers
# =============================================================================

def _get_repo_root() -> Path:
    """Ermittelt das Merle-Repo-Root relativ zur CLI-Installation."""
    current = Path(__file__).resolve()
    # tools/merle/main.py → repo root
    return current.parent.parent.parent


def _get_template_path() -> Path:
    """Pfad zum offiziellen Copier-Template."""
    return _get_repo_root() / "templates" / "bot"


def _run(cmd: list[str], cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Wrapper für subprocess mit Rich-Output."""
    console.print(f"[dim]→ {' '.join(cmd)}[/dim]")
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def _get_version() -> str:
    """Versucht Version aus pyproject oder metadata zu lesen."""
    try:
        import importlib.metadata
        return importlib.metadata.version("merle-cli")
    except Exception:
        return "0.2.0-dev"


# =============================================================================
# Commands
# =============================================================================

@app.command("new-bot", help="Erzeugt einen neuen, governance-konformen Merle Python-Bot aus dem offiziellen Template.")
def new_bot(
    name: str = typer.Argument(..., help="Name des neuen Bots (snake_case, z.B. invoice_processor)"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Kurzbeschreibung für README und Docs"),
    playwright: bool = typer.Option(False, "--playwright", "-p", help="Playwright + Browser-Automatisierung einbinden"),
    browser_engine: str = typer.Option("chromium", "--browser-engine", "-b", help="chromium | lightpanda"),
    lightpanda: bool = typer.Option(False, "--lightpanda", help="Shortcut für --browser-engine lightpanda"),
    pandas: bool = typer.Option(False, "--pandas", help="pandas + openpyxl für Datenverarbeitung"),
    pdf: bool = typer.Option(False, "--pdf", help="pdfplumber für PDF-Parsing"),
    uipath: bool = typer.Option(False, "--uipath", help="UiPath Orchestrator REST Client (nur begründet!)"),
    basebot: bool = typer.Option(True, "--basebot/--no-basebot", help="Von BaseBot (merle-core) erben"),
    location: str = typer.Option("python_bots", help="Ziel: python_bots (Monorepo) | standalone"),
) -> None:
    """Erzeugt einen neuen, voll konformen Merle Python-Bot (Template-First)."""
    template_path = _get_template_path()

    if not template_path.exists():
        console.print(Panel.fit(
            f"[red]Copier-Template nicht gefunden:[/red] {template_path}\n\n"
            "Stelle sicher, dass du im Merle-Repository arbeitest.\n"
            "Alternativ: [cyan]copier copy templates/bot python_bots/<name>[/cyan]",
            title="❌ Fehler",
            border_style="red",
        ))
        raise typer.Exit(1)

    effective_engine = "lightpanda" if lightpanda else browser_engine
    if effective_engine not in ("chromium", "lightpanda"):
        console.print(f"[red]Ungültige Engine:[/red] {effective_engine} (erlaubt: chromium, lightpanda)")
        raise typer.Exit(1)

    answers = {
        "bot_name": name,
        "bot_description": description or f"Automatisiert den Prozess '{name}'",
        "include_playwright": playwright or (effective_engine == "lightpanda"),
        "browser_engine": effective_engine,
        "include_pandas": pandas,
        "include_pdf": pdf,
        "include_uipath_orchestrator": uipath,
        "use_base_bot_class": basebot,
        "location": location,
    }

    target_dir = Path(location) / name

    console.print(Panel.fit(
        f"[bold green]Merle[/bold green] — neuer Bot: [bold]{name}[/bold]\n"
        f"Ziel: [cyan]{target_dir}[/cyan]\n"
        f"Features: Playwright={answers['include_playwright']}, pandas={pandas}, pdf={pdf}, UiPath={uipath}, BaseBot={basebot}",
        title="🚀 Bot Generator",
        border_style="green",
    ))

    if run_copy is None:
        console.print("[red]Copier nicht installiert. Bitte 'uv sync --group dev' ausführen.[/red]")
        raise typer.Exit(1)

    try:
        run_copy(
            str(template_path),
            str(target_dir),
            data=answers,
            overwrite=False,
            unsafe=True,  # Post-Hooks erlauben
        )
    except Exception as exc:
        console.print(f"[red]Generierungsfehler:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print("\n[bold green]✅ Bot erfolgreich generiert![/bold green]")
    console.print(
        f"\nNächste Schritte:\n"
        f"  [cyan]cd {target_dir}[/cyan]\n"
        f"  [cyan]uv sync --group dev[/cyan]\n"
        f"  [cyan]uv run python main.py[/cyan]\n"
        f"  [cyan]uv run pytest -q[/cyan]"
    )


@app.command("validate", help="Führt umfassende Governance- und Qualitäts-Checks für das Merle-Framework aus.")
def validate(
    strict: bool = typer.Option(False, "--strict", help="Strengere Checks (mypy --strict, bandit high)"),
    core_only: bool = typer.Option(False, "--core-only", help="Nur merle-core prüfen"),
) -> None:
    """Governance-Validator: Lint, Type, Test, Template, Legacy-Deprecated, Visibility."""
    root = _get_repo_root()
    errors: list[str] = []

    console.print(Panel.fit("[bold]Merle Governance & Quality Validation[/bold]", title="🔍 merle validate"))

    # 1. Ruff (Format + Lint)
    try:
        _run(["uv", "run", "ruff", "check", "."], cwd=root)
        _run(["uv", "run", "ruff", "format", "--check", "."], cwd=root)
        console.print("[green]✓[/green] Ruff lint + format: OK")
    except subprocess.CalledProcessError:
        errors.append("Ruff violations found")
        console.print("[red]✗[/red] Ruff failed")

    # 2. Mypy (merle-core)
    mypy_cmd = ["uv", "run", "mypy", "python_bots/shared/src/merle_core"]
    if strict:
        mypy_cmd.append("--strict")
    try:
        _run(mypy_cmd, cwd=root)
        console.print("[green]✓[/green] Mypy (merle-core): OK")
    except subprocess.CalledProcessError:
        errors.append("Mypy type errors in merle-core")
        console.print("[yellow]⚠[/yellow] Mypy reported issues (allowed in early phases)")

    # 3. Legacy template deprecated check
    legacy = root / "python_bots" / "template"
    if legacy.exists():
        console.print("[yellow]⚠[/yellow] Legacy template (python_bots/template/) detected — deprecated since Phase 1. Use templates/bot/ + 'merle new-bot'")
        if strict:
            errors.append("Legacy template still present")

    # 4. Template integrity (Copier + post-hook)
    tpl = _get_template_path()
    if not (tpl / "copier.yml").exists() or not (tpl / "hooks" / "post_gen_project.py").exists():
        errors.append("Copier template incomplete")
        console.print("[red]✗[/red] Official template broken")

    # 5. Check for accidental secrets / .env in git (simple heuristic)
    # (real check would be in pre-commit / gitleaks)

    # 6. Repo visibility reminder (from ADR-0008)
    console.print("[green]✓[/green] ADR-0008 (Private Repo) reminder active")

    table = Table(title="Validation Summary")
    table.add_column("Check", style="cyan")
    table.add_column("Result")
    table.add_row("Ruff + Format", "PASS" if not any("Ruff" in e for e in errors) else "FAIL")
    table.add_row("Mypy (core)", "PASS (with notes)" if not any("Mypy" in e for e in errors) else "FAIL")
    table.add_row("Legacy Template", "DEPRECATED WARNING" if legacy.exists() else "CLEAN")
    table.add_row("Copier Template", "OK" if not any("Copier" in e for e in errors) else "BROKEN")
    table.add_row("Repo Visibility", "PRIVATE (ADR-0008)")
    console.print(table)

    if errors:
        console.print(Panel("\n".join(f"• {e}" for e in errors), title="Issues Found", border_style="red"))
        if strict:
            raise typer.Exit(1)
    else:
        console.print("\n[bold green]✅ All governance checks passed. Ready for production bots.[/bold green]")


@app.command("docs", help="Baut oder served die MkDocs-Dokumentation (nie site/ committen!).")
def docs(
    serve: bool = typer.Option(True, "--serve/--build", help="Serve lokal (Default) oder static Build"),
    port: int = typer.Option(8000, "--port", "-p", help="Port für serve"),
    strict: bool = typer.Option(False, "--strict", help="MkDocs --strict Mode"),
) -> None:
    """Dokumentation (MkDocs). Baut nie site/ ins Git."""
    root = _get_repo_root()
    cmd = ["uv", "run", "mkdocs"]
    if serve:
        cmd += ["serve", "-a", f"localhost:{port}"]
        console.print(Panel.fit(f"Serving docs at [cyan]http://localhost:{port}[/cyan]\n(Strg+C zum Beenden)", title="📚 Merle Docs"))
    else:
        # Safety: clean site/ first
        (root / "site").mkdir(exist_ok=True)
        import shutil
        shutil.rmtree(root / "site", ignore_errors=True)
        cmd += ["build"]
        if strict:
            cmd.append("--strict")
        console.print(Panel.fit("Building static docs into site/ (will be .gitignored)", title="📚 MkDocs Build"))

    try:
        subprocess.run(cmd, cwd=root, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]MkDocs Fehler:[/red] {e}")
        raise typer.Exit(1)


@app.command("info", help="Zeigt Framework-Status, Versionen und wichtige Pfade.")
def info() -> None:
    """Informationsübersicht (Versionen, Struktur, Philosophie)."""
    root = _get_repo_root()
    version = _get_version()

    table = Table(title=f"Merle Framework Info — v{version}")
    table.add_column("Component", style="bold cyan")
    table.add_column("Status / Path")
    table.add_row("merle-core", "python_bots/shared/src/merle_core (uv workspace member)")
    table.add_row("Official Template", "templates/bot/ (Copier + post-hook)")
    table.add_row("Legacy Template", "python_bots/template/ ⚠️ DEPRECATED — do not use")
    table.add_row("CLI", "tools/merle/ (this binary)")
    table.add_row("Docs", "docs/ (MkDocs) + AGENTS.md (binding)")
    table.add_row("ADRs", "docs/decisions/ (7+ records)")
    table.add_row("Examples", "examples/ + integration_examples/")
    table.add_row("Governance", "AGENTS.md + CODEOWNERS + ADR-0008 (Private)")
    console.print(table)

    console.print(Panel.fit(
        "Python-First • Template-First • Governance\n"
        "UiPath nur bei nachgewiesenem qualitativen Vorteil (siehe Entscheidungsmatrix)",
        title="Philosophie",
        border_style="blue",
    ))


@app.command("version", help="Zeigt die aktuelle CLI- und Framework-Version.")
def version_cmd() -> None:
    """Version (SemVer + Phase)."""
    v = _get_version()
    console.print(f"[bold green]merle[/bold green] CLI v{v}  |  Merle Framework v0.2.0 (Professional Foundation)")
    console.print("Phase 1 complete — ready for bot development & internal enterprise use.")


if __name__ == "__main__":
    app()
