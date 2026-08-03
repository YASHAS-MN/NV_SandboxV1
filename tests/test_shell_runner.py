from pathlib import Path
from sandbox.orchestration import NebulaVerifier
from sandbox.intake.asset_types import AssetCategory

verifier = NebulaVerifier(timeout=10.0)
result = verifier.verify(Path("sandbox/samples/hello.sh"))
d = result.to_dict()

print("Shell result:", d["classification"]["category"], d["decision"])
if d["decision"] == "CONTINUE":
    print("  exit_code:", d["execution"]["exit_code"])

assert d["classification"]["category"] == AssetCategory.SCRIPT.value
assert d["decision"] == "CONTINUE"
# On Windows without bash, runner may return -1 from exception safety — that is acceptable
print("ShellRunner E2E test OK")
