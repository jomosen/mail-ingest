"""PDF attachment extraction from IMAP messages."""

from pathlib import Path

from imap_tools import MailMessage


def save_pdf_attachments(msg: MailMessage, dest_dir: str = "downloads") -> list[Path]:
    """Save all PDF attachments from *msg* to *dest_dir*.

    Creates *dest_dir* if it does not exist. Returns the list of saved file paths.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    saved: list[Path] = []
    for attachment in msg.attachments:
        if attachment.filename.lower().endswith(".pdf"):
            path = dest / attachment.filename
            path.write_bytes(attachment.payload)
            saved.append(path)

    return saved
