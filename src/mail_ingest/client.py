"""IMAP connection and message retrieval."""

import os
from collections.abc import Iterator

from imap_tools import AND, MailBox, MailMessage


def get_mailbox() -> MailBox:
    """Return an authenticated MailBox usable as a context manager.

    Reads IMAP_HOST, IMAP_USER, IMAP_PASSWORD and optionally IMAP_PORT
    (default 993) from environment variables.
    """
    host = os.environ["IMAP_HOST"]
    port = int(os.environ.get("IMAP_PORT", 993))
    user = os.environ["IMAP_USER"]
    password = os.environ["IMAP_PASSWORD"]
    return MailBox(host, port).login(user, password)


def fetch_messages(
    folder: str | None = None,
    unseen_only: bool = True,
    mark_seen: bool = False,
) -> Iterator[MailMessage]:
    """Yield messages from *folder*, defaulting to the IMAP_FOLDER env var or INBOX.

    Args:
        folder: Mailbox folder name. Falls back to IMAP_FOLDER env var, then INBOX.
        unseen_only: When True, only unseen messages are fetched.
        mark_seen: When True, fetched messages are marked as seen on the server.
    """
    target_folder = folder or os.environ.get("IMAP_FOLDER", "INBOX")
    criteria = AND(seen=False) if unseen_only else "ALL"

    with get_mailbox() as mailbox:
        mailbox.folder.set(target_folder)
        yield from mailbox.fetch(criteria, mark_seen=mark_seen)
