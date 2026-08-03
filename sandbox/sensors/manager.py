"""
Nebula Labs

Sensor Manager
"""

from __future__ import annotations

from sandbox.sensors.base import Sensor


class SensorManager:
    """
    Coordinates all registered sensors.

    Responsible for:
    - registration
    - execution ordering
    - lifecycle dispatch

    Not responsible for:
    - execution
    - observation
    - transcript construction
    """

    def __init__(self) -> None:

        self._sensors: list[Sensor] = []

    def register(
        self,
        sensor: Sensor,
    ) -> None:

        self._sensors.append(sensor)

        self._sensors.sort(
            key=lambda sensor: sensor.priority
        )

    def unregister(
        self,
        sensor: Sensor,
    ) -> None:

        self._sensors.remove(sensor)

    def clear(self) -> None:

        self._sensors.clear()

    @property
    def sensors(
        self,
    ) -> tuple[Sensor, ...]:

        return tuple(self._sensors)

    def before_execution(self) -> None:

        for sensor in self._sensors:

            sensor.before_execution()

    def after_execution(self) -> None:

        for sensor in self._sensors:

            sensor.after_execution()
