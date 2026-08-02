"""
Nebula Labs

Extension Evidence
"""

from __future__ import annotations

from dataclasses import dataclass

from sandbox.intake.evidence.base import Evidence


@dataclass(frozen=True, slots=True)
class ExtensionEvidence(Evidence):

    extension: str

    def __init__(self, extension: str):
        object.__setattr__(self, "analyzer", "extension")
        object.__setattr__(self, "extension", extension)

    def to_dict(self):

        return {
            "analyzer": self.analyzer,
            "extension": self.extension,
        }
