from pathlib import Path

from sandbox.runtime import (
    ExecutionRuntime,
    WorkspaceManager,
    RunnerManager,
    PythonRunner,
)

from sandbox.runtime.process_executor import ProcessExecutor

from sandbox.observation.observation_bus import ObservationBus

from sandbox.sensors import (
    SensorManager,
)

from sandbox.sensors.process_sensor import ProcessSensor
from sandbox.sensors.filesystem_sensor import FilesystemSensor


bus = ObservationBus()

sensor_manager = SensorManager()

sensor_manager.register(

    ProcessSensor(bus)

)

sensor_manager.register(

    FilesystemSensor(bus)

)

runner_manager = RunnerManager()

runner_manager.register(

    PythonRunner(

        ProcessExecutor()

    )

)

runtime = ExecutionRuntime(

    runner_manager=runner_manager,

    sensor_manager=sensor_manager,

    workspace_manager=WorkspaceManager(),

    observation_bus=bus,

)

session = runtime.execute(

    Path("sandbox/samples/hello.py")

)

assert session.exit_code == 0

assert session.duration_ms >= 0

assert session.transcript.context is not None

print(session.to_dict())
