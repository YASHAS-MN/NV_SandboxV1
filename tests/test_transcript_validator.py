from sandbox.behavior import (
    BehaviorTranscript,
    ObservationContext,
    TranscriptValidator,
)
from sandbox.core.events import Event

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="default",
    policy_version="1.0",
)

# 1. Valid Transcript
valid_transcript = BehaviorTranscript(
    context=context,
    event_count=2,
    events=[
        Event(sequence=1, sensor="test", event_type="A", relative_time_ms=0, payload={}),
        Event(sequence=2, sensor="test", event_type="B", relative_time_ms=10, payload={}),
    ]
)
assert TranscriptValidator.validate(valid_transcript) is True

# 2. Duplicate sequence raises ValueError
dup_transcript = BehaviorTranscript(
    context=context,
    event_count=2,
    events=[
        Event(sequence=1, sensor="test", event_type="A", relative_time_ms=0, payload={}),
        Event(sequence=1, sensor="test", event_type="B", relative_time_ms=10, payload={}),
    ]
)
try:
    TranscriptValidator.validate(dup_transcript)
    assert False, "Duplicate sequence should raise ValueError"
except ValueError:
    pass

# 3. Missing context raises ValueError
# Note: BehaviorTranscript type signature has context: ObservationContext,
# but we can pass None dynamically in Python to verify runtime assertions.
missing_ctx_transcript = BehaviorTranscript(
    context=None,  # type: ignore
    event_count=0,
    events=[]
)
try:
    TranscriptValidator.validate(missing_ctx_transcript)
    assert False, "Missing context should raise ValueError"
except ValueError:
    pass

# 4. Non-continuous sequence numbers raise ValueError
non_cont_transcript = BehaviorTranscript(
    context=context,
    event_count=2,
    events=[
        Event(sequence=1, sensor="test", event_type="A", relative_time_ms=0, payload={}),
        Event(sequence=3, sensor="test", event_type="B", relative_time_ms=10, payload={}),
    ]
)
try:
    TranscriptValidator.validate(non_cont_transcript)
    assert False, "Non-continuous sequence should raise ValueError"
except ValueError:
    pass

print("TranscriptValidator tests OK")
