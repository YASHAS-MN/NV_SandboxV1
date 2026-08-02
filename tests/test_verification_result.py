from sandbox.intake.asset_types import AssetCategory

from sandbox.intake.classification import (
    ClassificationResult,
)

from sandbox.static_analysis.report import (
    StaticAnalysisResult,
)

from sandbox.orchestration import VerificationResult

classification = ClassificationResult(
    category=AssetCategory.EXECUTABLE,
    confidence=1.0,
)

static = StaticAnalysisResult(
    risk_level="LOW",
    confidence=0.75,
)

result = VerificationResult(
    classification=classification,
    static_analysis=static,
)

print(result.to_dict())
