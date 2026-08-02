"""
Nebula Labs

Canonical Asset Categories
"""

from __future__ import annotations

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum
    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return str(self.value)


class AssetCategory(StrEnum):

    EXECUTABLE = "EXECUTABLE"

    SCRIPT = "SCRIPT"

    DOCUMENT = "DOCUMENT"

    IMAGE = "IMAGE"

    AUDIO = "AUDIO"

    VIDEO = "VIDEO"

    ARCHIVE = "ARCHIVE"

    DATA = "DATA"

    UNKNOWN = "UNKNOWN"
