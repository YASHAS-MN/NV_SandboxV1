"""
Nebula Labs

Python Runner
"""

from __future__ import annotations

import os
import shutil
import subprocess
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
        timeout: float = 30.0,
    ) -> None:

        self._executor = executor
        self._timeout = timeout

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

        # Make runtime copy read-only
        runtime_asset.chmod(0o444)

        start = time.perf_counter()

        safe_env = {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUNBUFFERED": "1",
        }

        if "SystemRoot" in os.environ:
            safe_env["SystemRoot"] = os.environ["SystemRoot"]

        try:
            result = self._executor.execute(

                command=[
                    sys.executable,
                    runtime_asset.name,
                ],

                cwd=workspace.path,
                timeout=self._timeout,
                env=safe_env,

            )
            exit_code = result.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            exit_code = -1
            timed_out = True

        duration = int(
            (time.perf_counter() - start) * 1000
        )

        return ExecutionResult(

            exit_code=exit_code,

            timed_out=timed_out,

            duration_ms=duration,

        )
