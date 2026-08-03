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

bus = ObservationBus()
sensor_manager = SensorManager()

runner_manager = RunnerManager()
# Register python runner with a short 1.0 second timeout for fast test execution
runner_manager.register(
    PythonRunner(ProcessExecutor(), timeout=1.0)
)

runtime = ExecutionRuntime(

    runner_manager=runner_manager,

    sensor_manager=sensor_manager,

    workspace_manager=WorkspaceManager(),

    observation_bus=bus,

)

session = runtime.execute(

    Path("sandbox/samples/infinite_loop.py")

)

print(session.to_dict())

assert session.timed_out is True

assert session.exit_code == -1
