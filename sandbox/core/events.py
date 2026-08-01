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
    Immutable representation of a single observed behavior.

    Notes
    -----
    - sequence defines canonical ordering.
    - relative_time_ms is informational only.
    - payload must contain only deterministic values.
    """

    sequence: int

    sensor: str

    event_type: str

    relative_time_ms: int

    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """
        Convert event into canonical dictionary.

        Keys are intentionally emitted
        in deterministic order.
        """

        return {
            "sequence": self.sequence,
            "sensor": self.sensor,
            "event_type": self.event_type,
            "relative_time_ms": self.relative_time_ms,
            "payload": self.payload,
        }
