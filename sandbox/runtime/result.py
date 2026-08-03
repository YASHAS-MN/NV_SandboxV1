from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """
    Lightweight outcome of executing an asset.
    """

    exit_code: int

    timed_out: bool

    duration_ms: int

    def to_dict(self):

        return {

            "exit_code": self.exit_code,

            "timed_out": self.timed_out,

            "duration_ms": self.duration_ms,

        }
