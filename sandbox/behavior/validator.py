from __future__ import annotations

from sandbox.behavior.transcript import BehaviorTranscript


class TranscriptValidator:

    @staticmethod
    def validate(
        transcript: BehaviorTranscript,
    ) -> bool:

        if transcript.context is None:
            raise ValueError("Observation context is missing.")

        if transcript.event_count != len(transcript.events):
            raise ValueError(
                f"Event count mismatch: count is {transcript.event_count}, but list length is {len(transcript.events)}"
            )

        sequences = [event.sequence for event in transcript.events]

        if len(sequences) != len(set(sequences)):
            raise ValueError("Duplicate sequence numbers found.")

        # If there are events, check that they form a continuous sequence from 1 to N
        if sequences:
            sorted_sequences = sorted(sequences)
            if sorted_sequences[0] != 1 or sorted_sequences[-1] != len(sequences):
                raise ValueError("Sequence numbers are not continuous from 1 to N.")
            for i, seq in enumerate(sorted_sequences):
                if seq != i + 1:
                    raise ValueError("Sequence numbers are not continuous from 1 to N.")

        return True
