from pathlib import Path
import tempfile

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.filesystem_sensor import FilesystemSensor

recorder = BehaviorRecorder()
bus = ObservationBus(recorder)
sensor = FilesystemSensor(bus)

with tempfile.TemporaryDirectory() as tmp:

    root = Path(tmp)

    before = sensor.snapshot(root)

    (root / "hello.txt").write_text("Nebula")

    after = sensor.snapshot(root)

    sensor.before_execution()
    sensor.observe(before, after)
    sensor.after_execution()

print(recorder.export().to_dict())

assert sensor.name == "filesystem"
assert recorder.event_count == 1
