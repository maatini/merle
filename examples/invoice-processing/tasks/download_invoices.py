"""
Task: Fetch and download new invoice PDFs from an email inbox.

Demonstrates:
- IMAP email connection with SSL
- Extraction of PDF attachments using python's email library
- Local simulation mode reading raw email (.eml) files
- Robust error handling and logging
"""

from __future__ import annotations

import email
from email.message import Message
import imaplib
from pathlib import Path
from typing import Any

from merle_core import BaseTask
from merle_core.retry import default_http_retry, with_retry


class DownloadInvoicesTask(BaseTask):
    """
    Downloads invoice PDFs from an email inbox.

    Supports both simulated local execution and real IMAP integration.
    """

    def __init__(self, settings: Any, input_dir: Path) -> None:
        super().__init__(settings, name="DownloadInvoices")
        self.input_dir = input_dir
        self.input_dir.mkdir(parents=True, exist_ok=True)

        # Local simulated inbox directory
        self.simulated_inbox = Path(getattr(settings, "simulated_inbox_dir", "./data/simulated_mail_inbox"))
        self.simulated_inbox.mkdir(parents=True, exist_ok=True)

    async def execute(self) -> dict[str, Any]:
        if self.settings.simulated_mode:
            self.logger.info("Running in Local Simulation Mode")
            # Populate simulated inbox if empty
            self._ensure_simulated_emails()
            downloaded = await self._fetch_local_emails()
        else:
            self.logger.info("Running in Real IMAP Mode (Host: {})", self.settings.imap_host)
            downloaded = await self._fetch_imap_emails()

        self.logger.success("Downloaded {} invoices to {}", len(downloaded), self.input_dir)
        return {
            "count": len(downloaded),
            "files": downloaded,
        }

    def _ensure_simulated_emails(self) -> None:
        """Create mock .eml files if simulated inbox is empty."""
        eml_files = list(self.simulated_inbox.glob("*.eml"))
        if eml_files:
            return

        self.logger.info("Populating simulated inbox with mock .eml files")

        # We need sample PDF files to embed.
        pdf_names = ["INV-2025-0042.pdf", "INV-2025-0043.pdf", "INV-2025-0044.pdf"]

        for name in pdf_names:
            pdf_path = self.input_dir / name
            # If the PDF does not exist, write a simple placeholder
            if not pdf_path.exists():
                pdf_path.write_bytes(f"PDF-CONTENT-FOR-{name}".encode())

            pdf_bytes = pdf_path.read_bytes()

            # Construct a basic email message with attachment using email.mime
            from email import encoders
            from email.mime.base import MIMEBase
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            msg = MIMEMultipart()
            msg["From"] = "billing@supplier.com"
            msg["To"] = "accounting@company.com"
            msg["Subject"] = f"Invoice {name.split('.')[0]}"
            msg.attach(MIMEText(f"Please find attached your invoice {name}.", "plain"))

            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_bytes)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{name}"')
            msg.attach(part)

            eml_path = self.simulated_inbox / f"{name.split('.')[0]}.eml"
            eml_path.write_bytes(msg.as_bytes())
            self.logger.debug("Created simulated email: {}", eml_path.name)

    async def _fetch_local_emails(self) -> list[str]:
        """Simulates IMAP download by reading local .eml files."""
        saved_files: list[str] = []
        eml_files = sorted(self.simulated_inbox.glob("*.eml"))

        for eml_path in eml_files:
            self.logger.debug("Processing local email: {}", eml_path.name)
            raw_bytes = eml_path.read_bytes()
            msg = email.message_from_bytes(raw_bytes)

            extracted = self._extract_attachments(msg)
            saved_files.extend(extracted)

            # Archive processed email
            archive_path = self.simulated_inbox / "archive"
            archive_path.mkdir(exist_ok=True)
            eml_path.rename(archive_path / eml_path.name)

        return saved_files

    @with_retry(policy=default_http_retry)
    async def _fetch_imap_emails(self) -> list[str]:
        """Fetches real emails via IMAP protocol and downloads attachments."""
        saved_files: list[str] = []

        if not self.settings.imap_host or not self.settings.imap_username:
            raise ValueError("IMAP credentials and host must be set for Real IMAP Mode")

        # Connect with timeout/retry policy
        self.logger.debug("Connecting to IMAP server {}:{}", self.settings.imap_host, self.settings.imap_port)
        mail = imaplib.IMAP4_SSL(self.settings.imap_host, self.settings.imap_port)

        try:
            mail.login(self.settings.imap_username, self.settings.imap_password)
            mail.select("inbox")

            # Search for unread emails with "Invoice" in subject
            status, messages = mail.search(None, '(UNSEEN SUBJECT "Invoice")')
            if status != "OK":
                self.logger.warning("Failed to search email inbox")
                return []

            mail_ids = messages[0].split()
            self.logger.info("Found {} unread invoice emails", len(mail_ids))

            for mail_id in mail_ids:
                status, data = mail.fetch(mail_id, "(RFC822)")
                if status != "OK":
                    self.logger.error("Failed to fetch email ID: {}", mail_id.decode())
                    continue

                raw_email = data[0][1]  # type: ignore
                msg = email.message_from_bytes(raw_email)

                # Extract
                extracted = self._extract_attachments(msg)
                saved_files.extend(extracted)

                # Mark as read (SEEN)
                mail.store(mail_id, "+FLAGS", "\\Seen")

        finally:
            try:
                mail.close()
                mail.logout()
            except Exception:
                pass

        return saved_files

    def _extract_attachments(self, msg: Message) -> list[str]:
        """Extracts PDF attachments from email message object."""
        saved: list[str] = []
        subject = msg.get("Subject", "No Subject")
        self.logger.info("Extracting attachments from email: '{}'", subject)

        for part in msg.walk():
            # Skip multipart containers
            if part.get_content_maintype() == "multipart":
                continue

            filename = part.get_filename()
            if not filename:
                continue

            # Ensure we only process PDF attachments
            if filename.lower().endswith(".pdf"):
                payload = part.get_payload(decode=True)
                if not payload:
                    continue

                target_path = self.input_dir / filename
                target_path.write_bytes(payload)
                self.logger.info("Saved email attachment: {}", filename)
                saved.append(str(target_path))

        return saved
