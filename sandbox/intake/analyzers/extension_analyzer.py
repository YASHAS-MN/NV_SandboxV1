"""
Nebula Labs

Extension Analyzer

Collects evidence from the filename extension.

This component NEVER classifies the asset.
It only reports what it observes.
"""

from __future__ import annotations

from pathlib import Path


class ExtensionAnalyzer:

    def analyze(
        self,
        asset: Path,
    ) -> dict:

        return {
            "extension": asset.suffix.lower(),
        }
