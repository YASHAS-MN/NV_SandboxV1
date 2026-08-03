from pathlib import Path

from sandbox.static_analysis import StaticGateway

sample = Path("sample.bin")

sample.write_bytes(b"Nebula Labs")

gateway = StaticGateway()

result = gateway.run(sample)

print(result.to_dict())

sample.unlink()
