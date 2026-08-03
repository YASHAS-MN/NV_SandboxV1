from pathlib import Path
from sandbox.runtime import (
    WorkspaceManager,
    ExecutionRuntime,
    RunnerManager,
)
from sandbox.runtime.runner import Runner
from sandbox.runtime.result import ExecutionResult
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors import SensorManager

workspace_path = None

class HookedRunner(Runner):
    @property
    def name(self):
        return "hooked"

    def supports(self, asset):
        return True

    def execute(self, asset, workspace):
        global workspace_path
        workspace_path = workspace.path
        assert workspace_path.exists()
        return ExecutionResult(exit_code=0, timed_out=False, duration_ms=10)

runner_manager = RunnerManager()
runner_manager.register(HookedRunner())

runtime = ExecutionRuntime(
    runner_manager=runner_manager,
    sensor_manager=SensorManager(),
    workspace_manager=WorkspaceManager(),
    observation_bus=ObservationBus(),
)

session = runtime.execute(Path("hello.py"))

# After execution, the workspace must be cleaned up and no longer exist
assert workspace_path is not None
assert not workspace_path.exists()

print("Workspace cleanup verified successfully")
