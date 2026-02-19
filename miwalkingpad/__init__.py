"""Public backend facade for py-xiaomi-walkingpad.

Only primary entry points are re-exported here.
Advanced consumers should import concrete types from structured submodules like
`miwalkingpad.types.models`, `miwalkingpad.types.events`, and
`miwalkingpad.types.errors`.
"""

from miwalkingpad.event_bus import AsyncEventBus
from miwalkingpad.miio_adapter import WalkingPadAdapter
from miwalkingpad.service import AsyncWalkingPadService

__all__ = [
    "AsyncEventBus",
    "AsyncWalkingPadService",
    "WalkingPadAdapter",
]
