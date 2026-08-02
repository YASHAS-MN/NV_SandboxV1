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

        if extension == ".exe":
            return AssetCategory.EXECUTABLE

        if extension == ".py":
            return AssetCategory.SCRIPT

        if extension == ".png":
            return AssetCategory.IMAGE

        if extension == ".pdf":
            return AssetCategory.DOCUMENT

        return AssetCategory.UNKNOWN

    def _category_from_magic(
        self,
        matched: str | None,
    ) -> AssetCategory:

        mapping = {
            "PE": AssetCategory.EXECUTABLE,
            "Windows PE (.exe)": AssetCategory.EXECUTABLE,
            "PNG": AssetCategory.IMAGE,
            "PDF": AssetCategory.DOCUMENT,
            "ZIP": AssetCategory.ARCHIVE,
            "ZIP / OOXML / APK / JAR": AssetCategory.ARCHIVE,
        }

        return mapping.get(
            matched,
            AssetCategory.UNKNOWN,
        )
