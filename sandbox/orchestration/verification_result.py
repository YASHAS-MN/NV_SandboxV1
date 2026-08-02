"""
Nebula Labs

Verification Result

Top-level protocol artifact returned by the
Gateway Orchestrator.
"""

from __future__ import annotations

from dataclasses import dataclass

from sandbox.intake.classification import ClassificationResult
from sandbox.static_analysis.report import StaticAnalysisResult


@dataclass(frozen=True, slots=True)
class VerificationResult:

    classification: ClassificationResult

    static_analysis: StaticAnalysisResult

    def to_dict(self):

        return {

            "classification":
                self.classification.to_dict(),

            "static_analysis":
                self.static_analysis.to_dict(),

        }
