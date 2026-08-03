"""
Nebula Labs

Process Executor
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class ProcessExecutor:
    """
    Thin wrapper around process execution.

    Future implementations may replace
    subprocess with gVisor, Firecracker,
    WSL, etc.
    """

    def execute(
        self,
        command: list[str],
        cwd: Path,
        timeout: float | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess:

        return subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=False,
            timeout=timeout,
            env=env,
        )
