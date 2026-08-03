from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType
from sandbox.behavior import ObservationContext, TranscriptBuilder

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="default",
    policy_version="1.0",
)
builder = TranscriptBuilder(context)

bus = ObservationBus()
bus.set_builder(builder)

bus.publish(
    sensor="filesystem",
    event_type=EventType.FILE_CREATE,
    payload={
        "path": "demo.txt",
    },
)

transcript = builder.build()
print(transcript.to_dict())

assert transcript.event_count == 1
assert transcript.events[0].sensor == "filesystem"
assert transcript.events[0].payload == {"path": "demo.txt"}
