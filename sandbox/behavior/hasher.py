import hashlib
import json

from sandbox.behavior.transcript import BehaviorTranscript


class TranscriptHasher:

    @staticmethod
    def hash(
        transcript: BehaviorTranscript,
    ) -> str:

        ordered = sorted(
            transcript.canonical_dict(),
            key=lambda event: event["sequence"],
        )

        serialized = json.dumps(
            ordered,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        return hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()
