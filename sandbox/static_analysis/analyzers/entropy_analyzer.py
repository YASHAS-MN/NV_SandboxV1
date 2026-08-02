"""
Nebula Labs

Entropy Analyzer

Computes Shannon entropy of an asset.
"""

from __future__ import annotations

import math
from pathlib import Path

from sandbox.static_analysis.evidence import EntropyEvidence


class EntropyAnalyzer:

    LOW_THRESHOLD = 5.0
    HIGH_THRESHOLD = 7.2

    def analyze(
        self,
        asset: Path,
    ) -> EntropyEvidence:

        data = asset.read_bytes()

        entropy = self._calculate_entropy(data)

        if entropy < self.LOW_THRESHOLD:
            classification = "LOW"

        elif entropy >= self.HIGH_THRESHOLD:
            classification = "HIGH"

        else:
            classification = "NORMAL"

        return EntropyEvidence(
            entropy=round(entropy, 4),
            sample_size=len(data),
            classification=classification,
        )

    def _calculate_entropy(
        self,
        data: bytes,
    ) -> float:

        if not data:
            return 0.0

        frequencies = [0] * 256

        for byte in data:
            frequencies[byte] += 1

        entropy = 0.0

        length = len(data)

        for count in frequencies:

            if count == 0:
                continue

            probability = count / length

            entropy -= probability * math.log2(probability)

        return entropy
