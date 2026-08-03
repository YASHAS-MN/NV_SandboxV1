from pathlib import Path

from sandbox.runtime import (
    ExecutionRuntime,
    WorkspaceManager,
    RunnerManager,
    PythonRunner,
)
from sandbox.runtime.process_executor import ProcessExecutor
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors import SensorManager
from sandbox.sensors.process_sensor import ProcessSensor
from sandbox.sensors.filesystem_sensor import FilesystemSensor
from sandbox.behavior import TranscriptValidator, TranscriptHasher

# 1. Setup Runtime
bus = ObservationBus()
sensor_manager = SensorManager()
sensor_manager.register(ProcessSensor(bus))
sensor_manager.register(FilesystemSensor(bus))

runner_manager = RunnerManager()
# Register runner with a 2.0 second timeout for fast infinite loop testing
runner_manager.register(
    PythonRunner(ProcessExecutor(), timeout=2.0)
)

runtime = ExecutionRuntime(
    runner_manager=runner_manager,
    sensor_manager=sensor_manager,
    workspace_manager=WorkspaceManager(),
    observation_bus=bus,
)


def run_pipeline_and_verify(asset_path: Path, expected_exit_code: int, expected_timeout: bool):
    # Retrieve path reference for checking cleanup
    workspace_mgr = runtime._workspace_manager

    session = runtime.execute(asset_path)

    # 1. Verify Outcome
    assert session.exit_code == expected_exit_code
    assert session.timed_out is expected_timeout
    assert session.duration_ms >= 0

    # 2. Verify Transcript & Hashing
    transcript = session.transcript
    assert transcript.context is not None
    assert TranscriptValidator.validate(transcript) is True

    t_hash = TranscriptHasher.hash(transcript)
    assert len(t_hash) == 64
    print(f"File: {asset_path.name} -> Hash: {t_hash}")

    # 3. Verify Workspace is removed
    assert workspace_mgr._directory is None


# Execute Regression Checks
run_pipeline_and_verify(Path("sandbox/samples/hello.py"), expected_exit_code=0, expected_timeout=False)
run_pipeline_and_verify(Path("sandbox/samples/infinite_loop.py"), expected_exit_code=-1, expected_timeout=True)

print("Regression Suite OK")
