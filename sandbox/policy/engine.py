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

    def evaluate(
        self,
        classification: ClassificationResult,
        static: StaticAnalysisResult,
    ) -> ExecutionDecision:

        category = classification.category

        # ---------- Static assets ----------

        if category in (
            AssetCategory.IMAGE,
            AssetCategory.DOCUMENT,
        ):

            return ExecutionDecision(
                action=ExecutionAction.COMPLETE,
                next_gateway=None,
                reason="Static asset does not require dynamic execution.",
            )

        # ---------- Executables ----------

        if category in (
            AssetCategory.EXECUTABLE,
            AssetCategory.SCRIPT,
        ):

            return ExecutionDecision(
                action=ExecutionAction.CONTINUE,
                next_gateway="dynamic",
                reason="Executable asset requires sandbox execution.",
            )

        # ---------- Archives ----------

        if category == AssetCategory.ARCHIVE:

            return ExecutionDecision(
                action=ExecutionAction.MANUAL_REVIEW,
                next_gateway=None,
                reason="Archive inspection not yet implemented.",
                warnings=[
                    "Container analysis pending.",
                ],
            )

        # ---------- Unknown ----------

        return ExecutionDecision(
            action=ExecutionAction.REJECT,
            next_gateway=None,
            reason="Unable to determine asset category.",
        )
