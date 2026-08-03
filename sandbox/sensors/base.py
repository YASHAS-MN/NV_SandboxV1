"""
Nebula Labs

Sensor Protocol
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Sensor(ABC):
    """
    Base class for every behavior sensor.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    def priority(self) -> int:
        return 100

    def before_execution(self) -> None:
        """
        Invoked immediately before execution starts.
        """
        return None

    def after_execution(self) -> None:
        """
        Invoked immediately after execution finishes.
        """
        return None
