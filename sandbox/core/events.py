"""
Nebula Labs
Canonical Event Model

Every observable behavior inside the sandbox is represented as an Event.
This file defines the protocol-level event structure.

Sprint:
S1-1 Behavior Recorder Foundation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Event:
    """
    Canonical protocol event.

    Consensus-critical information only.
    """

    sequence: int
    sensor: str
    event_type: str
    payload: dict[str, Any]

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "sensor": self.sensor,
            "event_type": self.event_type,
            "payload": self.payload,
        }


@dataclass(frozen=True, slots=True)
class RuntimeEventMetadata:
    """
    Runtime-only metadata.

    Never participates in consensus hashing.
    """

    relative_time_ms: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "relative_time_ms": self.relative_time_ms,
        }
