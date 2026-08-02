"""
Nebula Labs

Asset Classification Models
"""

from __future__ import annotations

from dataclasses import dataclass

from sandbox.intake.asset_types import AssetCategory


@dataclass(frozen=True, slots=True)
class AssetClassification:
    """
    Result of the intake classifier.
    """

    category: AssetCategory

    subtype: str

    extension: str

    mime_type: str

    requires_execution: bool

    confidence: float
