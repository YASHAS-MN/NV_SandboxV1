"""
Nebula Labs

Canonical Asset Categories
"""

from __future__ import annotations

from enum import Enum


class AssetCategory(str, Enum):

    EXECUTABLE = "EXECUTABLE"

    SCRIPT = "SCRIPT"

    DOCUMENT = "DOCUMENT"

    IMAGE = "IMAGE"

    AUDIO = "AUDIO"

    VIDEO = "VIDEO"

    ARCHIVE = "ARCHIVE"

    DATA = "DATA"

    UNKNOWN = "UNKNOWN"
