from pathlib import Path

from sandbox.intake.classifier import AssetClassifier

classifier = AssetClassifier()

samples = [
    "hello.py",
    "photo.png",
    "installer.exe",
    "report.pdf",
    "archive.zip",
    "unknown.xyz",
]

for sample in samples:

    result = classifier.classify(
        Path(sample)
    )

    print(sample)

    print(result.category.value)

    print()
