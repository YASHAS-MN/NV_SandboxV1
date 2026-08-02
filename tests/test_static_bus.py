from sandbox.static_analysis.static_bus import StaticEvidenceBus
from sandbox.static_analysis.evidence import (
    HashEvidence,
    EntropyEvidence,
)

bus = StaticEvidenceBus()

bus.publish(
    HashEvidence(
        algorithm="sha256",
        digest="abcd",
        file_size=100,
    )
)

bus.publish(
    EntropyEvidence(
        entropy=7.3,
        sample_size=100,
        classification="HIGH",
    )
)

for item in bus.snapshot():

    print(item.to_dict())
