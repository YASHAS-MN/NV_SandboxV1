"""
Nebula Labs

Verification Result

Top-level protocol artifact returned by the
Gateway Orchestrator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sandbox.intake.classification import ClassificationResult
from sandbox.static_analysis.report import StaticAnalysisResult


@dataclass(frozen=True, slots=True)
class VerificationResult:

    classification: ClassificationResult

    static_analysis: StaticAnalysisResult

    decision: str | None = None

    execution: dict[str, Any] | None = None

    transcript: dict[str, Any] | None = None

    hash: str | None = None

    def to_dict(self):

        res = {
            "classification": self.classification.to_dict(),
            "static_analysis": self.static_analysis.to_dict(),
        }

        if self.decision is not None:
            res["decision"] = self.decision

        if self.execution is not None:
            res["execution"] = self.execution
        if self.transcript is not None:
            res["transcript"] = self.transcript
        if self.hash is not None:
            res["hash"] = self.hash

        return res
