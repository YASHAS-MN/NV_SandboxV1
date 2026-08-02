from pathlib import Path

from sandbox.static_analysis.analyzers.hash_analyzer import HashAnalyzer

sample = Path("sample.bin")

sample.write_bytes(b"Nebula Labs")

analyzer = HashAnalyzer()

result = analyzer.analyze(sample)

print(result.to_dict())

assert len(result.digest) == 64
assert result.algorithm == "sha256"
assert result.file_size == len(b"Nebula Labs")

sample.unlink()
