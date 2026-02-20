from __future__ import annotations

from miwalkingpad.discovery import discover_handshake


def test_discover_handshake_returns_list() -> None:
    # On CI/dev machines there may be no devices; function must still return list.
    found = discover_handshake(timeout=1)
    assert isinstance(found, list)

