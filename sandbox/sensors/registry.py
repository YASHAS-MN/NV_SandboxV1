"""
Nebula Labs

Sensor Registry
"""

from __future__ import annotations

from sandbox.sensors.base import Sensor


class SensorRegistry:

    def __init__(self) -> None:
        self._sensors: list[Sensor] = []

    def register(
        self,
        sensor: Sensor,
    ) -> None:
        self._sensors.append(sensor)

    def collect_all(
        self,
        recorder,
    ) -> None:

        for sensor in self._sensors:
            sensor.collect(recorder)

    @property
    def sensors(self):
        return tuple(self._sensors)
