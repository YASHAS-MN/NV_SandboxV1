"""
Nebula Labs

Observation Bus

Receives observations from sensors and forwards them
to the TranscriptBuilder.
"""

from __future__ import annotations

import time
from typing import Any

from sandbox.behavior.builder import TranscriptBuilder
from sandbox.core.events import Event


class ObservationBus:

    def __init__(self) -> None:

        self._builder: TranscriptBuilder | None = None
        self._sequence = 0
        self._start_time = 0.0

    def set_builder(
        self,
        builder: TranscriptBuilder,
    ) -> None:

        self._builder = builder
        self._sequence = 0
        self._start_time = time.perf_counter()

    def publish(
        self,
        event: Event | None = None,
        *,
        sensor: str | None = None,
        event_type: Any | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:

        if self._builder is None:
            raise RuntimeError(
                "TranscriptBuilder not attached."
            )

        if event is not None:
            self._builder.append(event)
        else:
            self._sequence += 1
            elapsed = int((time.perf_counter() - self._start_time) * 1000)
            constructed_event = Event(
                sequence=self._sequence,
                sensor=sensor,
                event_type=event_type,
                relative_time_ms=elapsed,
                payload=payload,
            )
            self._builder.append(constructed_event)

    def clear(self) -> None:

        self._builder = None
