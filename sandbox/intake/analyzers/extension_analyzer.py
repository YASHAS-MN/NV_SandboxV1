"""
Nebula Labs

Extension Analyzer

Collects evidence from the filename extension.

This component NEVER classifies the asset.
It only reports what it observes.
"""

from __future__ import annotations

from pathlib import Path

from sandbox.intake.evidence import ExtensionEvidence


class ExtensionAnalyzer:

    def analyze(
        self,
        asset: Path,
    ) -> ExtensionEvidence:

        return ExtensionEvidence(
            extension=asset.suffix.lower()
        )
