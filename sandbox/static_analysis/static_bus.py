"""
Nebula Labs

Static Evidence Bus

Receives evidence produced by static analyzers.
"""

from __future__ import annotations

from sandbox.static_analysis.evidence import StaticEvidence


class StaticEvidenceBus:

    def __init__(self) -> None:

        self._evidence: list[StaticEvidence] = []

    def publish(
        self,
        evidence: StaticEvidence,
    ) -> None:

        self._evidence.append(evidence)

    def snapshot(
        self,
    ) -> list[StaticEvidence]:

        return self._evidence.copy()

    def clear(self) -> None:

        self._evidence.clear()
