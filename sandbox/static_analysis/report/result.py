"""
Nebula Labs

Static Analysis Result Protocol
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.static_analysis.evidence import StaticEvidence


@dataclass(frozen=True, slots=True)
class StaticAnalysisResult:

    risk_level: str

    confidence: float

    evidence_used: list[StaticEvidence] = field(default_factory=list)

    findings: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    def to_dict(self):

        return {

            "risk_level": self.risk_level,

            "confidence": self.confidence,

            "evidence_used": [
                e.to_dict()
                for e in self.evidence_used
            ],

            "findings": self.findings,

            "warnings": self.warnings,

        }
