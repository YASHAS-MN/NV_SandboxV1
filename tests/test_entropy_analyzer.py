from pathlib import Path

from sandbox.static_analysis.analyzers.entropy_analyzer import EntropyAnalyzer

sample = Path("entropy.bin")

sample.write_bytes(b"A" * 1024)

result = EntropyAnalyzer().analyze(sample)

print(result.to_dict())

assert result.classification == "LOW"

sample.unlink()
