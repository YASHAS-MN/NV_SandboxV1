from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObservationContext:
    """
    Canonical execution context shared by all validators.
    """

    protocol_version: str

    runtime_profile: str

    observation_profile: str

    policy_version: str

    def to_dict(self):

        return {

            "protocol_version": self.protocol_version,

            "runtime_profile": self.runtime_profile,

            "observation_profile": self.observation_profile,

            "policy_version": self.policy_version,

        }
