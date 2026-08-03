"""
Nebula Labs

Classification Engine

Consumes canonical Evidence objects and
produces a deterministic ClassificationResult.
"""

from __future__ import annotations

from sandbox.intake.asset_types import AssetCategory
from sandbox.intake.classification.result import ClassificationResult
from sandbox.intake.evidence import (
    Evidence,
    ExtensionEvidence,
    MagicEvidence,
)


class ClassificationEngine:

    def classify(
        self,
        evidence: list[Evidence],
    ) -> ClassificationResult:

        extension = None
        magic = None

        for item in evidence:

            if isinstance(item, ExtensionEvidence):
                extension = item

            elif isinstance(item, MagicEvidence):
                magic = item

        return self._fuse(
            extension,
            magic,
            evidence,
        )

    def _fuse(
        self,
        extension: ExtensionEvidence | None,
        magic: MagicEvidence | None,
        evidence: list[Evidence],
    ) -> ClassificationResult:

        if extension is None and magic is None:

            return ClassificationResult(
                category=AssetCategory.UNKNOWN,
                confidence=0.0,
                evidence_used=evidence,
            )

        if extension and magic:

            return self._resolve_conflict(
                extension,
                magic,
                evidence,
            )

        if extension:

            return ClassificationResult(
                category=self._category_from_extension(
                    extension.extension
                ),
                confidence=0.50,
                evidence_used=evidence,
            )

        return ClassificationResult(
            category=self._category_from_magic(
                magic.matched_format
            ),
            confidence=0.80,
            evidence_used=evidence,
        )

    def _resolve_conflict(
        self,
        extension: ExtensionEvidence,
        magic: MagicEvidence,
        evidence: list[Evidence],
    ) -> ClassificationResult:

        ext_category = self._category_from_extension(
            extension.extension
        )

        magic_category = self._category_from_magic(
            magic.matched_format
        )

        if magic.matched_format is None:
            return ClassificationResult(
                category=ext_category,
                confidence=0.70,
                evidence_used=evidence,
            )

        if ext_category == magic_category:

            return ClassificationResult(
                category=magic_category,
                confidence=1.0,
                evidence_used=evidence,
            )

        return ClassificationResult(
            category=magic_category,
            confidence=0.60,
            evidence_used=evidence,
            conflicts=[
                "Extension and magic signature disagree."
            ],
            warnings=[
                "Possible disguised asset."
            ],
        )

    def _category_from_extension(
        self,
        extension: str,
    ) -> AssetCategory:

        extension = extension.lower()

        # --- Executables ---
        if extension in (".exe", ".dll", ".so", ".dylib"):
            return AssetCategory.EXECUTABLE

        # --- Scripts (interpreted languages) ---
        if extension in (
            ".py", ".pyw",                        # Python
            ".js", ".ts", ".mjs", ".cjs",         # JavaScript / TypeScript
            ".rb",                                  # Ruby
            ".pl", ".pm",                          # Perl
            ".php",                                 # PHP
            ".lua",                                 # Lua
        ):
            return AssetCategory.SCRIPT

        # --- Shell scripts ---
        if extension in (".sh", ".bash", ".zsh", ".fish",  # Unix shells
                         ".ps1", ".psm1", ".psd1",          # PowerShell
                         ".bat", ".cmd"):
            return AssetCategory.SCRIPT

        # --- JVM bytecode ---
        if extension in (".jar", ".class", ".war", ".ear"):
            return AssetCategory.SCRIPT

        # --- Python bytecode ---
        if extension == ".pyc":
            return AssetCategory.SCRIPT

        # --- Images ---
        if extension in (".png", ".jpg", ".jpeg", ".gif",
                         ".bmp", ".webp", ".svg", ".ico",
                         ".tiff", ".tif"):
            return AssetCategory.IMAGE

        # --- Documents ---
        if extension in (".pdf", ".doc", ".docx", ".odt",
                         ".txt", ".md", ".rst", ".rtf"):
            return AssetCategory.DOCUMENT

        # --- Audio ---
        if extension in (".mp3", ".wav", ".flac", ".ogg",
                         ".aac", ".m4a", ".wma", ".opus"):
            return AssetCategory.AUDIO

        # --- Video ---
        if extension in (".mp4", ".mkv", ".avi", ".mov",
                         ".webm", ".flv", ".wmv", ".m4v"):
            return AssetCategory.VIDEO

        # --- Archives ---
        if extension in (".zip", ".tar", ".gz", ".tgz",
                         ".bz2", ".xz", ".7z", ".rar"):
            return AssetCategory.ARCHIVE

        # --- Data / structured text ---
        if extension in (".csv", ".json", ".xml", ".yaml",
                         ".yml", ".toml", ".ini", ".cfg",
                         ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp",
                         ".rs", ".go", ".cs", ".java"):
            return AssetCategory.DATA

        return AssetCategory.UNKNOWN

    def _category_from_magic(
        self,
        matched: str | None,
    ) -> AssetCategory:

        mapping = {
            "PE": AssetCategory.EXECUTABLE,
            "Windows PE (.exe)": AssetCategory.EXECUTABLE,
            "PNG": AssetCategory.IMAGE,
            "JPEG": AssetCategory.IMAGE,
            "PDF": AssetCategory.DOCUMENT,
            "ZIP": AssetCategory.ARCHIVE,
            "ZIP / OOXML / APK / JAR": AssetCategory.ARCHIVE,
            "MP3": AssetCategory.AUDIO,
        }

        return mapping.get(
            matched,
            AssetCategory.UNKNOWN,
        )
