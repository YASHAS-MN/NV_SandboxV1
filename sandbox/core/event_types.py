"""
Nebula Labs

Canonical Event Taxonomy (CBTS v1)

Every observable event in Nebula must originate
from this file.

Never hardcode event names elsewhere.
"""

from __future__ import annotations

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum
    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return str(self.value)


class EventType(StrEnum):

    # -------------------------
    # Engine
    # -------------------------

    EXECUTION_START = "EXECUTION_START"
    EXECUTION_END = "EXECUTION_END"

    # -------------------------
    # Process
    # -------------------------

    PROCESS_START = "PROCESS_START"
    PROCESS_EXIT = "PROCESS_EXIT"
    PROCESS_SPAWN = "PROCESS_SPAWN"

    # -------------------------
    # Filesystem
    # -------------------------

    FILE_CREATE = "FILE_CREATE"
    FILE_DELETE = "FILE_DELETE"
    FILE_MODIFY = "FILE_MODIFY"

    # -------------------------
    # Network
    # -------------------------

    NETWORK_CONNECT = "NETWORK_CONNECT"
    DNS_QUERY = "DNS_QUERY"
    HTTP_REQUEST = "HTTP_REQUEST"

    # -------------------------
    # Registry
    # -------------------------

    REGISTRY_READ = "REGISTRY_READ"
    REGISTRY_WRITE = "REGISTRY_WRITE"

    # -------------------------
    # Memory
    # -------------------------

    MEMORY_ALLOC = "MEMORY_ALLOC"
    MEMORY_FREE = "MEMORY_FREE"
