from pathlib import Path
import tempfile

from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.filesystem_sensor import FilesystemSensor


sensor = FilesystemSensor()
recorder = BehaviorRecorder()
bus = ObservationBus(recorder)

with tempfile.TemporaryDirectory() as tmp:

    root = Path(tmp)

    before = sensor.snapshot(root)

    (root / "hello.txt").write_text("Nebula")

    after = sensor.snapshot(root)

    sensor.collect(
        before,
        after,
        bus,
    )

print(recorder.export().to_dict())
