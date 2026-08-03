"""
Nebula Labs

Workspace Manager
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path


class WorkspaceManager:

    def __init__(self) -> None:

        self._directory: Path | None = None

    @property
    def path(self) -> Path:

        if self._directory is None:
            raise RuntimeError(
                "Workspace has not been created."
            )

        return self._directory

    def create(
        self,
    ) -> Path:

        self._directory = Path(
            tempfile.mkdtemp(
                prefix="nebula_runtime_"
            )
        )

        return self._directory

    def cleanup(
        self,
    ) -> None:

        if self._directory is None:
            return

        shutil.rmtree(
            self._directory,
            ignore_errors=True,
        )

        self._directory = None
