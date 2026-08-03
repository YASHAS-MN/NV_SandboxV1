"""
Nebula Labs

Intake Gateway

Coordinates the Intake subsystem.
"""

from __future__ import annotations

from pathlib import Path

from sandbox.intake.analyzers.extension_analyzer import ExtensionAnalyzer
from sandbox.intake.analyzers.magic_analyzer import MagicAnalyzer
from sandbox.intake.classification.engine import ClassificationEngine
from sandbox.intake.evidence_bus import EvidenceBus
from sandbox.orchestration.pipeline import PipelineStage


class IntakeGateway(PipelineStage):

    def __init__(self) -> None:

        self._extension = ExtensionAnalyzer()
        self._magic = MagicAnalyzer()

        self._bus = EvidenceBus()

        self._engine = ClassificationEngine()

    @property
    def name(self) -> str:
        return "intake"

    def run(
        self,
        asset: Path,
    ):

        self._bus.publish(
            self._extension.analyze(asset)
        )

        self._bus.publish(
            self._magic.analyze(asset)
        )

        result = self._engine.classify(
            self._bus.snapshot()
        )

        self._bus.clear()

        return result
