"""
Nebula Labs

Archive Runner

Recursively unpacks archive files (.zip, .tar, .gz, .tgz) into
the isolated workspace and runs NebulaVerifier on each extracted
asset.

Returns a composite ExecutionResult whose exit_code reflects the
worst outcome across all inner scans:
  - 0   all clean
  - 1   at least one inner asset was non-zero exit
  - -1  error during extraction or inner runtime exception
"""

from __future__ import annotations

import tarfile
import time
import zipfile
from pathlib import Path

from sandbox.runtime.runner import Runner
from sandbox.runtime.result import ExecutionResult
from sandbox.runtime.workspace import WorkspaceManager

_ZIP_SUFFIXES = {".zip"}
_TAR_SUFFIXES = {".tar", ".gz", ".tgz", ".bz2", ".xz"}


class ArchiveRunner(Runner):

    def __init__(self, timeout: float = 30.0) -> None:
        self._timeout = timeout

    @property
    def name(self) -> str:
        return "archive"

    def supports(self, asset: Path) -> bool:
        suffix = asset.suffix.lower()
        # Handle compound .tar.gz
        if asset.name.endswith(".tar.gz") or asset.name.endswith(".tar.bz2"):
            return True
        return suffix in (_ZIP_SUFFIXES | _TAR_SUFFIXES)

    def execute(
        self,
        asset: Path,
        workspace: WorkspaceManager,
    ) -> ExecutionResult:

        start = time.perf_counter()
        extract_dir = workspace.path / "_archive_contents"
        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            self._extract(asset, extract_dir)
        except Exception as e:
            duration = int((time.perf_counter() - start) * 1000)
            return ExecutionResult(exit_code=-1, timed_out=False, duration_ms=duration)

        # Lazily import to avoid circular dependency
        from sandbox.orchestration.verifier import NebulaVerifier

        worst_exit = 0
        for inner_file in sorted(extract_dir.rglob("*")):
            if not inner_file.is_file():
                continue
            try:
                verifier = NebulaVerifier(timeout=self._timeout)
                inner_result = verifier.verify(inner_file)
                inner_exec = inner_result.execution
                if inner_exec and inner_exec.get("exit_code", 0) != 0:
                    worst_exit = max(worst_exit, 1)
            except Exception:
                worst_exit = max(worst_exit, 1)

        duration = int((time.perf_counter() - start) * 1000)

        return ExecutionResult(
            exit_code=worst_exit,
            timed_out=False,
            duration_ms=duration,
        )

    def _extract(self, asset: Path, dest: Path) -> None:
        name = asset.name.lower()
        if name.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tar.xz", ".tar")):
            with tarfile.open(asset) as tf:
                # Safety: strip absolute paths and '..' components
                for member in tf.getmembers():
                    member_path = Path(member.name)
                    safe_parts = [
                        p for p in member_path.parts
                        if p not in ("..", ".") and not Path(p).is_absolute()
                    ]
                    member.name = str(Path(*safe_parts)) if safe_parts else member.name
                tf.extractall(dest)
        elif name.endswith(".zip"):
            with zipfile.ZipFile(asset) as zf:
                zf.extractall(dest)
        else:
            raise ValueError(f"Unsupported archive format: {asset.suffix}")
