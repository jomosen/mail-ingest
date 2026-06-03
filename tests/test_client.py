import pytest

from mail_ingest.client import fetch_messages, get_mailbox


def test_get_mailbox_passes_env_credentials_to_login(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMAP_HOST", "imap.example.com")
    monkeypatch.setenv("IMAP_PORT", "993")
    monkeypatch.setenv("IMAP_USER", "user@example.com")
    monkeypatch.setenv("IMAP_PASSWORD", "s3cr3t")

    captured: dict = {}

    class FakeMailBox:
        def __init__(self, host: str, port: int = 993) -> None:
            captured["host"] = host
            captured["port"] = port

        def login(self, user: str, password: str) -> "FakeMailBox":
            captured["user"] = user
            captured["password"] = password
            return self

        def __enter__(self) -> "FakeMailBox":
            return self

        def __exit__(self, *args: object) -> None:
            pass

    monkeypatch.setattr("mail_ingest.client.MailBox", FakeMailBox)

    get_mailbox()

    assert captured == {
        "host": "imap.example.com",
        "port": 993,
        "user": "user@example.com",
        "password": "s3cr3t",
    }


def test_fetch_messages_uses_inbox_when_folder_env_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMAP_HOST", "imap.example.com")
    monkeypatch.setenv("IMAP_USER", "user@example.com")
    monkeypatch.setenv("IMAP_PASSWORD", "s3cr3t")
    monkeypatch.delenv("IMAP_FOLDER", raising=False)

    folder_calls: list[str] = []

    class FakeFolder:
        def set(self, name: str) -> None:
            folder_calls.append(name)

    class FakeMailBox:
        def __init__(self, host: str, port: int = 993) -> None:
            self.folder = FakeFolder()

        def login(self, user: str, password: str) -> "FakeMailBox":
            return self

        def __enter__(self) -> "FakeMailBox":
            return self

        def __exit__(self, *args: object) -> None:
            pass

        def fetch(self, criteria: object, *, mark_seen: bool = False):
            return iter([])

    monkeypatch.setattr("mail_ingest.client.MailBox", FakeMailBox)

    list(fetch_messages())  # exhaust the generator

    assert folder_calls == ["INBOX"]
