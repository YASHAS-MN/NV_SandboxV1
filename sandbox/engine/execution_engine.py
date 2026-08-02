"""
Nebula Labs

Execution Engine

Coordinates all sensors and produces
a BehaviorTranscript.
"""

from __future__ import annotations

import subprocess
import tempfile
import shutil
from pathlib import Path

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.sensors.filesystem_sensor import FilesystemSensor
from sandbox.sensors.process_sensor import ProcessSensor
from sandbox.core.event_types import EventType
from sandbox.observation.observation_bus import ObservationBus


class ExecutionEngine:

    def __init__(self):

        self.filesystem = FilesystemSensor()
        self.process = ProcessSensor()

    def execute(
        self,
        asset: Path,
    ):

        recorder = BehaviorRecorder()
        bus = ObservationBus(recorder)

        with tempfile.TemporaryDirectory() as tmp:

            workspace = Path(tmp)

            target = workspace / asset.name

            shutil.copy2(asset, target)

            before = self.filesystem.snapshot(workspace)

            bus.publish(
                sensor="engine",
                event_type=EventType.EXECUTION_START,
                payload={
                    "asset": asset.name,
                },
            )

            completed = subprocess.run(
                ["python", str(target)],
                cwd=workspace,
                capture_output=True,
                text=True,
            )

            self.process.collect(
                completed,
                bus,
            )

            after = self.filesystem.snapshot(workspace)

            self.filesystem.collect(
                before,
                after,
                bus,
            )

            bus.publish(
                sensor="engine",
                event_type=EventType.EXECUTION_END,
                payload={},
            )

            return recorder.export()
