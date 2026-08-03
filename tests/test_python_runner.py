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

result = runner.execute(

    Path("sandbox/samples/hello.py"),

    workspace,

)

assert result.exit_code == 0

assert result.timed_out is False

assert result.duration_ms >= 0

workspace.cleanup()

print(result.to_dict())
