"""
Nebula Labs

Canonical Behavior Transcript (CBTS)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.core.events import Event


@dataclass(frozen=True, slots=True)
class BehaviorTranscript:
    """
    Canonical behavior transcript produced after
    dynamic execution.
    """

    protocol_version: str

    event_count: int

    events: list[Event] = field(default_factory=list)

    def to_dict(self):

        return {

            "protocol_version": self.protocol_version,

            "event_count": self.event_count,

            "events": [

                event.to_dict()

                for event in self.events

            ],

        }
