"""
Nebula Labs

Execution Runtime
"""

from __future__ import annotations

from pathlib import Path

from sandbox.behavior import (
    ObservationContext,
    TranscriptBuilder,
)

from sandbox.runtime.result import ExecutionResult
from sandbox.runtime.session import ExecutionSession

from sandbox.runtime.runner_manager import RunnerManager
from sandbox.runtime.workspace import WorkspaceManager

from sandbox.sensors.manager import SensorManager
from sandbox.observation.observation_bus import ObservationBus


class ExecutionRuntime:
    """
    High-level runtime orchestrator.

    Responsibilities:

    - create workspace
    - create observation context
    - construct transcript
    - coordinate sensors
    - select runner
    - package ExecutionSession
    """

    def __init__(
        self,
        runner_manager: RunnerManager,
        sensor_manager: SensorManager,
        workspace_manager: WorkspaceManager,
        observation_bus: ObservationBus,
    ) -> None:

        self._runner_manager = runner_manager
        self._sensor_manager = sensor_manager
        self._workspace_manager = workspace_manager
        self._observation_bus = observation_bus

    def execute(
        self,
        asset: Path,
    ) -> ExecutionSession:

        workspace = self._workspace_manager

        workspace.create()

        try:

            context = ObservationContext(

                protocol_version="1.0",

                runtime_profile="python-runtime-v1",

                observation_profile="default",

                policy_version="1.0",

            )

            builder = TranscriptBuilder(context)

            #
            # IMPORTANT
            #
            # ObservationBus should receive
            # the builder here.
            #
            # If your current ObservationBus
            # uses another setter name,
            # adjust ONLY this line.
            #

            self._observation_bus.set_builder(builder)

            self._sensor_manager.before_execution()

            runner = self._runner_manager.select(asset)

            result: ExecutionResult = runner.execute(

                asset,

                workspace,

            )

            self._sensor_manager.after_execution()

            transcript = builder.build()

            return ExecutionSession(

                transcript=transcript,

                exit_code=result.exit_code,

                timed_out=result.timed_out,

                duration_ms=result.duration_ms,

            )

        finally:

            workspace.cleanup()
