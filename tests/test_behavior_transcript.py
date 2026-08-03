from sandbox.behavior import BehaviorTranscript, ObservationContext

from sandbox.core.events import Event

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="filesystem-process-v1",
    policy_version="1.0",
)

transcript = BehaviorTranscript(

    context=context,

    event_count=2,

    events=[

        Event(
            sequence=1,
            sensor="process",
            event_type="PROCESS_START",
            relative_time_ms=0,
            payload={"pid": 123},
        ),

        Event(
            sequence=2,
            sensor="filesystem",
            event_type="FILE_CREATE",
            relative_time_ms=4,
            payload={"path": "artifact.txt"},
        ),

    ],

)

print(transcript.to_dict())

assert transcript.event_count == 2
