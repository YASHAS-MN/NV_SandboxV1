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


class ExecutionEngine:

    def __init__(self):

        self.filesystem = FilesystemSensor()

    def execute(
        self,
        asset: Path,
    ):

        recorder = BehaviorRecorder()

        with tempfile.TemporaryDirectory() as tmp:

            workspace = Path(tmp)

            target = workspace / asset.name

            shutil.copy2(asset, target)

            before = self.filesystem.snapshot(workspace)

            recorder.record(
                sensor="engine",
                event_type="EXECUTION_START",
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

            recorder.record(
                sensor="engine",
                event_type="PROCESS_EXIT",
                payload={
                    "exit_code": completed.returncode,
                    "stdout": len(completed.stdout),
                    "stderr": len(completed.stderr),
                },
            )

            after = self.filesystem.snapshot(workspace)

            self.filesystem.collect(
                before,
                after,
                recorder,
            )

            recorder.record(
                sensor="engine",
                event_type="EXECUTION_END",
                payload={},
            )

            return recorder.export()
