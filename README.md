# mail-ingest

![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A small helper that connects to an IMAP mailbox, fetches messages, and saves PDF attachments to a local folder.

## Installation

```bash
pip install -e .
cp .env.example .env   # fill in your credentials
```

## Configuration

| Variable | Description | Default |
|---|---|---|
| `IMAP_HOST` | IMAP server hostname | — |
| `IMAP_PORT` | IMAP port | `993` |
| `IMAP_USER` | Mailbox username | — |
| `IMAP_PASSWORD` | Mailbox password | — |
| `IMAP_FOLDER` | Folder to read | `INBOX` |

## Usage

```python
from dotenv import load_dotenv
from mail_ingest import get_mailbox, fetch_messages, save_pdf_attachments

load_dotenv()

# List all folders in the mailbox
with get_mailbox() as mailbox:
    for folder in mailbox.folder.list():
        print(folder)

# Fetch all messages and save PDF attachments
for msg in fetch_messages(unseen_only=False):
    paths = save_pdf_attachments(msg, dest_dir="downloads")
    print(msg.date, msg.subject, paths)
```

`fetch_messages` yields [`MailMessage`](https://github.com/ikvk/imap_tools) objects directly from imap-tools, so all their attributes (`msg.from_`, `msg.to`, `msg.html`, …) are available.
