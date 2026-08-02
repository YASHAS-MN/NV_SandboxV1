from subprocess import CompletedProcess

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.process_sensor import ProcessSensor


sensor = ProcessSensor()
recorder = BehaviorRecorder()
bus = ObservationBus(recorder)

completed = CompletedProcess(
    args=["python"],
    returncode=0,
    stdout="hello",
    stderr="",
)

sensor.collect(
    completed,
    bus,
)

print(
    recorder.export().to_dict()
)
