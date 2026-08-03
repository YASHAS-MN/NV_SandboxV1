"""
Nebula Labs

JavaScript Runner

Executes .js / .ts / .mjs files using Node.js.
Requires `node` to be installed and available in PATH.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path

from sandbox.runtime.runner import Runner
from sandbox.runtime.result import ExecutionResult
from sandbox.runtime.process_executor import ProcessExecutor
from sandbox.runtime.workspace import WorkspaceManager


class JavaScriptRunner(Runner):

    def __init__(
        self,
        executor: ProcessExecutor,
        timeout: float = 30.0,
    ) -> None:
        self._executor = executor
        self._timeout = timeout

    @property
    def name(self) -> str:
        return "javascript"

    def supports(self, asset: Path) -> bool:
        return asset.suffix.lower() in (".js", ".ts", ".mjs", ".cjs")

    def execute(
        self,
        asset: Path,
        workspace: WorkspaceManager,
    ) -> ExecutionResult:

        runtime_asset = workspace.path / asset.name
        shutil.copy2(asset, runtime_asset)
        runtime_asset.chmod(0o444)

        start = time.perf_counter()

        safe_env = {
            "NODE_ENV": "sandbox",
            "NO_COLOR": "1",
            "PYTHONPATH": str(workspace.path),  # for shim compatibility
        }
        if "SystemRoot" in os.environ:
            safe_env["SystemRoot"] = os.environ["SystemRoot"]
        if "PATH" in os.environ:
            safe_env["PATH"] = os.environ["PATH"]

        try:
            result = self._executor.execute(
                command=["node", runtime_asset.name],
                cwd=workspace.path,
                timeout=self._timeout,
                env=safe_env,
            )
            exit_code = result.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            exit_code = -1
            timed_out = True

        duration = int((time.perf_counter() - start) * 1000)

        return ExecutionResult(
            exit_code=exit_code,
            timed_out=timed_out,
            duration_ms=duration,
        )
