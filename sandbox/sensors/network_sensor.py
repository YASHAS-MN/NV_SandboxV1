"""
Nebula Labs

Network Sensor

Observes network connection attempts made during execution.

Strategy
--------
Before execution begins, a `sitecustomize.py` shim is written
into the workspace directory. Python automatically imports any
`sitecustomize.py` on the PYTHONPATH before user code runs,
allowing us to monkey-patch `socket.socket.connect` to log all
outbound connection attempts to a JSON sidecar file.

After execution completes, the sensor reads the sidecar log,
translates each record into a NETWORK_CONNECT event, and publishes
it to the ObservationBus. The shim and sidecar are then removed.

Scope
-----
This captures Python-level socket calls only. Native binary
connections bypass this layer entirely (by design — we do not
run native binaries in this sandbox).
"""

from __future__ import annotations

import json
from pathlib import Path

from sandbox.sensors.base import Sensor
from sandbox.observation.observation_bus import ObservationBus
from sandbox.core.event_types import EventType


# Name of the sidecar log written by the shim
_SIDECAR_NAME = ".nebula_network_log.json"

# The shim injected into the workspace as sitecustomize.py
# It monkey-patches socket.socket.connect at import time so every
# subsequent socket call by user code is logged.
_SHIM_TEMPLATE = """\
# Nebula Network Sensor Shim — injected by sandbox
import socket as _socket
import json as _json
import os as _os

_SIDECAR = _os.path.join(_os.path.dirname(__file__), "{sidecar}")
_orig_connect = _socket.socket.connect

def _patched_connect(self, address):
    record = {{
        "host": address[0] if isinstance(address, (tuple, list)) else str(address),
        "port": address[1] if isinstance(address, (tuple, list)) and len(address) > 1 else None,
        "family": self.family.name if hasattr(self.family, "name") else str(self.family),
    }}
    try:
        existing = _json.loads(open(_SIDECAR).read()) if _os.path.exists(_SIDECAR) else []
    except Exception:
        existing = []
    existing.append(record)
    with open(_SIDECAR, "w") as _f:
        _json.dump(existing, _f)
    return _orig_connect(self, address)

_socket.socket.connect = _patched_connect
"""


class NetworkSensor(Sensor):

    def __init__(
        self,
        bus: ObservationBus,
        workspace_path: Path | None = None,
    ) -> None:
        self._bus = bus
        self._workspace_path: Path | None = workspace_path
        self._connections: list[dict] = []

    @property
    def name(self) -> str:
        return "network"

    @property
    def priority(self) -> int:
        # Run before ProcessSensor (priority 100) so shim is
        # in place before the process starts.
        return 10

    def attach(self, workspace_path: Path) -> None:
        """
        Called by the runtime to bind this sensor to the active
        workspace directory before before_execution() is invoked.
        """
        self._workspace_path = workspace_path

    def before_execution(self) -> None:
        self._connections.clear()

        if self._workspace_path is None:
            return

        shim_content = _SHIM_TEMPLATE.format(sidecar=_SIDECAR_NAME)
        shim_path = self._workspace_path / "sitecustomize.py"
        shim_path.write_text(shim_content, encoding="utf-8")

    def after_execution(self) -> None:
        if self._workspace_path is None:
            return

        sidecar = self._workspace_path / _SIDECAR_NAME
        if sidecar.exists():
            try:
                records = json.loads(sidecar.read_text(encoding="utf-8"))
                self._connections = records if isinstance(records, list) else []
            except Exception:
                self._connections = []
            sidecar.unlink(missing_ok=True)

        shim = self._workspace_path / "sitecustomize.py"
        shim.unlink(missing_ok=True)

        for record in self._connections:
            self._bus.publish(
                sensor=self.name,
                event_type=EventType.NETWORK_CONNECT,
                payload={
                    "host": record.get("host", "unknown"),
                    "port": record.get("port"),
                    "family": record.get("family", "unknown"),
                },
            )

        self._connections.clear()
        self._workspace_path = None
