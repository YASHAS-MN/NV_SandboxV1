"""
Nebula Labs

Magic Byte Evidence
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sandbox.intake.evidence.base import Evidence


@dataclass(frozen=True, slots=True)
class MagicEvidence(Evidence):

    signature: bytes
    hex_signature: str
    matched_format: str | None

    def __init__(
        self,
        *,
        signature: bytes,
        hex_signature: str,
        matched_format: str | None,
    ) -> None:
        object.__setattr__(self, "analyzer", "magic")
        object.__setattr__(self, "signature", signature)
        object.__setattr__(self, "hex_signature", hex_signature)
        object.__setattr__(self, "matched_format", matched_format)

    def to_dict(self) -> dict[str, Any]:
        return {
            "analyzer": self.analyzer,
            "signature": self.hex_signature,
            "matched_format": self.matched_format,
        }
