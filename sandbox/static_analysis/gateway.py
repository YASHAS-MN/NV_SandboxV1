"""
Nebula Labs

Static Analysis Gateway

Coordinates the Static Analysis subsystem.
"""

from __future__ import annotations

from pathlib import Path

from sandbox.static_analysis.analyzers.hash_analyzer import HashAnalyzer
from sandbox.static_analysis.analyzers.entropy_analyzer import EntropyAnalyzer
from sandbox.static_analysis.report.engine import StaticAnalysisEngine
from sandbox.static_analysis.static_bus import StaticEvidenceBus


class StaticGateway:

    def __init__(self) -> None:

        self._hash = HashAnalyzer()
        self._entropy = EntropyAnalyzer()

        self._bus = StaticEvidenceBus()

        self._engine = StaticAnalysisEngine()

    def process(
        self,
        asset: Path,
    ):

        self._bus.publish(
            self._hash.analyze(asset)
        )

        self._bus.publish(
            self._entropy.analyze(asset)
        )

        result = self._engine.analyze(
            self._bus.snapshot()
        )

        self._bus.clear()

        return result
