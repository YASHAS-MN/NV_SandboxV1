"""
Nebula Labs

Asset Classifier

Determines the asset type before any
security processing begins.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from sandbox.intake.asset_types import AssetCategory
from sandbox.intake.models import AssetClassification


class AssetClassifier:

    SCRIPT_EXTENSIONS = {
        ".py",
        ".js",
        ".ps1",
        ".sh",
    }

    EXECUTABLE_EXTENSIONS = {
        ".exe",
        ".msi",
        ".apk",
    }

    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".xlsx",
        ".pptx",
        ".txt",
    }

    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
    }

    AUDIO_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".flac",
    }

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".avi",
        ".mkv",
    }

    ARCHIVE_EXTENSIONS = {
        ".zip",
        ".7z",
        ".rar",
        ".tar",
        ".gz",
    }

    def classify(
        self,
        asset: Path,
    ) -> AssetClassification:

        ext = asset.suffix.lower()

        mime, _ = mimetypes.guess_type(asset)

        if ext in self.SCRIPT_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.SCRIPT,
                subtype="script",
                extension=ext,
                mime_type=mime or "",
                requires_execution=True,
                confidence=1.0,
            )

        if ext in self.EXECUTABLE_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.EXECUTABLE,
                subtype="binary",
                extension=ext,
                mime_type=mime or "",
                requires_execution=True,
                confidence=1.0,
            )

        if ext in self.DOCUMENT_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.DOCUMENT,
                subtype="document",
                extension=ext,
                mime_type=mime or "",
                requires_execution=False,
                confidence=1.0,
            )

        if ext in self.IMAGE_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.IMAGE,
                subtype="image",
                extension=ext,
                mime_type=mime or "",
                requires_execution=False,
                confidence=1.0,
            )

        if ext in self.AUDIO_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.AUDIO,
                subtype="audio",
                extension=ext,
                mime_type=mime or "",
                requires_execution=False,
                confidence=1.0,
            )

        if ext in self.VIDEO_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.VIDEO,
                subtype="video",
                extension=ext,
                mime_type=mime or "",
                requires_execution=False,
                confidence=1.0,
            )

        if ext in self.ARCHIVE_EXTENSIONS:

            return AssetClassification(
                category=AssetCategory.ARCHIVE,
                subtype="archive",
                extension=ext,
                mime_type=mime or "",
                requires_execution=False,
                confidence=1.0,
            )

        return AssetClassification(
            category=AssetCategory.UNKNOWN,
            subtype="unknown",
            extension=ext,
            mime_type=mime or "",
            requires_execution=False,
            confidence=0.0,
        )
