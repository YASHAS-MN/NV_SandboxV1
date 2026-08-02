"""
Nebula Labs

Process Sensor

Observes process execution metadata.
"""

from __future__ import annotations

from subprocess import CompletedProcess

from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType


class ProcessSensor:

    name = "process"

    def collect(
        self,
        completed: CompletedProcess,
        bus: ObservationBus,
    ) -> None:

        bus.publish(
            sensor=self.name,
            event_type=EventType.PROCESS_EXIT,
            payload={
                "exit_code": completed.returncode,
                "stdout_bytes": len(completed.stdout),
                "stderr_bytes": len(completed.stderr),
            },
        )
