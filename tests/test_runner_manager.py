from pathlib import Path

from sandbox.runtime import (
    Runner,
    RunnerManager,
)


class PythonRunner(Runner):

    @property
    def name(self):
        return "python"

    def supports(self, asset):
        return asset.suffix == ".py"

    def execute(self, asset, workspace):
        return None


class ExeRunner(Runner):

    @property
    def name(self):
        return "exe"

    def supports(self, asset):
        return asset.suffix == ".exe"

    def execute(self, asset, workspace):
        return None


manager = RunnerManager()

manager.register(PythonRunner())
manager.register(ExeRunner())

assert manager.select(Path("hello.py")).name == "python"

assert manager.select(Path("virus.exe")).name == "exe"

try:
    manager.select(Path("archive.zip"))
    raise AssertionError("Expected RuntimeError")
except RuntimeError:
    pass

print("RunnerManager OK")
