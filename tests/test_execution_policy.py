from sandbox.intake.asset_types import AssetCategory
from sandbox.intake.classification import ClassificationResult

from sandbox.static_analysis.report import (
    StaticAnalysisResult,
)

from sandbox.policy import ExecutionPolicyEngine

engine = ExecutionPolicyEngine()

classification = ClassificationResult(
    category=AssetCategory.EXECUTABLE,
    confidence=1.0,
)

static = StaticAnalysisResult(
    risk_level="LOW",
    confidence=0.75,
)

decision = engine.evaluate(
    classification,
    static,
)

print(decision.to_dict())

assert decision.action.value == "CONTINUE"

medium_static = StaticAnalysisResult(
    risk_level="MEDIUM",
    confidence=0.75,
)

manual_review = engine.evaluate(
    classification,
    medium_static,
)

print(manual_review.to_dict())

assert manual_review.action.value == "MANUAL_REVIEW"
