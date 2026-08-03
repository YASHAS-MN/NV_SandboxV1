from pathlib import Path

from sandbox.runtime import (
    PythonRunner,
    WorkspaceManager,
)
from sandbox.runtime.process_executor import (
    ProcessExecutor,
)

workspace = WorkspaceManager()

workspace.create()

runner = PythonRunner(

    ProcessExecutor(),

)

session = runner.execute(

    Path("sandbox/samples/hello.py"),

    workspace,

)

assert session.exit_code == 0

assert session.timed_out is False

assert session.duration_ms >= 0

assert session.transcript.event_count == 0

workspace.cleanup()

print(session.to_dict())
