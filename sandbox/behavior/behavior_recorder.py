"""
Nebula Labs
Behavior Recorder

Responsible for:
- Recording events
- Assigning canonical sequence numbers
- Producing immutable transcript data

Sprint:
S1-1 Behavior Recorder Foundation
"""

from __future__ import annotations

import time
from typing import Any

from sandbox.core.events import Event, RuntimeEventMetadata
from sandbox.transcripts.transcript import BehaviorTranscript


class BehaviorRecorder:
    """
    Canonical event recorder.

    This is the ONLY component allowed to assemble
    behavioral events into a transcript.
    """

    def __init__(self) -> None:
        self._events: list[tuple[Event, RuntimeEventMetadata]] = []
        self._sequence = 0
        self._start_time = time.perf_counter()

    def record(
        self,
        *,
        sensor: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> Event:

        self._sequence += 1

        elapsed = int((time.perf_counter() - self._start_time) * 1000)

        event = Event(
            sequence=self._sequence,
            sensor=sensor,
            event_type=event_type,
            payload=payload,
        )

        metadata = RuntimeEventMetadata(
            relative_time_ms=elapsed,
        )

        self._events.append(
            (
                event,
                metadata,
            )
        )

        return event

    def export(self) -> BehaviorTranscript:
        """
        Export immutable transcript.
        """

        return BehaviorTranscript(events=self._events.copy())

    def reset(self) -> None:
        self._events.clear()
        self._sequence = 0
        self._start_time = time.perf_counter()

    @property
    def event_count(self) -> int:
        return len(self._events)
