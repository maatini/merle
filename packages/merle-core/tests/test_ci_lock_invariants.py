"""CI lock invariants: Quality `uv lock --check` and Trivy-fixed cryptography.

These tests drive the same Quality command as `.github/workflows/ci.yml`
and parse the shipped invoice-processing lock — they do not reimplement
the resolver.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import tomllib

from packaging.version import Version

_TRIVY_FIXED_CRYPTOGRAPHY = Version("50.0.0")


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "pyproject.toml").is_file() and (parent / "examples" / "invoice-processing" / "uv.lock").is_file():
            return parent
    raise AssertionError("could not locate merle workspace root from test file")


def _locked_package_version(lock_path: Path, name: str) -> Version:
    data = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    for package in data.get("package", []):
        if package.get("name") == name:
            return Version(str(package["version"]))
    raise AssertionError(f"{name!r} not found in {lock_path}")


def test_uv_lock_check_matches_quality_job() -> None:
    """Same HARD Quality step: `uv lock --check` at the repo root must exit 0."""
    result = subprocess.run(
        ["uv", "lock", "--check"],
        cwd=_repo_root(),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"uv lock --check failed (Quality job first HARD step):\n{result.stdout}{result.stderr}"
    )


def test_invoice_processing_lock_pins_trivy_fixed_cryptography() -> None:
    """Trivy CVE-2026-69247 is fixed in cryptography 50.0.0; 49.x must not remain locked."""
    lock_path = _repo_root() / "examples" / "invoice-processing" / "uv.lock"
    version = _locked_package_version(lock_path, "cryptography")
    assert version >= _TRIVY_FIXED_CRYPTOGRAPHY, (
        f"{lock_path} pins cryptography {version}, need >= {_TRIVY_FIXED_CRYPTOGRAPHY} (CVE-2026-69247)"
    )


def test_ci_workflow_keeps_quality_and_security_hard_gates() -> None:
    """Quality + Security steps stay HARD — same commands as .github/workflows/ci.yml."""
    workflow = (_repo_root() / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    required = (
        "uv lock --check",
        "uv run ruff check .",
        "uv run mypy packages/merle-core/src/merle_core --strict",
        "uv run pytest packages/merle-core",
        "uv run merle validate --strict",
        "uv run bandit",
        'severity: "CRITICAL,HIGH"',
        'exit-code: "1"',
        "trufflesecurity/trufflehog@",
    )
    missing = [item for item in required if item not in workflow]
    assert not missing, f"CI workflow missing HARD gates: {missing}"
