"""
Nebula Labs

Static Analysis Engine

Consumes StaticEvidence objects and produces
a deterministic StaticAnalysisResult.
"""

from __future__ import annotations

from sandbox.static_analysis.evidence import (
    StaticEvidence,
    HashEvidence,
    EntropyEvidence,
)

from sandbox.static_analysis.report.result import StaticAnalysisResult


class StaticAnalysisEngine:

    def analyze(
        self,
        evidence: list[StaticEvidence],
    ) -> StaticAnalysisResult:

        hash_evidence = None
        entropy_evidence = None

        for item in evidence:

            if isinstance(item, HashEvidence):
                hash_evidence = item

            elif isinstance(item, EntropyEvidence):
                entropy_evidence = item

        return self._evaluate(
            hash_evidence,
            entropy_evidence,
            evidence,
        )

    def _evaluate(
        self,
        hash_evidence: HashEvidence | None,
        entropy_evidence: EntropyEvidence | None,
        evidence: list[StaticEvidence],
    ) -> StaticAnalysisResult:

        findings: list[str] = []
        warnings: list[str] = []

        risk = "UNKNOWN"
        confidence = 0.0

        if hash_evidence:

            findings.append(
                "SHA-256 fingerprint calculated."
            )

            confidence += 0.25

        if entropy_evidence:

            confidence += 0.50

            if entropy_evidence.classification == "LOW":

                risk = "LOW"

            elif entropy_evidence.classification == "NORMAL":

                risk = "LOW"

            elif entropy_evidence.classification == "HIGH":

                risk = "MEDIUM"

                warnings.append(
                    "High entropy detected. Packed or encrypted content possible."
                )

        confidence = min(confidence, 1.0)

        return StaticAnalysisResult(
            risk_level=risk,
            confidence=confidence,
            evidence_used=evidence,
            findings=findings,
            warnings=warnings,
        )
