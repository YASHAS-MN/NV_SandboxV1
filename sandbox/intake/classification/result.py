"""
Nebula Labs

Classification Result Protocol
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.intake.evidence import Evidence
from sandbox.intake.asset_types import AssetCategory


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """
    Canonical output of the Classification Engine.

    This object represents Nebula's understanding of the
    asset identity based on available evidence.
    """

    category: AssetCategory

    confidence: float

    evidence_used: list[Evidence] = field(default_factory=list)

    conflicts: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:

        return {

            "category": self.category.value,

            "confidence": self.confidence,

            "evidence_used": [
                e.to_dict()
                for e in self.evidence_used
            ],

            "conflicts": self.conflicts,

            "warnings": self.warnings,

        }
