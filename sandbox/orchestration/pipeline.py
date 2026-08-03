"""
Nebula Labs

Pipeline Stage Protocol
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class PipelineStage(ABC):
    """
    Base class for every verification gateway.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def run(
        self,
        asset: Path,
    ) -> Any:
        ...
