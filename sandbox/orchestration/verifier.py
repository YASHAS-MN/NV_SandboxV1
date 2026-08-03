"""
Nebula Labs

Nebula Verifier

Coordinates all stages of verification pipeline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sandbox.intake.gateway import IntakeGateway
from sandbox.static_analysis.gateway import StaticGateway
from sandbox.policy.engine import ExecutionPolicyEngine
from sandbox.policy.decision import ExecutionAction
from sandbox.runtime import (
    ExecutionRuntime,
    WorkspaceManager,
    RunnerManager,
    PythonRunner,
    JavaScriptRunner,
    ShellRunner,
    JavaRunner,
    ArchiveRunner,
)
from sandbox.runtime.process_executor import ProcessExecutor
from sandbox.observation.observation_bus import ObservationBus
from sandbox.sensors.manager import SensorManager
from sandbox.sensors.process_sensor import ProcessSensor
from sandbox.sensors.filesystem_sensor import FilesystemSensor
from sandbox.sensors.network_sensor import NetworkSensor
from sandbox.behavior.hasher import TranscriptHasher
from sandbox.behavior.execution_metadata import ExecutionMetadata
from sandbox.orchestration.verification_result import VerificationResult


class NebulaVerifier:

    def __init__(self, timeout: float = 30.0) -> None:

        self._intake = IntakeGateway()
        self._static = StaticGateway()
        self._policy = ExecutionPolicyEngine()

        self._bus = ObservationBus()
        self._sensor_manager = SensorManager()
        self._sensor_manager.register(NetworkSensor(self._bus))
        self._sensor_manager.register(ProcessSensor(self._bus))
        self._sensor_manager.register(FilesystemSensor(self._bus))

        executor = ProcessExecutor()
        self._runner_manager = RunnerManager()
        self._runner_manager.register(PythonRunner(executor, timeout=timeout))
        self._runner_manager.register(JavaScriptRunner(executor, timeout=timeout))
        self._runner_manager.register(ShellRunner(executor, timeout=timeout))
        self._runner_manager.register(JavaRunner(executor, timeout=timeout))
        self._runner_manager.register(ArchiveRunner(timeout=timeout))

        self._runtime = ExecutionRuntime(
            runner_manager=self._runner_manager,
            sensor_manager=self._sensor_manager,
            workspace_manager=WorkspaceManager(),
            observation_bus=self._bus,
        )

    def verify(
        self,
        asset: Path | str,
    ) -> VerificationResult:

        asset_path = Path(asset)

        # 1. Intake Stage
        classification = self._intake.run(asset_path)

        # 2. Static Analysis Stage
        static_analysis = self._static.run(asset_path)

        # 3. Policy Stage
        policy_decision = self._policy.evaluate(classification, static_analysis)

        execution_dict = None
        transcript_dict = None
        t_hash = None

        # 4. Runtime Stage (if policy says CONTINUE)
        if policy_decision.action == ExecutionAction.CONTINUE:

            session = self._runtime.execute(asset_path)

            execution_meta = ExecutionMetadata(
                exit_code=session.exit_code,
                timed_out=session.timed_out,
                duration_ms=session.duration_ms,
            )
            execution_dict = execution_meta.to_dict()
            transcript_dict = session.transcript.to_dict()
            t_hash = TranscriptHasher.hash(session.transcript)

        # 5. Package final VerificationResult
        return VerificationResult(
            classification=classification,
            static_analysis=static_analysis,
            decision=policy_decision.action.value,
            execution=execution_dict,
            transcript=transcript_dict,
            hash=t_hash,
        )
