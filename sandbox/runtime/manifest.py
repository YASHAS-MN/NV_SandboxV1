"""
Nebula Labs

Workspace Manifest
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WorkspaceManifest:
    """
    Describes the isolated execution workspace.
    """

    root: Path
    asset: Path

    def to_dict(self):

        return {
            "root": str(self.root),
            "asset": str(self.asset),
        }
