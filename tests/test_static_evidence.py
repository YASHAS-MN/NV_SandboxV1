from sandbox.static_analysis.evidence import (
    HashEvidence,
    EntropyEvidence,
    YaraEvidence,
)

print(
    HashEvidence(
        algorithm="sha256",
        digest="abcd1234",
        file_size=2048,
    ).to_dict()
)

print(
    EntropyEvidence(
        entropy=7.81,
        sample_size=2048,
        classification="HIGH",
    ).to_dict()
)

print(
    YaraEvidence(
        matched_rules=[
            "Trojan.Generic",
            "Packed.Binary",
        ]
    ).to_dict()
)
