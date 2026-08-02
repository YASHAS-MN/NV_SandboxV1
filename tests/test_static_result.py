from sandbox.static_analysis.report import StaticAnalysisResult
from sandbox.static_analysis.evidence import (
    HashEvidence,
)

result = StaticAnalysisResult(

    risk_level="UNKNOWN",

    confidence=0.0,

    evidence_used=[
        HashEvidence(
            algorithm="sha256",
            digest="abcd",
            file_size=10,
        )
    ],
)

print(result.to_dict())
