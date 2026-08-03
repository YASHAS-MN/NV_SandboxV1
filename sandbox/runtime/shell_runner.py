"""
Nebula Labs

Shell Runner

Executes shell scripts (.sh, .bash, .ps1, .bat, .cmd) inside the
isolated workspace. Selects interpreter based on file extension and
host operating system.

Supported interpreters:
  - bash    for .sh / .bash / .zsh (Unix/WSL)
  - powershell for .ps1 (Windows)
  - cmd     for .bat / .cmd (Windows)
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

_UNIX_SHELLS = {".sh", ".bash", ".zsh", ".fish"}
_PS_SHELLS   = {".ps1", ".psm1", ".psd1"}
_CMD_SHELLS  = {".bat", ".cmd"}


def _interpreter_for(suffix: str) -> list[str] | None:
    """Returns the command prefix for a given shell extension."""
    s = suffix.lower()
    if s in _UNIX_SHELLS:
        return ["bash"]
    if s in _PS_SHELLS:
        if sys.platform == "win32":
            return ["powershell", "-ExecutionPolicy", "Bypass", "-File"]
        return ["pwsh", "-File"]
    if s in _CMD_SHELLS:
        return ["cmd", "/c"]
    return None


class ShellRunner(Runner):

    def __init__(
        self,
        executor: ProcessExecutor,
        timeout: float = 30.0,
    ) -> None:
        self._executor = executor
        self._timeout = timeout

    @property
    def name(self) -> str:
        return "shell"

    def supports(self, asset: Path) -> bool:
        return asset.suffix.lower() in (
            _UNIX_SHELLS | _PS_SHELLS | _CMD_SHELLS
        )

    def execute(
        self,
        asset: Path,
        workspace: WorkspaceManager,
    ) -> ExecutionResult:

        runtime_asset = workspace.path / asset.name
        shutil.copy2(asset, runtime_asset)
        runtime_asset.chmod(0o444)

        interp = _interpreter_for(asset.suffix)
        if interp is None:
            return ExecutionResult(exit_code=-1, timed_out=False, duration_ms=0)

        start = time.perf_counter()

        safe_env = {}
        if "SystemRoot" in os.environ:
            safe_env["SystemRoot"] = os.environ["SystemRoot"]
        if "PATH" in os.environ:
            safe_env["PATH"] = os.environ["PATH"]
        if "HOME" in os.environ:
            safe_env["HOME"] = os.environ["HOME"]

        try:
            result = self._executor.execute(
                command=interp + [runtime_asset.name],
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
