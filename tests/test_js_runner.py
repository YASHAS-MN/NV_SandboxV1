from pathlib import Path
from sandbox.orchestration import NebulaVerifier
from sandbox.intake.asset_types import AssetCategory

verifier = NebulaVerifier(timeout=10.0)
result = verifier.verify(Path("sandbox/samples/hello.js"))
d = result.to_dict()

print("JS result:", d["classification"]["category"], d["decision"])

assert d["classification"]["category"] == AssetCategory.SCRIPT.value
assert d["decision"] == "CONTINUE"
assert d["execution"]["exit_code"] == 0, f"Got exit_code {d['execution']['exit_code']}"
assert len(d["hash"]) == 64

print("JavaScriptRunner E2E test OK")
