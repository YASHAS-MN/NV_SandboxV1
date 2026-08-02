"""
Nebula Labs

Process Sensor

Observes process execution metadata.
"""

from __future__ import annotations

from subprocess import CompletedProcess

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.core.event_types import EventType


class ProcessSensor:

    name = "process"

    def collect(
        self,
        completed: CompletedProcess,
        recorder: BehaviorRecorder,
    ) -> None:

        recorder.record(
            sensor=self.name,
            event_type=EventType.PROCESS_EXIT,
            payload={
                "exit_code": completed.returncode,
                "stdout_bytes": len(completed.stdout),
                "stderr_bytes": len(completed.stderr),
            },
        )
