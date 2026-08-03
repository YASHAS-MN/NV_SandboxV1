"""
Nebula Labs

Behavior Transcript Builder
"""

from __future__ import annotations

from sandbox.behavior.context import ObservationContext
from sandbox.behavior.transcript import BehaviorTranscript
from sandbox.core.events import Event


class TranscriptBuilder:

    def __init__(
        self,
        context: ObservationContext,
    ) -> None:

        self._context = context
        self._events: list[Event] = []

    def append(
        self,
        event: Event,
    ) -> None:

        self._events.append(event)

    def build(
        self,
    ) -> BehaviorTranscript:

        return BehaviorTranscript(

            context=self._context,

            event_count=len(self._events),

            events=list(self._events),

        )

    def reset(
        self,
    ) -> None:

        self._events.clear()
