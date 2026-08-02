from sandbox.intake.evidence import ExtensionEvidence
from sandbox.intake.evidence_bus import EvidenceBus

bus = EvidenceBus()

bus.publish(
    ExtensionEvidence(".exe")
)

bus.publish(
    ExtensionEvidence(".png")
)

snapshot = bus.snapshot()

for item in snapshot:
    print(item.to_dict())
