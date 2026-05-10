"""
Beispiel: Dateibasierte Integration zwischen Python und UiPath.

Dieses Muster wird verwendet, wenn Python-Bots und UiPath-Roboter
über geteilte Dateien oder Message Queues kommunizieren.

Vorteile:
- Einfach, keine API-Entwicklung nötig
- Entkoppelt: Beide Seiten können unabhängig laufen
- Gut für Batch-Verarbeitung

Nachteile:
- Keine Echtzeit-Kommunikation
- Dateizugriff muss koordiniert werden (Locking)
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from loguru import logger


class FileBasedIntegration:
    """Liest und schreibt Integrationsdateien für UiPath <-> Python Austausch."""

    def __init__(self, shared_path: Path):
        self.shared_path = Path(shared_path)
        self.shared_path.mkdir(parents=True, exist_ok=True)
        self.logger = logger.bind(component="FileBasedIntegration")

    def write_for_uipath(self, data: list[dict], filename: str = None) -> Path:
        """
        Schreibt Daten als JSON-Datei für UiPath.

        UiPath kann JSON über die Deserialize-JSON-Activity einlesen.
        """
        if filename is None:
            filename = f"python_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        output_path = self.shared_path / "for_uipath" / filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

        self.logger.info("Daten für UiPath geschrieben: {} ({} Einträge)", output_path, len(data))
        return output_path

    def read_from_uipath(self, pattern: str = "*.csv") -> list[dict]:
        """
        Liest CSV-Dateien, die von UiPath geschrieben wurden.

        UiPath kann CSV über die Write-CSV-Activity schreiben.
        """
        input_dir = self.shared_path / "from_uipath"
        results = []

        for csv_file in input_dir.glob(pattern):
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                results.extend(rows)
            self.logger.info("CSV von UiPath gelesen: {} ({} Zeilen)", csv_file.name, len(rows))

        return results

    def archive_processed(self, file_path: Path) -> Path:
        """Verschiebe verarbeitete Datei ins Archiv."""
        archive_dir = self.shared_path / "archive"
        archive_dir.mkdir(exist_ok=True)
        target = archive_dir / file_path.name
        file_path.rename(target)
        self.logger.info("Datei archiviert: {} -> {}", file_path, target)
        return target


# Beispiel-Nutzung
if __name__ == "__main__":
    integration = FileBasedIntegration(Path("./shared_data"))

    # Daten für UiPath schreiben
    data = [
        {"invoice_id": "INV-001", "amount": 1500.00, "status": "pending"},
        {"invoice_id": "INV-002", "amount": 2300.50, "status": "pending"},
    ]
    integration.write_for_uipath(data)

    # Von UiPath geschriebene Daten lesen
    # uipath_data = integration.read_from_uipath()
