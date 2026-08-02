"""
Nebula Labs

Entropy Evidence
"""

from __future__ import annotations

from dataclasses import dataclass

from sandbox.static_analysis.evidence.base import StaticEvidence


@dataclass(frozen=True, slots=True)
class EntropyEvidence(StaticEvidence):

    entropy: float

    sample_size: int

    classification: str

    def __init__(
        self,
        entropy: float,
        sample_size: int,
        classification: str,
    ):
        object.__setattr__(self, "analyzer", "entropy")

        object.__setattr__(self, "entropy", entropy)

        object.__setattr__(self, "sample_size", sample_size)

        object.__setattr__(self, "classification", classification)

    def to_dict(self):

        return {

            "analyzer": self.analyzer,

            "entropy": self.entropy,

            "sample_size": self.sample_size,

            "classification": self.classification,

        }
