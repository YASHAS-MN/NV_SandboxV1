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

        self._pipeline = [
            IntakeGateway(),
            StaticGateway(),
        ]

    @property
    def pipeline(self):

        return tuple(self._pipeline)

    def verify(
        self,
        asset: Path,
    ) -> VerificationResult:

        results = {}

        for stage in self._pipeline:

            results[stage.name] = stage.run(asset)

        return VerificationResult(
            classification=results["intake"],
            static_analysis=results["static"],
        )
