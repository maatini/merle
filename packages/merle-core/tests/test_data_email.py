"""
Mocked unit tests for merle_core.data.email.EmailClient.
Uses mocks for imaplib/smtplib — no real network.
"""

from __future__ import annotations

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from merle_core.data.email import EmailClient
from merle_core.exceptions import DataProcessingError


def _make_raw_email_with_attachment(filename: str, content: bytes) -> bytes:
    msg = MIMEMultipart()
    msg["From"] = "sender@example.com"
    msg["To"] = "user@example.com"
    msg["Subject"] = "Test"
    msg.attach(MIMEText("body", "plain"))

    part = MIMEApplication(content, Name=filename)
    part["Content-Disposition"] = f'attachment; filename="{filename}"'
    msg.attach(part)
    return msg.as_bytes()


class TestDownloadAttachments:
    def test_download_attachments_success(self, tmp_path: Path):
        raw = _make_raw_email_with_attachment("invoice.pdf", b"%PDF-fake")

        mock_mail = MagicMock()
        mock_mail.login.return_value = ("OK", [b"Logged in"])
        mock_mail.select.return_value = ("OK", [b"1"])
        mock_mail.search.return_value = ("OK", [b"1"])
        mock_mail.fetch.return_value = ("OK", [(b"1 (RFC822)", raw)])
        mock_mail.logout.return_value = ("BYE", [b""])

        with patch("merle_core.data.email.imaplib.IMAP4_SSL", return_value=mock_mail):
            files = EmailClient.download_attachments(
                host="imap.example.com",
                username="user@example.com",
                password="secret",
                output_dir=tmp_path,
            )

        assert len(files) == 1
        assert files[0].name == "invoice.pdf"
        assert files[0].read_bytes() == b"%PDF-fake"
        mock_mail.login.assert_called_once_with("user@example.com", "secret")
        mock_mail.select.assert_called_once_with("INBOX")

    def test_download_attachments_search_failure(self, tmp_path: Path):
        mock_mail = MagicMock()
        mock_mail.search.return_value = ("NO", [b"bad"])

        with patch("merle_core.data.email.imaplib.IMAP4_SSL", return_value=mock_mail):
            with pytest.raises(DataProcessingError, match="IMAP"):
                EmailClient.download_attachments(
                    host="imap.example.com",
                    username="u",
                    password="p",
                    output_dir=tmp_path,
                )

    def test_download_attachments_connection_error(self, tmp_path: Path):
        with patch(
            "merle_core.data.email.imaplib.IMAP4_SSL",
            side_effect=OSError("connection refused"),
        ):
            with pytest.raises(DataProcessingError, match="IMAP email fetch"):
                EmailClient.download_attachments(
                    host="imap.example.com",
                    username="u",
                    password="p",
                    output_dir=tmp_path,
                )

    def test_download_attachments_non_ssl(self, tmp_path: Path):
        mock_mail = MagicMock()
        mock_mail.search.return_value = ("OK", [b""])  # no messages
        mock_mail.logout.return_value = ("BYE", [b""])

        with patch("merle_core.data.email.imaplib.IMAP4", return_value=mock_mail) as mock_imap:
            files = EmailClient.download_attachments(
                host="imap.example.com",
                username="u",
                password="p",
                output_dir=tmp_path,
                ssl=False,
                port=143,
            )

        assert files == []
        mock_imap.assert_called_once_with("imap.example.com", 143)


class TestSendEmail:
    def test_send_email_success(self, tmp_path: Path):
        attach = tmp_path / "report.txt"
        attach.write_text("hello")

        mock_server = MagicMock()
        with patch("merle_core.data.email.smtplib.SMTP", return_value=mock_server) as mock_smtp:
            EmailClient.send_email(
                host="smtp.example.com",
                username="bot@example.com",
                password="secret",
                to_addr="dest@example.com",
                subject="Report",
                body="<b>hi</b>",
                attachments=[attach],
                port=587,
                use_tls=True,
            )

        mock_smtp.assert_called_once_with("smtp.example.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("bot@example.com", "secret")
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

        # Verify recipients and payload contain subject
        args = mock_server.sendmail.call_args[0]
        assert args[0] == "bot@example.com"
        assert args[1] == ["dest@example.com"]
        assert "Report" in args[2]

    def test_send_email_multiple_recipients(self):
        mock_server = MagicMock()
        with patch("merle_core.data.email.smtplib.SMTP", return_value=mock_server):
            EmailClient.send_email(
                host="smtp.example.com",
                username="bot@example.com",
                password="secret",
                to_addr=["a@example.com", "b@example.com"],
                subject="Hi",
                body="plain",
                use_tls=False,
                subtype="plain",
            )

        mock_server.starttls.assert_not_called()
        recipients = mock_server.sendmail.call_args[0][1]
        assert recipients == ["a@example.com", "b@example.com"]

    def test_send_email_missing_attachment_raises(self, tmp_path: Path):
        missing = tmp_path / "nope.pdf"
        with pytest.raises(DataProcessingError, match="Attachment file not found"):
            EmailClient.send_email(
                host="smtp.example.com",
                username="bot@example.com",
                password="secret",
                to_addr="dest@example.com",
                subject="x",
                body="y",
                attachments=[missing],
            )

    def test_send_email_smtp_failure(self):
        with patch("merle_core.data.email.smtplib.SMTP", side_effect=OSError("smtp down")):
            with pytest.raises(DataProcessingError, match="SMTP email sending failed"):
                EmailClient.send_email(
                    host="smtp.example.com",
                    username="bot@example.com",
                    password="secret",
                    to_addr="dest@example.com",
                    subject="x",
                    body="y",
                )
