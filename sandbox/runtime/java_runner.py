"""
Nebula Labs

Java Runner

Executes JVM assets (.jar, .class) inside the isolated workspace.
Requires `java` to be installed and available in PATH.

.jar files  → java -jar <file>
.class files → java <classname>  (classname = stem without .class)
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


class JavaRunner(Runner):

    def __init__(
        self,
        executor: ProcessExecutor,
        timeout: float = 30.0,
    ) -> None:
        self._executor = executor
        self._timeout = timeout

    @property
    def name(self) -> str:
        return "java"

    def supports(self, asset: Path) -> bool:
        return asset.suffix.lower() in (".jar", ".class", ".war", ".ear")

    def execute(
        self,
        asset: Path,
        workspace: WorkspaceManager,
    ) -> ExecutionResult:

        runtime_asset = workspace.path / asset.name
        shutil.copy2(asset, runtime_asset)
        runtime_asset.chmod(0o444)

        suffix = asset.suffix.lower()
        if suffix in (".jar", ".war", ".ear"):
            command = ["java", "-jar", runtime_asset.name]
        else:
            # .class — use stem as class name
            command = ["java", runtime_asset.stem]

        start = time.perf_counter()

        safe_env = {}
        if "SystemRoot" in os.environ:
            safe_env["SystemRoot"] = os.environ["SystemRoot"]
        if "PATH" in os.environ:
            safe_env["PATH"] = os.environ["PATH"]

        try:
            result = self._executor.execute(
                command=command,
                cwd=workspace.path,
                timeout=self._timeout,
                env=safe_env if safe_env else None,
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
