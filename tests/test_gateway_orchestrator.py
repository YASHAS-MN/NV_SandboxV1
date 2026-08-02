from pathlib import Path

from sandbox.orchestration import GatewayOrchestrator

sample = Path("sample.exe")

sample.write_bytes(bytes.fromhex("4D5A"))

gateway = GatewayOrchestrator()

result = gateway.verify(sample)

print(result.to_dict())

# Verification assertions
assert result.classification.category.value == "EXECUTABLE"
assert result.static_analysis.risk_level is not None
assert set(result.to_dict().keys()) == {"classification", "static_analysis"}

sample.unlink()
