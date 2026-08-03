from subprocess import CompletedProcess

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.process_sensor import ProcessSensor

recorder = BehaviorRecorder()
bus = ObservationBus(recorder)
sensor = ProcessSensor(bus)

completed = CompletedProcess(
    args=["python"],
    returncode=0,
    stdout="hello",
    stderr="",
)

sensor.before_execution()
sensor.observe(completed)
sensor.after_execution()

print(
    recorder.export().to_dict()
)

assert sensor.name == "process"
assert recorder.event_count == 1
