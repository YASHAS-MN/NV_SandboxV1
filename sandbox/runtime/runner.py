"""
Nebula Labs

Execution Runner Protocol
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from sandbox.runtime import ExecutionSession
from sandbox.runtime.workspace import WorkspaceManager


class Runner(ABC):
    """
    Base class for all executable runtimes.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def supports(
        self,
        asset: Path,
    ) -> bool:
        """
        Returns True if this runner can execute
        the supplied asset.
        """
        ...

    @abstractmethod
    def execute(
        self,
        asset: Path,
        workspace: WorkspaceManager,
    ) -> ExecutionSession:
        ...
