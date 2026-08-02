from pathlib import Path

from sandbox.static_analysis.analyzers.entropy_analyzer import EntropyAnalyzer
from sandbox.static_analysis.static_bus import StaticEvidenceBus

sample = Path("entropy.bin")

sample.write_bytes(b"Nebula Labs" * 100)

bus = StaticEvidenceBus()

bus.publish(
    EntropyAnalyzer().analyze(sample)
)

for item in bus.snapshot():
    print(item.to_dict())

sample.unlink()
