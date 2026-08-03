from sandbox.behavior import BehaviorTranscript, ObservationContext
from sandbox.runtime import ExecutionSession

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="filesystem-process-v1",
    policy_version="1.0",
)

transcript = BehaviorTranscript(
    context=context,
    event_count=0,
    events=[],
)

session = ExecutionSession(
    transcript=transcript,
    exit_code=0,
    timed_out=False,
    duration_ms=120,
)

print(session.to_dict())

assert session.exit_code == 0
assert session.timed_out is False
assert session.duration_ms == 120
assert session.transcript == transcript
