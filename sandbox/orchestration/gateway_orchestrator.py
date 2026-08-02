"""
Nebula Labs

Gateway Orchestrator

Coordinates all verification gateways.
"""

from __future__ import annotations

from pathlib import Path

from sandbox.intake import IntakeGateway
from sandbox.static_analysis import StaticGateway

from sandbox.orchestration.verification_result import (
    VerificationResult,
)


class GatewayOrchestrator:

    def __init__(self) -> None:

        self._intake = IntakeGateway()
        self._static = StaticGateway()

    def verify(
        self,
        asset: Path,
    ) -> VerificationResult:

        classification = self._intake.process(asset)

        static_analysis = self._static.process(asset)

        return VerificationResult(
            classification=classification,
            static_analysis=static_analysis,
        )
