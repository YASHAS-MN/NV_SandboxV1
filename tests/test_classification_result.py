from sandbox.intake.asset_types import AssetCategory
from sandbox.intake.classification import ClassificationResult
from sandbox.intake.evidence import ExtensionEvidence

result = ClassificationResult(
    category=AssetCategory.EXECUTABLE,
    confidence=1.0,
    evidence_used=[
        ExtensionEvidence(".exe")
    ],
)

print(result.to_dict())
