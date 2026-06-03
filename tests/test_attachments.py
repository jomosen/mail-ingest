from dataclasses import dataclass
from pathlib import Path

import pytest

from mail_ingest.attachments import save_pdf_attachments


@dataclass
class _Attachment:
    filename: str
    payload: bytes


class _FakeMessage:
    def __init__(self, attachments: list[_Attachment]) -> None:
        self.attachments = attachments


def test_saves_only_pdf_attachments(tmp_path: Path) -> None:
    msg = _FakeMessage([
        _Attachment("invoice.pdf", b"%PDF-invoice"),
        _Attachment("RECEIPT.PDF", b"%PDF-receipt"),
        _Attachment("notes.txt", b"plain text"),
        _Attachment("", b"no filename"),
    ])

    saved = save_pdf_attachments(msg, dest_dir=str(tmp_path / "out"))

    assert len(saved) == 2
    assert (tmp_path / "out" / "invoice.pdf").read_bytes() == b"%PDF-invoice"
    assert (tmp_path / "out" / "RECEIPT.PDF").read_bytes() == b"%PDF-receipt"


def test_creates_dest_dir_if_missing(tmp_path: Path) -> None:
    dest = tmp_path / "new" / "nested"
    msg = _FakeMessage([_Attachment("doc.pdf", b"%PDF")])

    save_pdf_attachments(msg, dest_dir=str(dest))

    assert dest.is_dir()


def test_returns_correct_paths(tmp_path: Path) -> None:
    msg = _FakeMessage([_Attachment("report.pdf", b"%PDF")])

    paths = save_pdf_attachments(msg, dest_dir=str(tmp_path))

    assert paths == [tmp_path / "report.pdf"]


def test_no_attachments_returns_empty_list(tmp_path: Path) -> None:
    msg = _FakeMessage([])

    paths = save_pdf_attachments(msg, dest_dir=str(tmp_path))

    assert paths == []
