from sandbox.behavior import (
    BehaviorTranscript,
    ObservationContext,
    TranscriptHasher,
)
from sandbox.core.events import Event

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="default",
    policy_version="1.0",
)

# Transcript 1
t1 = BehaviorTranscript(
    context=context,
    event_count=1,
    events=[
        Event(sequence=1, sensor="test", event_type="A", relative_time_ms=10, payload={"val": 1}),
    ]
)

# Transcript 2: Same, but different relative_time_ms
t2 = BehaviorTranscript(
    context=context,
    event_count=1,
    events=[
        Event(sequence=1, sensor="test", event_type="A", relative_time_ms=999, payload={"val": 1}),
    ]
)

# Transcript 3: Different payload
t3 = BehaviorTranscript(
    context=context,
    event_count=1,
    events=[
        Event(sequence=1, sensor="test", event_type="A", relative_time_ms=10, payload={"val": 2}),
    ]
)

hash1 = TranscriptHasher.hash(t1)
hash2 = TranscriptHasher.hash(t2)
hash3 = TranscriptHasher.hash(t3)

print("Hash 1:", hash1)
print("Hash 2:", hash2)
print("Hash 3:", hash3)

assert hash1 == hash2, "Same canonical data with different metadata must have the same hash"
assert hash1 != hash3, "Different payloads must result in different hashes"

print("TranscriptHasher tests OK")
