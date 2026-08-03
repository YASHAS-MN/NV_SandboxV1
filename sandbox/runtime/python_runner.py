"""
Nebula Labs

Python Runner
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

from sandbox.runtime.runner import Runner
from sandbox.runtime.result import ExecutionResult
from sandbox.runtime.process_executor import ProcessExecutor
from sandbox.runtime.workspace import WorkspaceManager


class PythonRunner(Runner):

    def __init__(
        self,
        executor: ProcessExecutor,
    ) -> None:

        self._executor = executor

    @property
    def name(self) -> str:
        return "python"

    def supports(
        self,
        asset: Path,
    ) -> bool:

        return asset.suffix == ".py"

    def execute(
        self,
        asset: Path,
        workspace: WorkspaceManager,
    ) -> ExecutionResult:

        runtime_asset = workspace.path / asset.name

        shutil.copy2(asset, runtime_asset)

        start = time.perf_counter()

        result = self._executor.execute(

            command=[
                sys.executable,
                runtime_asset.name,
            ],

            cwd=workspace.path,

        )

        duration = int(
            (time.perf_counter() - start) * 1000
        )

        return ExecutionResult(

            exit_code=result.returncode,

            timed_out=False,

            duration_ms=duration,

        )
