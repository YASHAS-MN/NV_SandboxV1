__all__ = ["IntakeGateway"]


def __getattr__(name):
    if name == "IntakeGateway":
        from .gateway import IntakeGateway

        return IntakeGateway

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
