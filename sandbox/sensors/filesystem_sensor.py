"""
Nebula Labs

Filesystem Sensor

Observes filesystem mutations between two snapshots.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from sandbox.sensors.base import Sensor
from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType


class FilesystemSensor(Sensor):

    def __init__(
        self,
        bus: ObservationBus,
    ) -> None:

        self._bus = bus
        self._created_files: list[tuple[str, str]] = []
        self._deleted_files: list[str] = []
        self._modified_files: list[tuple[str, str, str]] = []

    @property
    def name(self) -> str:
        return "filesystem"

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

    def before_execution(self) -> None:

        self._created_files.clear()
        self._deleted_files.clear()
        self._modified_files.clear()

    def observe(
        self,
        before: dict[str, str],
        after: dict[str, str],
    ) -> None:

        before_files = set(before)
        after_files = set(after)

        created = after_files - before_files
        deleted = before_files - after_files
        common = before_files & after_files

        for file in sorted(created):
            self._created_files.append((file, after[file]))

        for file in sorted(deleted):
            self._deleted_files.append(file)

        for file in sorted(common):
            if before[file] != after[file]:
                self._modified_files.append((file, before[file], after[file]))

    def after_execution(self) -> None:

        for file, sha256 in self._created_files:

            self._bus.publish(
                sensor=self.name,
                event_type=EventType.FILE_CREATE,
                payload={
                    "path": file,
                    "sha256": sha256,
                },
            )

        for file in self._deleted_files:

            self._bus.publish(
                sensor=self.name,
                event_type=EventType.FILE_DELETE,
                payload={
                    "path": file,
                },
            )

        for file, old_hash, new_hash in self._modified_files:

            self._bus.publish(
                sensor=self.name,
                event_type=EventType.FILE_MODIFY,
                payload={
                    "path": file,
                    "old_hash": old_hash,
                    "new_hash": new_hash,
                },
            )

        self._created_files.clear()
        self._deleted_files.clear()
        self._modified_files.clear()
