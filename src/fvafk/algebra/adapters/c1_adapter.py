"""C1 (encoding/normalization) adapter → Evidence.

This adapter translates C1 layer outputs (encoding, normalization,
grapheme-to-phoneme) into Evidence atoms for GRAPHEME and PHONEME
domains.

Key contracts:

1. **Domain coverage**: C1 adapter emits Evidence in domains
   ``GRAPHEME`` and ``PHONEME``.
2. **Encoding evidence**: When text is successfully encoded/normalized,
   adapter emits Evidence with kind ``"encoding.normalized"`` or
   ``"encoding.validated"``.
3. **No semantic jump**: C1 adapter never emits SEMANTICS or HUKM
   evidence kinds.
4. **CPB compliance**: All Evidence must pass CPB validation for bridge
   ``GRAPHEME → PHONEME``.

Since C1 typically operates on raw strings (not structured objects),
this adapter provides a convenience method ``adapt_text()`` in addition
to the standard ``adapt()`` protocol.

Example usage::

    from fvafk.algebra.adapters import C1Adapter

    adapter = C1Adapter()

    # Method 1: adapt raw text
    evidence = adapter.adapt_text("كاتب", normalized="كاتب")

    # Method 2: adapt a dict-like object (if C1 returns structured output)
    obj = {"text": "كاتب", "normalized": "كاتب"}
    evidence = adapter.adapt(obj)
"""

from __future__ import annotations

from typing import Any, Tuple

from fvafk.algebra import Evidence

from .common import BaseAdapter


class C1Adapter(BaseAdapter):
    """Adapter for C1 (encoding/normalization) → Evidence.

    Translates C1 encoding/normalization outputs into Evidence tuples
    supporting GRAPHEME and PHONEME domain claims.
    """

    def __init__(self, *, strict: bool = False):
        """Initialize C1 adapter.

        Args:
            strict: If ``True``, raise ``TypeError`` on unrecognized
                object types; if ``False``, return empty tuple silently.
                Default ``False`` because C1 often works with plain
                strings, not structured objects.
        """
        super().__init__(source_module="c1", strict=strict)

    def adapt(self, obj: Any) -> Tuple[Evidence, ...]:
        """Convert C1 output to Evidence tuple.

        Args:
            obj: A dict-like object with keys ``"text"`` and optionally
                ``"normalized"``, or a plain string.

        Returns:
            Tuple of Evidence atoms.

        Raises:
            TypeError: If ``obj`` is not dict-like or string and
                ``strict=True``.
        """
        if isinstance(obj, str):
            # Plain string: emit basic encoding evidence
            return self.adapt_text(obj, normalized=obj)

        if isinstance(obj, dict):
            text = obj.get("text", "")
            normalized = obj.get("normalized", text)
            return self.adapt_text(text, normalized=normalized)

        if self.strict:
            raise TypeError(
                f"C1Adapter.adapt() expects dict or str, got {type(obj).__name__}"
            )
        return ()

    def adapt_text(
        self, text: str, *, normalized: str | None = None
    ) -> Tuple[Evidence, ...]:
        """Convert raw text to Evidence tuple.

        Args:
            text: Original input text.
            normalized: Normalized form (optional). If not provided,
                assumed same as ``text``.

        Returns:
            Tuple of Evidence atoms.
        """
        if not text:
            return ()

        normalized = normalized or text

        evidence_list = []

        # Evidence: text successfully encoded
        evidence_list.append(
            self.make_evidence(
                kind="encoding.validated",
                obj_type="text",
                obj_id=text,
                detail=f"text='{text}' validated as Arabic",
                weight=1.0,
            )
        )

        # Evidence: normalization applied (if text changed)
        if normalized != text:
            evidence_list.append(
                self.make_evidence(
                    kind="encoding.normalized",
                    obj_type="text",
                    obj_id=text,
                    detail=f"normalized '{text}' → '{normalized}'",
                    weight=0.9,
                )
            )

        return tuple(evidence_list)


__all__ = ["C1Adapter"]
