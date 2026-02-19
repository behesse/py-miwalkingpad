"""Structured public type exports for backend consumers."""

from miwalkingpad.types.errors import (
    CommandValidationError,
    ConfigurationError,
    DeviceCommunicationError,
    WalkingPadAppError,
)
from miwalkingpad.types.events import (
    CommandExecutedEvent,
    ErrorEvent,
    OperationTimingEvent,
    StatusUpdatedEvent,
)
from miwalkingpad.types.models import CommandResult, PadMode, PadSensitivity, PadStatus

__all__ = [
    "PadMode",
    "PadSensitivity",
    "PadStatus",
    "CommandResult",
    "StatusUpdatedEvent",
    "CommandExecutedEvent",
    "ErrorEvent",
    "OperationTimingEvent",
    "WalkingPadAppError",
    "ConfigurationError",
    "DeviceCommunicationError",
    "CommandValidationError",
]
