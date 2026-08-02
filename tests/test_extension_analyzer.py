from pathlib import Path

from sandbox.intake.analyzers.extension_analyzer import ExtensionAnalyzer

analyzer = ExtensionAnalyzer()

print(
    analyzer.analyze(
        Path("installer.exe")
    )
)

print(
    analyzer.analyze(
        Path("photo.png")
    )
)
