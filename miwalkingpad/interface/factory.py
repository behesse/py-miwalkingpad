from __future__ import annotations

from miwalkingpad.event_bus import AsyncEventBus
from miwalkingpad.service import AsyncWalkingPadService
from miwalkingpad.interface.config import AppConfig, load_config
from miwalkingpad.miio_adapter import WalkingPadAdapter


def create_service(config: AppConfig | None = None) -> tuple[AppConfig, AsyncWalkingPadService]:
    cfg = config or load_config()
    adapter = WalkingPadAdapter(
        ip=cfg.walkingpad_ip,
        token=cfg.walkingpad_token,
        model=cfg.walkingpad_model,
        timeout_seconds=cfg.request_timeout_seconds,
    )
    service = AsyncWalkingPadService(adapter=adapter, event_bus=AsyncEventBus())
    return cfg, service

