"""
Nebula Labs

Filesystem Sensor

Observes filesystem mutations between two snapshots.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType


class FilesystemSensor:

    name = "filesystem"

    def snapshot(
        self,
        root: Path,
    ) -> dict[str, str]:

        state = {}

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            relative = str(file.relative_to(root))

            digest = hashlib.sha256(
                file.read_bytes()
            ).hexdigest()

            state[relative] = digest

        return state

    def collect(
        self,
        before: dict[str, str],
        after: dict[str, str],
        bus: ObservationBus,
    ) -> None:

        before_files = set(before)
        after_files = set(after)

        created = after_files - before_files
        deleted = before_files - after_files

        common = before_files & after_files

        for file in sorted(created):

            bus.publish(
                sensor=self.name,
                event_type=EventType.FILE_CREATE,
                payload={
                    "path": file,
                    "sha256": after[file],
                },
            )

        for file in sorted(deleted):

            bus.publish(
                sensor=self.name,
                event_type=EventType.FILE_DELETE,
                payload={
                    "path": file,
                },
            )

        for file in sorted(common):

            if before[file] != after[file]:

                bus.publish(
                    sensor=self.name,
                    event_type=EventType.FILE_MODIFY,
                    payload={
                        "path": file,
                        "old_hash": before[file],
                        "new_hash": after[file],
                    },
                )
