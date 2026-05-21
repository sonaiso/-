"""C2B (morphology) adapter: RootExtractor → Evidence.

This adapter translates ``RootExtractionResult`` objects from
``fvafk.c2b.RootExtractor`` into Evidence atoms for the algebra layer.

Key contracts:

1. **Domain coverage**: C2B adapter emits Evidence in domains
   ``MORPH_SURFACE``, ``ROOT`` (primary), and occasionally
   ``MORPH_DEEP`` when pattern information is available.
2. **Root evidence**: When ``RootExtractionResult.root`` is not
   ``None``, adapter emits Evidence with kind ``"root.candidate"`` or
   ``"root.extracted"`` (reserved for high-confidence cases).
3. **Affixes as residuals**: Prefix/suffix information may be
   translated into Evidence kind ``"affix.detected"`` or into
   Residual when affixes are ambiguous.
4. **No semantic/hukm jump**: C2B adapter **never** emits Evidence
   kinds ``semantic.*`` or ``hukm.*``; it supports ROOT claims only.
5. **CPB compliance**: All Evidence must pass CPB validation for
   bridges ``MORPH_SURFACE → ROOT`` or ``ROOT → MORPH_DEEP``.

Example usage::

    from fvafk.c2b import RootExtractor
    from fvafk.algebra.adapters import C2bAdapter

    extractor = RootExtractor()
    result = extractor.extract_with_affixes("كاتب")

    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(result)

    for ev in evidence_tuple:
        print(ev.kind, ev.source, ev.detail)
    # Output:
    # root.candidate c2b:RootExtractionResult:كاتب root=('ك', 'ت', 'ب')
"""

from __future__ import annotations

from typing import Any, Tuple

from fvafk.c2b import RootExtractionResult, Root
from fvafk.algebra import Evidence, Residual

from .common import BaseAdapter


class C2bAdapter(BaseAdapter):
    """Adapter for C2B (morphology) RootExtractor → Evidence.

    Translates ``RootExtractionResult`` into Evidence tuples supporting
    ROOT domain claims. Never emits SEMANTICS or HUKM evidence kinds.
    """

    def __init__(self, *, strict: bool = True):
        """Initialize C2B adapter.

        Args:
            strict: If ``True``, raise ``TypeError`` on unrecognized
                object types; if ``False``, return empty tuple silently.
        """
        super().__init__(source_module="c2b", strict=strict)

    def adapt(self, obj: Any) -> Tuple[Evidence, ...]:
        """Convert RootExtractionResult to Evidence tuple.

        Args:
            obj: A ``RootExtractionResult`` from ``RootExtractor``.

        Returns:
            Tuple of Evidence atoms. Empty tuple ``()`` if ``obj.root``
            is ``None`` (no root extracted).

        Raises:
            TypeError: If ``obj`` is not a ``RootExtractionResult`` and
                ``strict=True``.
        """
        if not isinstance(obj, RootExtractionResult):
            if self.strict:
                raise TypeError(
                    f"C2bAdapter.adapt() expects RootExtractionResult, "
                    f"got {type(obj).__name__}"
                )
            return ()

        evidence_list = []

        # Primary claim: root extraction
        if obj.root is not None:
            evidence_list.append(self._make_root_evidence(obj))

        # Secondary claims: affixes (if present)
        if obj.prefix:
            evidence_list.append(self._make_affix_evidence(obj, "prefix"))
        if obj.suffix:
            evidence_list.append(self._make_affix_evidence(obj, "suffix"))

        return tuple(evidence_list)

    def adapt_with_residuals(
        self, obj: Any
    ) -> Tuple[Tuple[Evidence, ...], Tuple[Residual, ...]]:
        """Convert RootExtractionResult to (Evidence, Residuals) pair.

        This extended method returns both Evidence and Residuals. Use
        this when the caller needs explicit gap reporting (e.g. when
        stripped_word differs significantly from normalized_word,
        indicating aggressive affix stripping).

        Args:
            obj: A ``RootExtractionResult``.

        Returns:
            Tuple of (evidence_tuple, residual_tuple).
        """
        if not isinstance(obj, RootExtractionResult):
            if self.strict:
                raise TypeError(
                    f"C2bAdapter.adapt_with_residuals() expects RootExtractionResult, "
                    f"got {type(obj).__name__}"
                )
            return ((), ())

        evidence_tuple = self.adapt(obj)
        residuals = []

        # Check for aggressive stripping: if stripped_word is much
        # shorter than normalized_word, record a residual.
        if obj.stripped_word and obj.normalized_word:
            stripped_len = len(obj.stripped_word)
            normalized_len = len(obj.normalized_word)
            if stripped_len > 0 and normalized_len > 0:
                ratio = stripped_len / normalized_len
                if ratio < 0.5:
                    # More than half the word was stripped — potential
                    # over-segmentation.
                    residuals.append(
                        Residual(
                            kind="affix.aggressive_stripping",
                            description=(
                                f"stripped '{obj.stripped_word}' is much shorter "
                                f"than normalized '{obj.normalized_word}' "
                                f"(ratio {ratio:.2f}); possible over-segmentation."
                            ),
                        )
                    )

        # Check for weak letters in root (و/ي/ا) — often ambiguous
        if obj.root is not None:
            weak_count = sum(
                1 for letter in obj.root.letters if letter in {"و", "ي", "ا"}
            )
            if weak_count >= 2:
                # Multiple weak letters increase ambiguity
                residuals.append(
                    Residual(
                        kind="root.weak_letters",
                        description=(
                            f"root {obj.root.letters} contains {weak_count} weak "
                            "letters (و/ي/ا); pattern ambiguity is higher."
                        ),
                    )
                )

        return (evidence_tuple, tuple(residuals))

    def _make_root_evidence(self, result: RootExtractionResult) -> Evidence:
        """Construct Evidence for root extraction.

        Args:
            result: RootExtractionResult with non-None root.

        Returns:
            Evidence with kind "root.candidate" citing the original
            normalized_word.
        """
        assert result.root is not None

        # Use normalized_word as the stable identifier (since
        # RootExtractionResult lacks a unique id field).
        # Format: root letters as string "ك-ت-ب"
        root_str = "-".join(result.root.letters)

        detail = f"root={result.root.letters} from '{result.normalized_word}'"
        if result.stripped_word != result.normalized_word:
            detail += f" (stripped='{result.stripped_word}')"

        # Weight: lower weight for weak roots (more ambiguous)
        weak_letters = {"و", "ي", "ا", "ء"}
        weak_count = sum(1 for letter in result.root.letters if letter in weak_letters)
        weight = max(0.5, 1.0 - (weak_count * 0.1))

        return self.make_evidence(
            kind="root.candidate",
            obj_type="RootExtractionResult",
            obj_id=result.normalized_word,
            detail=detail,
            weight=weight,
        )

    def _make_affix_evidence(
        self, result: RootExtractionResult, affix_type: str
    ) -> Evidence:
        """Construct Evidence for detected prefix/suffix.

        Args:
            result: RootExtractionResult.
            affix_type: "prefix" or "suffix".

        Returns:
            Evidence with kind "affix.detected".
        """
        affix_value = result.prefix if affix_type == "prefix" else result.suffix
        assert affix_value  # caller ensures non-empty

        detail = f"{affix_type}='{affix_value}' in '{result.normalized_word}'"

        return self.make_evidence(
            kind="affix.detected",
            obj_type="RootExtractionResult",
            obj_id=result.normalized_word,
            detail=detail,
            weight=0.6,  # Affixes are less certain than roots
        )


__all__ = ["C2bAdapter"]
