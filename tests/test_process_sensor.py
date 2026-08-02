from subprocess import CompletedProcess

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.sensors.process_sensor import ProcessSensor


sensor = ProcessSensor()
recorder = BehaviorRecorder()

completed = CompletedProcess(
    args=["python"],
    returncode=0,
    stdout="hello",
    stderr="",
)

sensor.collect(
    completed,
    recorder,
)

print(
    recorder.export().to_dict()
)
