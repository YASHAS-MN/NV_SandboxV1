"""
Nebula Labs

Behavior Transcript

Canonical protocol artifact produced by the
Behavior Recorder.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.core.events import Event


@dataclass(slots=True)
class BehaviorTranscript:
    """
    Immutable behavioral transcript.

    This object represents the complete
    observation of one execution.
    """

    events: list[Event] = field(default_factory=list)

    def event_count(self) -> int:
        return len(self.events)

    def to_dict(self) -> list[dict]:
        return [event.to_dict() for event in self.events]
