__all__ = [
    "VerificationResult",
    "GatewayOrchestrator",
    "PipelineStage",
    "NebulaVerifier",
]


def __getattr__(name):
    if name == "VerificationResult":
        from .verification_result import VerificationResult

        return VerificationResult

    if name == "GatewayOrchestrator":
        from .gateway_orchestrator import GatewayOrchestrator

        return GatewayOrchestrator

    if name == "PipelineStage":
        from .pipeline import PipelineStage

        return PipelineStage

    if name == "NebulaVerifier":
        from .verifier import NebulaVerifier

        return NebulaVerifier

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
