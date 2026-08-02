from pathlib import Path
from sandbox.engine.execution_engine import ExecutionEngine
from sandbox.transcripts.serializer import TranscriptSerializer

engine = ExecutionEngine()
asset = Path("sandbox/samples/hello.py")
transcript = engine.execute(asset)
print(TranscriptSerializer.serialize(transcript))
