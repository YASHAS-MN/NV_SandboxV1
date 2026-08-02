from sandbox.static_analysis.report.engine import StaticAnalysisEngine

from sandbox.static_analysis.evidence import (
    HashEvidence,
    EntropyEvidence,
)

engine = StaticAnalysisEngine()

print("--- Test 1 (High Entropy) ---")
result1 = engine.analyze(
    [
        HashEvidence(
            algorithm="sha256",
            digest="abcd",
            file_size=100,
        ),
        EntropyEvidence(
            entropy=7.8,
            sample_size=100,
            classification="HIGH",
        ),
    ]
)

print(result1.to_dict())

print("\n--- Test 2 (Low Entropy) ---")
result2 = engine.analyze(
    [
        HashEvidence(
            algorithm="sha256",
            digest="abcd",
            file_size=100,
        ),
        EntropyEvidence(
            entropy=2.1,
            sample_size=100,
            classification="LOW",
        ),
    ]
)

print(result2.to_dict())
