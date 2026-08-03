from sandbox.behavior import BehaviorTranscript

from sandbox.core.events import Event

transcript = BehaviorTranscript(

    protocol_version="1.0",

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
