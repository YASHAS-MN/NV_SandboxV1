"""
Nebula Labs

Execution Policy Engine

Determines the next verification step based on
gateway protocol artifacts.
"""

from __future__ import annotations

from sandbox.intake.asset_types import AssetCategory
from sandbox.intake.classification import ClassificationResult
from sandbox.policy.decision import (
    ExecutionAction,
    ExecutionDecision,
)
from sandbox.static_analysis.report import StaticAnalysisResult


class ExecutionPolicyEngine:

    _EXECUTION_CATEGORIES = (
        AssetCategory.EXECUTABLE,
        AssetCategory.SCRIPT,
        AssetCategory.ARCHIVE,
    )

    _STATIC_ONLY_CATEGORIES = (
        AssetCategory.IMAGE,
        AssetCategory.DOCUMENT,
        AssetCategory.AUDIO,
        AssetCategory.VIDEO,
        AssetCategory.DATA,
    )

    _LOW_RISK = "LOW"

    def evaluate(
        self,
        classification: ClassificationResult,
        static: StaticAnalysisResult,
    ) -> ExecutionDecision:

        category = classification.category
        risk = static.risk_level.upper()

        if category == AssetCategory.UNKNOWN:
            return ExecutionDecision(
                action=ExecutionAction.REJECT,
                next_gateway=None,
                reason="Unable to determine asset category.",
            )

        if risk != self._LOW_RISK:
            return ExecutionDecision(
                action=ExecutionAction.MANUAL_REVIEW,
                next_gateway=None,
                reason="Static analysis indicates elevated risk.",
                warnings=[f"Static analysis risk is {static.risk_level}."] ,
            )

        # ---------- Static assets (no execution needed) ----------

        if category in self._STATIC_ONLY_CATEGORIES:

            return ExecutionDecision(
                action=ExecutionAction.COMPLETE,
                next_gateway=None,
                reason="Static asset does not require dynamic execution.",
            )

        # ---------- Executables & Scripts ----------

        if category in self._EXECUTION_CATEGORIES:

            return ExecutionDecision(
                action=ExecutionAction.CONTINUE,
                next_gateway="dynamic",
                reason="Executable asset requires sandbox execution.",
            )

        return ExecutionDecision(
            action=ExecutionAction.REJECT,
            next_gateway=None,
            reason="Unable to determine asset category.",
        )
