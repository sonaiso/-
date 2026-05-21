"""Syntax adapter: syntactic links → Evidence.

This adapter translates syntax layer outputs (Link objects from
``fvafk.syntax``) into Evidence atoms for the SYNTAX domain.

Key contracts:

1. **Domain coverage**: Syntax adapter emits Evidence in domain
   ``SYNTAX`` only.
2. **Link evidence**: When syntactic links are detected (ISNADI,
   TADMINI, TAQYIDI), adapter emits Evidence with kind
   ``"syntax.link_detected"`` or ``"syntax.relation_candidate"``.
3. **No semantic/hukm jump**: Syntax adapter **never** emits Evidence
   kinds ``semantic.*`` or ``hukm.*``; it supports SYNTAX claims only,
   not SEMANTICS or HUKM.
4. **CPB compliance**: All Evidence must pass CPB validation for
   bridges ``MORPH_DEEP → SYNTAX`` or ``SYNTAX → SEMANTICS``.

Example usage::

    from fvafk.syntax import find_isnadi_links
    from fvafk.algebra.adapters import SyntaxAdapter

    # Find ISNADI links in a token sequence
    links = find_isnadi_links(tokens)

    adapter = SyntaxAdapter()
    for link in links:
        evidence_tuple = adapter.adapt(link)
        for ev in evidence_tuple:
            print(ev.kind, ev.source, ev.detail)
"""

from __future__ import annotations

from typing import Any, Tuple

from fvafk.algebra import Evidence

from .common import BaseAdapter


class SyntaxAdapter(BaseAdapter):
    """Adapter for syntax layer Link objects → Evidence.

    Translates syntactic link objects (ISNADI, TADMINI, TAQYIDI) into
    Evidence tuples supporting SYNTAX domain claims. Never emits
    SEMANTICS or HUKM evidence kinds.
    """

    def __init__(self, *, strict: bool = True):
        """Initialize syntax adapter.

        Args:
            strict: If ``True``, raise ``TypeError`` on unrecognized
                object types; if ``False``, return empty tuple silently.
        """
        super().__init__(source_module="syntax", strict=strict)

    def adapt(self, obj: Any) -> Tuple[Evidence, ...]:
        """Convert Link object to Evidence tuple.

        Args:
            obj: A ``Link`` object from ``fvafk.syntax`` or a dict-like
                object with keys ``"link_type"``, ``"source"``,
                ``"target"``.

        Returns:
            Tuple of Evidence atoms. Empty tuple if link is invalid or
            unrecognized.

        Raises:
            TypeError: If ``obj`` is not a Link or dict and
                ``strict=True``.
        """
        # Check if obj has Link-like attributes
        if hasattr(obj, "link_type") and hasattr(obj, "source") and hasattr(obj, "target"):
            return self._adapt_link_object(obj)

        # Check if obj is dict-like
        if isinstance(obj, dict):
            return self._adapt_link_dict(obj)

        if self.strict:
            raise TypeError(
                f"SyntaxAdapter.adapt() expects Link or dict, got {type(obj).__name__}"
            )
        return ()

    def _adapt_link_object(self, link: Any) -> Tuple[Evidence, ...]:
        """Adapt a Link object (has link_type, source, target attributes).

        Args:
            link: Link object from fvafk.syntax.

        Returns:
            Tuple of Evidence atoms.
        """
        link_type = str(link.link_type) if hasattr(link.link_type, "value") else str(link.link_type)

        # Extract source/target identifiers
        source_id = self._extract_token_id(link.source)
        target_id = self._extract_token_id(link.target)

        # Construct stable identifier for this link
        obj_id = f"{link_type}:{source_id}->{target_id}"

        detail = f"link_type={link_type} from '{source_id}' to '{target_id}'"

        # Weight: higher for ISNADI (core syntactic relation), lower for
        # TAQYIDI (modifier/adjunct)
        weight = self._compute_link_weight(link_type)

        evidence = self.make_evidence(
            kind="syntax.relation_candidate",
            obj_type="Link",
            obj_id=obj_id,
            detail=detail,
            weight=weight,
        )

        return (evidence,)

    def _adapt_link_dict(self, link_dict: dict) -> Tuple[Evidence, ...]:
        """Adapt a dict-like link representation.

        Args:
            link_dict: Dict with keys "link_type", "source", "target".

        Returns:
            Tuple of Evidence atoms.
        """
        link_type = link_dict.get("link_type", "UNKNOWN")
        source_id = str(link_dict.get("source", ""))
        target_id = str(link_dict.get("target", ""))

        if not link_type or not source_id or not target_id:
            return ()

        obj_id = f"{link_type}:{source_id}->{target_id}"
        detail = f"link_type={link_type} from '{source_id}' to '{target_id}'"
        weight = self._compute_link_weight(link_type)

        evidence = self.make_evidence(
            kind="syntax.relation_candidate",
            obj_type="Link",
            obj_id=obj_id,
            detail=detail,
            weight=weight,
        )

        return (evidence,)

    def _extract_token_id(self, token: Any) -> str:
        """Extract stable identifier from token object.

        Args:
            token: Token object (may have .surface, .text, or other
                identifier fields).

        Returns:
            String identifier for the token.
        """
        # Try common token identifier fields
        if hasattr(token, "surface"):
            return str(token.surface)
        if hasattr(token, "text"):
            return str(token.text)
        if hasattr(token, "value"):
            return str(token.value)
        # Fallback to string representation
        return str(token)

    def _compute_link_weight(self, link_type: str) -> float:
        """Compute Evidence weight based on link type.

        Args:
            link_type: Link type string (e.g. "ISNADI", "TADMINI",
                "TAQYIDI").

        Returns:
            Weight value between 0.5 and 1.0.
        """
        link_type_upper = link_type.upper()

        # ISNADI (إسنادي) is core predication — highest weight
        if "ISNADI" in link_type_upper or "ISN" in link_type_upper:
            return 0.9

        # TADMINI (تضميني) is complement/argument — high weight
        if "TADMINI" in link_type_upper or "TADMN" in link_type_upper:
            return 0.8

        # TAQYIDI (تقييدي) is modifier/adjunct — moderate weight
        if "TAQYIDI" in link_type_upper or "TAQYD" in link_type_upper:
            return 0.7

        # Unknown link type — conservative weight
        return 0.6


__all__ = ["SyntaxAdapter"]
