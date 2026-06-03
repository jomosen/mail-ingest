"""
mail_ingest — fetches messages from an IMAP mailbox and saves PDF attachments.
"""

from .client import fetch_messages, get_mailbox
from .attachments import save_pdf_attachments

__all__ = ["get_mailbox", "fetch_messages", "save_pdf_attachments"]
