from pathlib import Path

from sandbox.engine.execution_engine import ExecutionEngine
from sandbox.transcripts.serializer import TranscriptSerializer


engine = ExecutionEngine()

asset = Path("sandbox/samples/hello.py")

hashes = []

for i in range(10):

    transcript = engine.execute(asset)

    serialized = TranscriptSerializer.serialize(
        transcript
    )

    hashes.append(serialized)

print()

print("Unique transcripts:", len(set(hashes)))

assert len(set(hashes)) == 1
