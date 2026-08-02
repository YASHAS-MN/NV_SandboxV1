"""
Nebula Labs

Observation Bus

Receives observations from sensors and forwards them
to the BehaviorRecorder.

This is the only communication channel between
Sensors and the Recorder.
"""

from __future__ import annotations

from typing import Any

from sandbox.behavior.behavior_recorder import BehaviorRecorder


class ObservationBus:

    def __init__(
        self,
        recorder: BehaviorRecorder,
    ) -> None:

        self._recorder = recorder

    def publish(
        self,
        *,
        sensor: str,
        event_type,
        payload: dict[str, Any],
    ) -> None:

        self._recorder.record(
            sensor=sensor,
            event_type=event_type,
            payload=payload,
        )
