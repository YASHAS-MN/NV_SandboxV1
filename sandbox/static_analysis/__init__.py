"""
Nebula Static Analysis Gateway
"""

__all__ = [
    "StaticEvidenceBus",
    "StaticGateway",
]


def __getattr__(name):
    if name == "StaticEvidenceBus":
        from .static_bus import StaticEvidenceBus

        return StaticEvidenceBus

    if name == "StaticGateway":
        from .gateway import StaticGateway

        return StaticGateway

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
