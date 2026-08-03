"""
Nebula Labs

Canonical Behavior Transcript (CBTS)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.core.events import Event
from sandbox.behavior.context import ObservationContext


@dataclass(frozen=True, slots=True)
class BehaviorTranscript:
    """
    Canonical behavior transcript produced after
    dynamic execution.
    """

    context: ObservationContext

    event_count: int

    events: list[Event] = field(default_factory=list)

    def canonical_dict(self):
        return [
            event.canonical_dict()
            for event in self.events
        ]

    def to_dict(self):

        return {

            "context": self.context.to_dict(),

            "event_count": self.event_count,

            "events": [

                event.to_dict()

                for event in self.events

            ],

        }
