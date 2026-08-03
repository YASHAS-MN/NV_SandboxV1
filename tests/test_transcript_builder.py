from sandbox.behavior import (
    BehaviorTranscript,
    ObservationContext,
    TranscriptBuilder,
)
from sandbox.core.events import Event

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="filesystem-process-v1",
    policy_version="1.0",
)

builder = TranscriptBuilder(context)

builder.append(
    Event(
        sequence=1,
        sensor="process",
        event_type="PROCESS_START",
        relative_time_ms=0,
        payload={"pid": 123},
    )
)

builder.append(
    Event(
        sequence=2,
        sensor="filesystem",
        event_type="FILE_CREATE",
        relative_time_ms=5,
        payload={"path": "hello.txt"},
    )
)

transcript = builder.build()

print(transcript.to_dict())

assert transcript.event_count == 2
assert len(transcript.events) == 2
assert transcript.context == context

# Verify reset works
builder.reset()
assert len(builder.build().events) == 0
