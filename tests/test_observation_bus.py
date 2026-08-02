from sandbox.behavior.behavior_recorder import BehaviorRecorder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType

recorder = BehaviorRecorder()

bus = ObservationBus(recorder)

bus.publish(
    sensor="filesystem",
    event_type=EventType.FILE_CREATE,
    payload={
        "path": "demo.txt",
    },
)

transcript = recorder.export()

print(transcript.to_dict())
