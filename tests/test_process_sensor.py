from subprocess import CompletedProcess

from sandbox.behavior import ObservationContext, TranscriptBuilder
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.process_sensor import ProcessSensor

context = ObservationContext(
    protocol_version="1.0",
    runtime_profile="python-runtime-v1",
    observation_profile="default",
    policy_version="1.0",
)
builder = TranscriptBuilder(context)

bus = ObservationBus()
bus.set_builder(builder)
sensor = ProcessSensor(bus)

completed = CompletedProcess(
    args=["python"],
    returncode=0,
    stdout="hello",
    stderr="",
)

sensor.before_execution()
sensor.observe(completed)
sensor.after_execution()

transcript = builder.build()
print(transcript.to_dict())

assert sensor.name == "process"
assert transcript.event_count == 1
