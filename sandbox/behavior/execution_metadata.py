from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionMetadata:
    """
    Runtime information accompanying a transcript.
    Not part of the canonical hash.
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
