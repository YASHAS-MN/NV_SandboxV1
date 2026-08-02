from pathlib import Path

from sandbox.intake.analyzers.extension_analyzer import ExtensionAnalyzer

analyzer = ExtensionAnalyzer()

print(
    analyzer.analyze(
        Path("installer.exe")
    ).to_dict()
)

print(
    analyzer.analyze(
        Path("photo.png")
    ).to_dict()
)
