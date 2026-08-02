"""
Nebula Labs

SHA256 Analyzer
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from sandbox.static_analysis.evidence import HashEvidence


class HashAnalyzer:

    CHUNK_SIZE = 1024 * 1024

    def analyze(
        self,
        asset: Path,
    ) -> HashEvidence:

        hasher = hashlib.sha256()

        with asset.open("rb") as file:

            while True:

                chunk = file.read(self.CHUNK_SIZE)

                if not chunk:
                    break

                hasher.update(chunk)

        return HashEvidence(
            algorithm="sha256",
            digest=hasher.hexdigest(),
            file_size=asset.stat().st_size,
        )
