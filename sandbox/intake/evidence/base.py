"""
Nebula Labs

Canonical Evidence Protocol
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Evidence(ABC):
    """
    Base protocol artifact for all intake evidence.
    """

    analyzer: str

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError
