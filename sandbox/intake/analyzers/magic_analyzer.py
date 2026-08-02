"""
Nebula Labs

Magic Byte Analyzer

Collects magic bytes evidence from files.
"""

from __future__ import annotations

from pathlib import Path

from sandbox.intake.evidence.magic import MagicEvidence


class MagicAnalyzer:

    SIGNATURES = {
        "4d5a": "Windows PE (.exe)",
        "89504e47": "PNG",
        "25504446": "PDF",
        "504b0304": "ZIP / OOXML / APK / JAR",
    }

    def analyze(
        self,
        asset: Path,
    ) -> MagicEvidence:

        with open(asset, "rb") as f:
            signature = f.read(16)

        hex_sig = signature.hex().lower()
        matched = None

        for prefix, fmt in self.SIGNATURES.items():
            if hex_sig.startswith(prefix):
                matched = fmt
                break

        return MagicEvidence(
            signature=signature,
            hex_signature=hex_sig,
            matched_format=matched,
        )
