import os
from pathlib import Path

from sandbox.static_analysis.analyzers.entropy_analyzer import EntropyAnalyzer

sample = Path("random.bin")

sample.write_bytes(os.urandom(4096))

result = EntropyAnalyzer().analyze(sample)

print(result.to_dict())

assert result.classification == "HIGH"

sample.unlink()
