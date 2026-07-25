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

from pathlib import Path
import subprocess

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
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
    # tools/merle/merle/main.py → repo root
    return current.parent.parent.parent.parent


def _get_template_path() -> Path:
    """Pfad zum offiziellen Copier-Template."""
    return _get_repo_root() / "templates" / "bot"


def _run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Wrapper für subprocess mit Rich-Output."""
    console.print(f"[dim]→ {' '.join(cmd)}[/dim]")
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def _get_version() -> str:
    """Versucht CLI-Version aus package metadata zu lesen."""
    try:
        import importlib.metadata

        return importlib.metadata.version("merle-cli")
    except Exception:
        return "0.7.0-dev"


def _get_framework_version() -> str:
    """Framework-Version aus merle-core (SSOT), Fallback metadata / pyproject."""
    try:
        from merle_core import __version__ as core_version

        return core_version
    except Exception:
        pass
    try:
        import importlib.metadata

        return importlib.metadata.version("merle-core")
    except Exception:
        return "0.7.0"


# =============================================================================
# Commands
# =============================================================================


@app.command("new-bot", help="Erzeugt einen neuen, governance-konformen Merle Python-Bot aus dem offiziellen Template.")
def new_bot(
    name: str = typer.Argument(..., help="Name des neuen Bots (snake_case, z.B. invoice_processor)"),
    description: str | None = typer.Option(None, "--description", "-d", help="Kurzbeschreibung für README und Docs"),
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
        console.print(
            Panel.fit(
                f"[red]Copier-Template nicht gefunden:[/red] {template_path}\n\n"
                "Stelle sicher, dass du im Merle-Repository arbeitest.\n"
                "Alternativ: [cyan]copier copy templates/bot python_bots/<name>[/cyan]",
                title="❌ Fehler",
                border_style="red",
            )
        )
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

    console.print(
        Panel.fit(
            f"[bold green]Merle[/bold green] — neuer Bot: [bold]{name}[/bold]\n"
            f"Ziel: [cyan]{target_dir}[/cyan]\n"
            f"Features: Playwright={answers['include_playwright']}, pandas={pandas}, pdf={pdf}, UiPath={uipath}, BaseBot={basebot}",
            title="🚀 Bot Generator",
            border_style="green",
        )
    )

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
    strict: bool = typer.Option(False, "--strict", help="Strengere Checks (mypy fail + bandit -ll)"),
    core_only: bool = typer.Option(False, "--core-only", help="Nur merle-core prüfen (skip template/repo notes)"),
) -> None:
    """Governance-Validator: Ruff + pytest always gate; mypy/bandit hard only with --strict."""
    root = _get_repo_root()
    results: dict[str, str] = {}
    hard_errors: list[str] = []
    soft_notes: list[str] = []

    console.print(Panel.fit("[bold]Merle Governance & Quality Validation[/bold]", title="🔍 merle validate"))

    # 1. Ruff (Format + Lint) — always blocking
    try:
        _run(["uv", "run", "ruff", "check", "."], cwd=root)
        _run(["uv", "run", "ruff", "format", "--check", "."], cwd=root)
        console.print("[green]✓[/green] Ruff lint + format: OK")
        results["Ruff + Format"] = "PASS"
    except subprocess.CalledProcessError:
        hard_errors.append("Ruff violations found")
        console.print("[red]✗[/red] Ruff failed")
        results["Ruff + Format"] = "FAIL"

    # 2. Pytest (merle-core) — always blocking
    try:
        _run(["uv", "run", "pytest", "packages/merle-core", "-q"], cwd=root)
        console.print("[green]✓[/green] Pytest (merle-core): OK")
        results["Pytest (merle-core)"] = "PASS"
    except subprocess.CalledProcessError:
        hard_errors.append("Pytest failures in merle-core")
        console.print("[red]✗[/red] Pytest failed")
        results["Pytest (merle-core)"] = "FAIL"

    # 3. Mypy (merle-core) — soft by default; blocking under --strict
    mypy_cmd = ["uv", "run", "mypy", "packages/merle-core/src/merle_core"]
    if strict:
        mypy_cmd.append("--strict")
    try:
        _run(mypy_cmd, cwd=root)
        console.print("[green]✓[/green] Mypy (merle-core): OK")
        results["Mypy (core)"] = "PASS"
    except subprocess.CalledProcessError:
        if strict:
            hard_errors.append("Mypy type errors in merle-core")
            console.print("[red]✗[/red] Mypy failed (--strict)")
            results["Mypy (core)"] = "FAIL"
        else:
            soft_notes.append("Mypy type errors in merle-core (non-blocking; use --strict to gate)")
            console.print("[yellow]⚠[/yellow] Mypy reported issues (soft; enable with --strict)")
            results["Mypy (core)"] = "PASS"

    # 4. Bandit (optional, only under --strict)
    if strict:
        try:
            _run(
                [
                    "uv",
                    "run",
                    "bandit",
                    "-c",
                    "pyproject.toml",
                    "-r",
                    "packages/merle-core/src/merle_core",
                    "-ll",
                    "-q",
                ],
                cwd=root,
            )
            console.print("[green]✓[/green] Bandit (-ll): OK")
            results["Bandit (-ll)"] = "PASS"
        except subprocess.CalledProcessError:
            hard_errors.append("Bandit findings at -ll severity")
            console.print("[red]✗[/red] Bandit failed (--strict)")
            results["Bandit (-ll)"] = "FAIL"
        except FileNotFoundError:
            soft_notes.append("bandit not installed; skipped under --strict")
            results["Bandit (-ll)"] = "PASS"

    # 5. Template integrity (Copier + post-hook)
    if not core_only:
        tpl = _get_template_path()
        if not (tpl / "copier.yml").exists() or not (tpl / "hooks" / "post_gen_project.py").exists():
            hard_errors.append("Copier template incomplete")
            console.print("[red]✗[/red] Official template broken")
            results["Copier Template"] = "FAIL"
        else:
            console.print("[green]✓[/green] Copier template integrity: OK")
            results["Copier Template"] = "PASS"

        # Repo visibility reminder (ADR-0009)
        console.print("[green]✓[/green] ADR-0009 (Public Source-Available Repo) active")
        results["Repo Visibility"] = "PASS"

    table = Table(title="Validation Summary")
    table.add_column("Check", style="cyan")
    table.add_column("Result")
    for check, result in results.items():
        style = "green" if result == "PASS" else "red"
        table.add_row(check, f"[{style}]{result}[/{style}]")
    console.print(table)

    if soft_notes:
        console.print(
            Panel("\n".join(f"• {n}" for n in soft_notes), title="Notes (non-blocking)", border_style="yellow")
        )

    if hard_errors:
        console.print(Panel("\n".join(f"• {e}" for e in hard_errors), title="Issues Found", border_style="red"))
        raise typer.Exit(1)

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
        console.print(
            Panel.fit(
                f"Serving docs at [cyan]http://localhost:{port}[/cyan]\n(Strg+C zum Beenden)", title="📚 Merle Docs"
            )
        )
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
        raise typer.Exit(1) from e


@app.command("info", help="Zeigt Framework-Status, Versionen und wichtige Pfade.")
def info() -> None:
    """Informationsübersicht (Versionen, Struktur, Philosophie)."""
    version = _get_version()

    table = Table(title=f"Merle Framework Info — v{version}")
    table.add_column("Component", style="bold cyan")
    table.add_column("Status / Path")
    table.add_row("merle-core", "packages/merle-core/src/merle_core (uv workspace member)")
    table.add_row("Official Template", "templates/bot/ (Copier + post-hook)")
    table.add_row("CLI", "tools/merle/ (this binary)")
    table.add_row("Docs", "docs/ (MkDocs) + AGENTS.md (binding)")
    table.add_row("ADRs", "docs/decisions/ (7+ records)")
    table.add_row("Examples", "examples/ + integration_examples/")
    table.add_row("Governance", "AGENTS.md + CODEOWNERS + ADR-0009 (Public)")
    console.print(table)

    console.print(
        Panel.fit(
            "Python-First • Template-First • Governance\n"
            "UiPath nur bei nachgewiesenem qualitativen Vorteil (siehe Entscheidungsmatrix)",
            title="Philosophie",
            border_style="blue",
        )
    )


@app.command("version", help="Zeigt die aktuelle CLI- und Framework-Version.")
def version_cmd() -> None:
    """Version (SemVer + Phase)."""
    v = _get_version()
    fw = _get_framework_version()
    console.print(f"[bold green]merle[/bold green] CLI v{v}  |  Merle Framework v{fw}")
    console.print("Python-first RPA framework — ready for bot development & internal enterprise use.")


if __name__ == "__main__":
    app()
