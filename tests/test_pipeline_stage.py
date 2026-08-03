from pathlib import Path

from sandbox.orchestration import PipelineStage


class DummyStage(PipelineStage):

    @property
    def name(self):
        return "dummy"

    def run(self, asset: Path):
        return asset.name


stage = DummyStage()

assert stage.name == "dummy"

assert stage.run(Path("abc.exe")) == "abc.exe"

print("PipelineStage OK")
