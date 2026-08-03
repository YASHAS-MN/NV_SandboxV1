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
        pass

    def execute(
        self,
        asset: Path,
    ):

        recorder = BehaviorRecorder()
        bus = ObservationBus(recorder)

        filesystem = FilesystemSensor(bus)
        process = ProcessSensor(bus)

        with tempfile.TemporaryDirectory() as tmp:

            workspace = Path(tmp)

            target = workspace / asset.name

            shutil.copy2(asset, target)

            filesystem.before_execution()
            process.before_execution()

            before = filesystem.snapshot(workspace)

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

            process.observe(completed)

            after = filesystem.snapshot(workspace)

            filesystem.observe(before, after)

            process.after_execution()
            filesystem.after_execution()

            bus.publish(
                sensor="engine",
                event_type=EventType.EXECUTION_END,
                payload={},
            )

            return recorder.export()
