"""
Nebula Labs

Abstract Sensor Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sandbox.behavior.behavior_recorder import BehaviorRecorder


class Sensor(ABC):
    """
    Every sensor observes one aspect
    of program behaviour.

    Sensors NEVER modify transcripts directly.
    """

    name: str

    @abstractmethod
    def collect(
        self,
        recorder: BehaviorRecorder,
    ) -> None:
        """
        Observe behaviour and emit events.
        """
        raise NotImplementedError
