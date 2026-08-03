from pathlib import Path

from sandbox.runtime import Runner


class DummyRunner(Runner):

    @property
    def name(self):
        return "dummy"

    def supports(self, asset):
        return asset.suffix == ".dummy"

    def execute(self, asset, workspace):
        return None


runner = DummyRunner()

assert runner.name == "dummy"

assert runner.supports(
    Path("hello.dummy")
)

print("Runner protocol OK")
