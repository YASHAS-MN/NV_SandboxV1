from pathlib import Path

from sandbox.intake import IntakeGateway

sample = Path("sample.exe")

sample.write_bytes(bytes.fromhex("4D5A"))

gateway = IntakeGateway()

result = gateway.run(sample)

print(result.to_dict())

sample.unlink()
