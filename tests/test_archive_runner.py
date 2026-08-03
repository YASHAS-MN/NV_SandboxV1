import tempfile
import zipfile
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

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    loop = root / "loop.py"
    loop.write_text("while True:\n    pass\n")

    archive = root / "loop.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(loop, arcname="loop.py")

    timed_out = NebulaVerifier(timeout=1.0).verify(archive).to_dict()

    assert timed_out["classification"]["category"] == AssetCategory.ARCHIVE.value
    assert timed_out["decision"] == "CONTINUE"
    assert timed_out["execution"]["timed_out"] is True
    assert timed_out["execution"]["exit_code"] == -1

print("ArchiveRunner E2E test OK")
