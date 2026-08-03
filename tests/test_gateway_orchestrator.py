from pathlib import Path

from sandbox.orchestration import GatewayOrchestrator

sample = Path("sample.exe")

sample.write_bytes(bytes.fromhex("4D5A"))

gateway = GatewayOrchestrator()

# Pipeline verification
assert len(gateway.pipeline) == 2
assert gateway.pipeline[0].name == "intake"
assert gateway.pipeline[1].name == "static"

result = gateway.verify(sample)

print(result.to_dict())

# Verification assertions
assert result.classification.category.value == "EXECUTABLE"
assert result.static_analysis.risk_level is not None
assert set(result.to_dict().keys()) == {"classification", "static_analysis"}

sample.unlink()
