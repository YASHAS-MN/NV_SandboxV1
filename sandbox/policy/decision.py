"""
Nebula Labs

Execution Policy Decision Protocol
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ExecutionAction(str, Enum):
    COMPLETE = "COMPLETE"
    CONTINUE = "CONTINUE"
    REJECT = "REJECT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


@dataclass(frozen=True, slots=True)
class ExecutionDecision:
    """
    Canonical output of the Execution Policy Engine.
    """

    action: ExecutionAction

    next_gateway: str | None

    reason: str

    warnings: list[str] = field(default_factory=list)

    def to_dict(self):

        return {

            "action": self.action.value,

            "next_gateway": self.next_gateway,

            "reason": self.reason,

            "warnings": self.warnings,

        }
