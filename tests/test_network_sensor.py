from pathlib import Path

from sandbox.runtime import (
    ExecutionRuntime,
    WorkspaceManager,
    RunnerManager,
    PythonRunner,
)
from sandbox.runtime.process_executor import ProcessExecutor
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.manager import SensorManager
from sandbox.sensors.process_sensor import ProcessSensor
from sandbox.sensors.filesystem_sensor import FilesystemSensor
from sandbox.sensors.network_sensor import NetworkSensor
from sandbox.core.event_types import EventType

bus = ObservationBus()
sensor_manager = SensorManager()
sensor_manager.register(NetworkSensor(bus))
sensor_manager.register(ProcessSensor(bus))
sensor_manager.register(FilesystemSensor(bus))

runner_manager = RunnerManager()
runner_manager.register(PythonRunner(ProcessExecutor(), timeout=5.0))

runtime = ExecutionRuntime(
    runner_manager=runner_manager,
    sensor_manager=sensor_manager,
    workspace_manager=WorkspaceManager(),
    observation_bus=bus,
)

session = runtime.execute(Path("sandbox/samples/phone_home.py"))
transcript = session.transcript

print("Events recorded:", transcript.event_count)
for event in transcript.events:
    print(f"  [{event.sequence}] {event.event_type} — {event.payload}")

network_events = [
    e for e in transcript.events
    if e.event_type == EventType.NETWORK_CONNECT
]

assert len(network_events) >= 1, "Expected at least one NETWORK_CONNECT event"
assert network_events[0].payload["host"] == "93.184.216.34"
assert network_events[0].payload["port"] == 80
assert network_events[0].sensor == "network"

print("NetworkSensor test OK")
