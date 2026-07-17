"""
Email utilities using standard library imaplib, smtplib and email modules.
"""

from __future__ import annotations

import email
import imaplib
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Sequence

from ..exceptions import DataProcessingError


class EmailClient:
    """Helper class to receive and send emails using standard Python protocols."""

    @staticmethod
    def download_attachments(
        host: str,
        username: str,
        password: str,
        folder: str = "INBOX",
        search_criteria: str = "UNSEEN",
        output_dir: str | Path | None = None,
        port: int = 993,
        ssl: bool = True,
    ) -> list[Path]:
        """
        Connect to an IMAP server, find emails matching search_criteria,
        download their attachments to output_dir, and return paths to the downloaded files.
        """
        output_path = Path(output_dir) if output_dir else Path.cwd()
        output_path.mkdir(parents=True, exist_ok=True)
        downloaded_files: list[Path] = []

        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(host, port) if ssl else imaplib.IMAP4(host, port)
            mail.login(username, password)
            mail.select(folder)

            # Search emails
            status, response = mail.search(None, search_criteria)
            if status != "OK":
                raise DataProcessingError(f"IMAP search failed with status {status}")

            email_ids = response[0].split()
            for mail_id in email_ids:
                # Fetch message content
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                if status != "OK" or not msg_data:
                    continue

                raw_email = msg_data[0]
                if isinstance(raw_email, tuple):
                    raw_email = raw_email[1]
                if isinstance(raw_email, bytes):
                    msg = email.message_from_bytes(raw_email)
                else:
                    msg = email.message_from_string(str(raw_email))

                # Process parts for attachments
                for part in msg.walk():
                    if part.get_content_maintype() == "multipart":
                        continue
                    if part.get("Content-Disposition") is None:
                        continue

                    filename = part.get_filename()
                    if filename:
                        # Decode filename if needed
                        decoded = email.header.decode_header(filename)
                        filename_str = ""
                        for part_str, encoding in decoded:
                            if isinstance(part_str, bytes):
                                filename_str += part_str.decode(encoding or "utf-8", errors="ignore")
                            else:
                                filename_str += str(part_str)

                        file_path = output_path / filename_str
                        # Save attachment
                        with open(file_path, "wb") as f:
                            payload = part.get_payload(decode=True)
                        if isinstance(payload, bytes):
                            f.write(payload)
                        downloaded_files.append(file_path)

            mail.logout()
            return downloaded_files

        except Exception as exc:
            raise DataProcessingError(f"IMAP email fetch or attachment download failed: {exc}") from exc

    @staticmethod
    def send_email(
        host: str,
        username: str,
        password: str,
        to_addr: str | Sequence[str],
        subject: str,
        body: str,
        attachments: Sequence[str | Path] | None = None,
        port: int = 587,
        use_tls: bool = True,
        subtype: str = "html",
    ) -> None:
        """
        Send an email via SMTP.
        """
        # Prepare recipients
        recipients = [to_addr] if isinstance(to_addr, str) else list(to_addr)

        # Create message container
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        # Attach body
        msg.attach(MIMEText(body, subtype))

        # Attach files
        if attachments:
            for attach_path in attachments:
                path = Path(attach_path)
                if not path.exists():
                    raise DataProcessingError(f"Attachment file not found: {path}")

                try:
                    with open(path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=path.name)
                    part["Content-Disposition"] = f'attachment; filename="{path.name}"'
                    msg.attach(part)
                except Exception as exc:
                    raise DataProcessingError(f"Failed to attach file {path.name}: {exc}") from exc

        try:
            # Connect and send
            server = smtplib.SMTP(host, port)
            if use_tls:
                server.starttls()
            server.login(username, password)
            server.sendmail(username, recipients, msg.as_string())
            server.quit()
        except Exception as exc:
            raise DataProcessingError(f"SMTP email sending failed: {exc}") from exc
