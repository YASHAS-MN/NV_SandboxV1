from pathlib import Path

from sandbox.static_analysis.analyzers.hash_analyzer import HashAnalyzer
from sandbox.static_analysis.static_bus import StaticEvidenceBus

sample = Path("sample.bin")

sample.write_bytes(b"Nebula")

bus = StaticEvidenceBus()

bus.publish(
    HashAnalyzer().analyze(sample)
)

for item in bus.snapshot():

    print(item.to_dict())

sample.unlink()
