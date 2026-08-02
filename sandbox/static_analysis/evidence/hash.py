"""
Nebula Labs

SHA-256 Evidence
"""

from __future__ import annotations

from dataclasses import dataclass

from sandbox.static_analysis.evidence.base import StaticEvidence


@dataclass(frozen=True, slots=True)
class HashEvidence(StaticEvidence):

    algorithm: str

    digest: str

    file_size: int

    def __init__(
        self,
        algorithm: str,
        digest: str,
        file_size: int,
    ):
        object.__setattr__(self, "analyzer", "hash")

        object.__setattr__(self, "algorithm", algorithm)

        object.__setattr__(self, "digest", digest)

        object.__setattr__(self, "file_size", file_size)

    def to_dict(self):

        return {

            "analyzer": self.analyzer,

            "algorithm": self.algorithm,

            "digest": self.digest,

            "file_size": self.file_size,

        }
