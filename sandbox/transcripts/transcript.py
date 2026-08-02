"""
Nebula Labs

Behavior Transcript

Canonical protocol artifact produced by the
Behavior Recorder.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.core.events import Event, RuntimeEventMetadata


@dataclass(slots=True)
class BehaviorTranscript:
    """
    Immutable behavioral transcript.

    This object represents the complete
    observation of one execution.
    """

    events: list[tuple[Event, RuntimeEventMetadata]] = field(default_factory=list)

    def event_count(self) -> int:
        return len(self.events)

    def canonical_dict(self):
        return [
            event.canonical_dict()
            for event, _ in self.events
        ]

    def to_dict(self):
        transcript = []
        for event, metadata in self.events:
            entry = event.canonical_dict()
            entry.update(metadata.to_dict())
            transcript.append(entry)
        return transcript
