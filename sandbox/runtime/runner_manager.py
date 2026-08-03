"""
Nebula Labs

Runner Manager
"""

from __future__ import annotations

from pathlib import Path

from sandbox.runtime.runner import Runner


class RunnerManager:
    """
    Selects the appropriate execution runner
    for a given asset.
    """

    def __init__(self) -> None:
        self._runners: list[Runner] = []

    def register(
        self,
        runner: Runner,
    ) -> None:

        self._runners.append(runner)

    @property
    def runners(
        self,
    ) -> tuple[Runner, ...]:

        return tuple(self._runners)

    def select(
        self,
        asset: Path,
    ) -> Runner:

        for runner in self._runners:

            if runner.supports(asset):
                return runner

        raise RuntimeError(
            f"No runner registered for asset: {asset}"
        )
