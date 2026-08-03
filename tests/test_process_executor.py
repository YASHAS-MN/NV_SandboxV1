import sys
from pathlib import Path

from sandbox.runtime.process_executor import (
    ProcessExecutor,
)

executor = ProcessExecutor()

result = executor.execute(

    [
        sys.executable,
        "-c",
        "print('hello')",
    ],

    cwd=Path.cwd(),

)

assert result.returncode == 0

assert b"hello" in result.stdout

print("ProcessExecutor OK")
