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

from sandbox.behavior import ObservationContext, TranscriptBuilder
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

        context = ObservationContext(
            protocol_version="1.0",
            runtime_profile="python-runtime-v1",
            observation_profile="default",
            policy_version="1.0",
        )
        builder = TranscriptBuilder(context)
        bus = ObservationBus()
        bus.set_builder(builder)

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

            return builder.build()
