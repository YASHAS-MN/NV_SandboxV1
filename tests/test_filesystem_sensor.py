from pathlib import Path
import tempfile

from sandbox.behavior import ObservationContext, TranscriptBuilder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.filesystem_sensor import FilesystemSensor

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="default",
    policy_version="1.0",
)
builder = TranscriptBuilder(context)

bus = ObservationBus()
bus.set_builder(builder)
sensor = FilesystemSensor(bus)

with tempfile.TemporaryDirectory() as tmp:

    root = Path(tmp)

    before = sensor.snapshot(root)

    (root / "hello.txt").write_text("Nebula")

    after = sensor.snapshot(root)

    sensor.before_execution()
    sensor.observe(before, after)
    sensor.after_execution()

transcript = builder.build()
print(transcript.to_dict())

assert sensor.name == "filesystem"
assert transcript.event_count == 1
