from pathlib import Path

from sandbox.orchestration import NebulaVerifier
from sandbox.intake.asset_types import AssetCategory


def test_hello_pipeline():

    # Register short timeout for the runner under test
    verifier = NebulaVerifier(timeout=2.0)

    result = verifier.verify(Path("sandbox/samples/hello.py"))
    result_dict = result.to_dict()

    # 1. Verify Classification
    assert result_dict["classification"]["category"] == AssetCategory.SCRIPT.value
    assert result_dict["classification"]["confidence"] == 0.7

    # 2. Verify Static Analysis
    assert result_dict["static_analysis"]["risk_level"] == "LOW"

    # 3. Verify Decision
    assert result_dict["decision"] == "CONTINUE"

    # 4. Verify Sandbox Execution
    assert result_dict["execution"]["exit_code"] == 0
    assert result_dict["execution"]["timed_out"] is False
    assert result_dict["execution"]["duration_ms"] >= 0

    # 5. Verify Transcript & Hash
    assert result_dict["transcript"]["context"] is not None
    assert len(result_dict["hash"]) == 64


def test_infinite_loop_pipeline():

    verifier = NebulaVerifier(timeout=1.0)

    result = verifier.verify(Path("sandbox/samples/infinite_loop.py"))
    result_dict = result.to_dict()

    # 1. Verify Classification
    assert result_dict["classification"]["category"] == AssetCategory.SCRIPT.value

    # 2. Verify Decision
    assert result_dict["decision"] == "CONTINUE"

    # 3. Verify Sandbox Execution (Timeout case)
    assert result_dict["execution"]["exit_code"] == -1
    assert result_dict["execution"]["timed_out"] is True
    assert result_dict["execution"]["duration_ms"] >= 1000  # Should be close to the 1.0s timeout

    # 4. Verify Transcript & Hash
    assert result_dict["transcript"]["context"] is not None
    assert len(result_dict["hash"]) == 64


# Run E2E pipeline checks
test_hello_pipeline()
test_infinite_loop_pipeline()

print("NebulaVerifier E2E tests OK")
