"""
Nebula Labs

Evidence Bus

Receives evidence from intake analyzers.

The Classification Engine is the only
consumer of this evidence.
"""

from __future__ import annotations

from sandbox.intake.evidence import Evidence


class EvidenceBus:

    def __init__(self) -> None:

        self._evidence: list[Evidence] = []

    def publish(
        self,
        evidence: Evidence,
    ) -> None:

        self._evidence.append(evidence)

    def snapshot(self) -> list[Evidence]:
        """
        Immutable copy of all collected evidence.
        """

        return self._evidence.copy()

    def clear(self) -> None:

        self._evidence.clear()
