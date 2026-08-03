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

from sandbox.behavior.transcript import BehaviorTranscript


class TranscriptSerializer:

    @staticmethod
    def serialize(
        transcript: BehaviorTranscript,
    ) -> str:
        """
        Produce canonical JSON.

        Rules
        -----
        - sequence sorted
        - UTF-8 compatible
        - deterministic key ordering
        """

        ordered = sorted(
            transcript.canonical_dict(),
            key=lambda event: event["sequence"],
        )

        return json.dumps(
            ordered,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
