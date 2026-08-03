from pathlib import Path
from sandbox.orchestration import NebulaVerifier
from sandbox.intake.asset_types import AssetCategory

verifier = NebulaVerifier(timeout=10.0)
result = verifier.verify(Path("sandbox/samples/sample.zip"))
d = result.to_dict()

print("Archive result:", d["classification"]["category"], d["decision"])
if d.get("execution"):
    print("  exit_code:", d["execution"]["exit_code"])

assert d["classification"]["category"] == AssetCategory.ARCHIVE.value
assert d["decision"] == "CONTINUE"
assert d.get("hash") is not None

print("ArchiveRunner E2E test OK")
