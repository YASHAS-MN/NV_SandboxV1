"""
Nebula Labs

Canonical Static Analysis Evidence Protocol
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StaticEvidence(ABC):
    """
    Base protocol artifact for every static analyzer.
    """

    analyzer: str

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError
