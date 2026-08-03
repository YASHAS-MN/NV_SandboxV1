from __future__ import annotations

from dataclasses import dataclass

from sandbox.behavior import BehaviorTranscript


@dataclass(frozen=True, slots=True)
class ExecutionSession:
    """
    Represents one completed execution of an asset.
    """

    transcript: BehaviorTranscript

    exit_code: int

    timed_out: bool

    duration_ms: int

    def to_dict(self):

        return {

            "transcript": self.transcript.to_dict(),

            "exit_code": self.exit_code,

            "timed_out": self.timed_out,

            "duration_ms": self.duration_ms,

        }
