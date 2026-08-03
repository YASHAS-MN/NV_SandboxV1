"""
Nebula Labs

Execution Runtime
"""

from __future__ import annotations

import time
from pathlib import Path

from shared.logger import logger
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

        start = time.perf_counter()
        workspace = self._workspace_manager

        context = ObservationContext(
            protocol_version="1.0",
            runtime_profile="nebula-runtime-v2",
            observation_profile="default",
            policy_version="1.0",
        )
        builder = TranscriptBuilder(context)

        logger.info(f"Preparing execution context for asset: {asset.name}")

        try:
            logger.info("Creating temporary workspace...")
            workspace.create()

            self._observation_bus.set_builder(builder)

            # Broadcast workspace path to all sensors (e.g. NetworkSensor)
            self._sensor_manager.attach_workspace(workspace.path)

            self._sensor_manager.before_execution()

            logger.info("Selecting execution runner...")
            runner = self._runner_manager.select(asset)

            logger.info(f"Starting execution of {asset.name} via runner: {runner.name}")
            result: ExecutionResult = runner.execute(
                asset,
                workspace,
            )

            if result.timed_out:
                logger.warning(f"Execution timed out for asset: {asset.name}")

            logger.info(f"Execution finished. exit_code: {result.exit_code}, duration: {result.duration_ms}ms")

            self._sensor_manager.after_execution()

            transcript = builder.build()

            return ExecutionSession(
                transcript=transcript,
                exit_code=result.exit_code,
                timed_out=result.timed_out,
                duration_ms=result.duration_ms,
            )

        except Exception as e:
            logger.error(f"Execution failed due to unhandled exception: {e}", exc_info=True)
            duration = int((time.perf_counter() - start) * 1000)
            transcript = builder.build()
            return ExecutionSession(
                transcript=transcript,
                exit_code=-1,
                timed_out=False,
                duration_ms=duration,
            )

        finally:
            logger.info("Cleaning up temporary workspace...")
            workspace.cleanup()
