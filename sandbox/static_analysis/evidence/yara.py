"""
Nebula Labs

YARA Evidence
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sandbox.static_analysis.evidence.base import StaticEvidence


@dataclass(frozen=True, slots=True)
class YaraEvidence(StaticEvidence):

    matched_rules: list[str] = field(default_factory=list)

    match_count: int = 0

    def __init__(
        self,
        matched_rules: list[str],
    ):
        object.__setattr__(self, "analyzer", "yara")

        object.__setattr__(self, "matched_rules", matched_rules)

        object.__setattr__(self, "match_count", len(matched_rules))

    def to_dict(self):

        return {

            "analyzer": self.analyzer,

            "matched_rules": self.matched_rules,

            "match_count": self.match_count,

        }
