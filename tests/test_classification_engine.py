from sandbox.intake.classification.engine import ClassificationEngine
from sandbox.intake.evidence import (
    ExtensionEvidence,
    MagicEvidence,
)

engine = ClassificationEngine()

print("--- Test 1 (Agreement) ---")
result1 = engine.classify(
    [
        ExtensionEvidence(".exe"),
        MagicEvidence(
            signature=b"MZ",
            hex_signature="4D5A",
            matched_format="PE",
        ),
    ]
)

print(result1.to_dict())

print("\n--- Test 2 (Conflict) ---")
result2 = engine.classify(
    [
        ExtensionEvidence(".png"),
        MagicEvidence(
            signature=b"MZ",
            hex_signature="4D5A",
            matched_format="PE",
        ),
    ]
)

print(result2.to_dict())
