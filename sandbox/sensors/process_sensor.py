"""
Nebula Labs

Process Sensor

Observes process execution metadata.
"""

from __future__ import annotations

from subprocess import CompletedProcess

from sandbox.sensors.base import Sensor
from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType


class ProcessSensor(Sensor):

    def __init__(
        self,
        bus: ObservationBus,
    ) -> None:

        self._bus = bus
        self._completed: CompletedProcess | None = None

    @property
    def name(self) -> str:
        return "process"

    def before_execution(self) -> None:

        self._completed = None

    def observe(
        self,
        completed: CompletedProcess,
    ) -> None:

        self._completed = completed

    def after_execution(self) -> None:

        if self._completed is not None:

            self._bus.publish(
                sensor=self.name,
                event_type=EventType.PROCESS_EXIT,
                payload={
                    "exit_code": self._completed.returncode,
                    "stdout_bytes": len(self._completed.stdout),
                    "stderr_bytes": len(self._completed.stderr),
                },
            )

            self._completed = None
