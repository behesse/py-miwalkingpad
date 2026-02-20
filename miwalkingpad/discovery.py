from __future__ import annotations

import binascii
import socket
from dataclasses import dataclass
from typing import Any

import miio.miioprotocol as mproto
from miio import Device
from miio.deviceinfo import DeviceInfo


@dataclass(slots=True)
class HandshakeDiscoveryResult:
    ip: str
    device_id: str
    token: str
    auth_ok: bool = False
    info: dict[str, Any] | None = None
    auth_error: str | None = None


def discover_handshake(*, timeout: int = 5, token: str | None = None) -> list[HandshakeDiscoveryResult]:
    """Discover miIO devices via handshake broadcast/unicast and return structured data."""
    target = "<broadcast>"

    helobytes = bytes.fromhex(
        "21310020ffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    )

    found: dict[str, HandshakeDiscoveryResult] = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        for _ in range(3):
            sock.sendto(helobytes, (target, 54321))

        while True:
            try:
                data, recv_addr = sock.recvfrom(1024)
                msg = mproto.Message.parse(data)
                ip = recv_addr[0]

                if ip in found:
                    continue

                entry = HandshakeDiscoveryResult(
                    ip=ip,
                    device_id=binascii.hexlify(msg.header.value.device_id).decode(),
                    token=msg.checksum.hex(),
                )

                if token:
                    _enrich_with_token(entry=entry, token=token)

                found[ip] = entry
            except socket.timeout:
                return list(found.values())
            except Exception:
                return list(found.values())
    finally:
        sock.close()


def _enrich_with_token(*, entry: HandshakeDiscoveryResult, token: str) -> None:
    try:
        # Keep auth probe short even for wrong tokens.
        dev = Device(ip=entry.ip, token=token, timeout=2, lazy_discover=False)
        dev.retry_count = 0
        info = DeviceInfo(dev.send("miIO.info", retry_count=0))
        raw = getattr(info, "raw", None)
        entry.info = raw if isinstance(raw, dict) else {"repr": str(info)}
        entry.auth_ok = True
    except Exception as exc:  # noqa: BLE001
        entry.auth_ok = False
        entry.auth_error = str(exc)
