"""
Nebula Labs
Canonical Transcript Serializer

Responsible for:
- Canonical event ordering
- Stable JSON serialization
"""

from __future__ import annotations

import json
from typing import Any


class TranscriptSerializer:

    @staticmethod
    def serialize(events: list[dict[str, Any]]) -> str:
        """
        Produce canonical JSON.

        Rules
        -----
        - sequence sorted
        - UTF-8 compatible
        - deterministic key ordering
        """

        ordered = sorted(
            events,
            key=lambda event: event["sequence"],
        )

        return json.dumps(
            ordered,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
