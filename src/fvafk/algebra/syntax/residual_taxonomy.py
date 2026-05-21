"""Syntax-specific residual taxonomy.

Defines the canonical set of residuals for syntactic operations.
Each residual kind has a constructor function that ensures consistent
description formatting.

The ten syntax residual kinds:

1. **syntax.context_absent** — Surrounding tokens needed for disambiguation
2. **syntax.operator_scope_unresolved** — Operator scope not determined (e.g., إن, لم)
3. **syntax.case_missing** — Case marking (إعراب) not visible on surface
4. **syntax.case_estimated** — Case marking estimated/inferred (تقدير)
5. **syntax.case_ambiguous** — Multiple case readings possible
6. **syntax.governor_ambiguous** — Multiple possible عامل candidates
7. **syntax.ellipsis_possible** — Possible ellipsis (حذف) in structure
8. **syntax.attachment_ambiguous** — Unclear which phrase attaches where
9. **syntax.relation_candidate** — Relation type (ISN/TADMN/TAQYID) not finalized
10. **syntax.word_order_ambiguous** — Multiple word order interpretations

All residual constructors return :class:`fvafk.algebra.Residual` instances.
"""

from __future__ import annotations

from typing import FrozenSet

from fvafk.algebra import Residual


# Canonical set of syntax residual kinds
SYNTAX_RESIDUAL_KINDS: FrozenSet[str] = frozenset({
    "syntax.context_absent",
    "syntax.operator_scope_unresolved",
    "syntax.case_missing",
    "syntax.case_estimated",
    "syntax.case_ambiguous",
    "syntax.governor_ambiguous",
    "syntax.ellipsis_possible",
    "syntax.attachment_ambiguous",
    "syntax.relation_candidate",
    "syntax.word_order_ambiguous",
})


def make_context_absent(description: str = "") -> Residual:
    """Create residual for missing surrounding tokens.

    Args:
        description: Custom description (optional). If empty, uses default.

    Returns:
        Residual with kind ``syntax.context_absent``.
    """
    desc = description or "Syntax analysis needs surrounding tokens for disambiguation"
    return Residual(kind="syntax.context_absent", description=desc)


def make_operator_scope_unresolved(operator: str = "", description: str = "") -> Residual:
    """Create residual for unresolved operator scope.

    Args:
        operator: Operator name (e.g., "إن", "لم").
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.operator_scope_unresolved``.
    """
    if description:
        desc = description
    elif operator:
        desc = f"Scope of operator '{operator}' not fully determined"
    else:
        desc = "Operator scope requires additional context to resolve"
    return Residual(kind="syntax.operator_scope_unresolved", description=desc)


def make_case_missing(description: str = "") -> Residual:
    """Create residual for missing case marking.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.case_missing``.
    """
    desc = description or "Case marking (إعراب) not visible on surface form"
    return Residual(kind="syntax.case_missing", description=desc)


def make_case_estimated(description: str = "") -> Residual:
    """Create residual for estimated/inferred case marking.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.case_estimated``.
    """
    desc = description or "Case marking estimated (تقدير) rather than observed"
    return Residual(kind="syntax.case_estimated", description=desc)


def make_case_ambiguous(cases: str = "", description: str = "") -> Residual:
    """Create residual for ambiguous case marking.

    Args:
        cases: String listing possible cases (e.g., "رفع/نصب").
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.case_ambiguous``.
    """
    if description:
        desc = description
    elif cases:
        desc = f"Multiple case readings possible: {cases}"
    else:
        desc = "Case marking ambiguous without additional context"
    return Residual(kind="syntax.case_ambiguous", description=desc)


def make_governor_ambiguous(governors: str = "", description: str = "") -> Residual:
    """Create residual for ambiguous governor (عامل).

    Args:
        governors: String listing possible governors.
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.governor_ambiguous``.
    """
    if description:
        desc = description
    elif governors:
        desc = f"Multiple governor candidates: {governors}"
    else:
        desc = "Governor (عامل) ambiguous without additional context"
    return Residual(kind="syntax.governor_ambiguous", description=desc)


def make_ellipsis_possible(description: str = "") -> Residual:
    """Create residual for possible ellipsis (حذف).

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.ellipsis_possible``.
    """
    desc = description or "Possible ellipsis (حذف) in syntactic structure"
    return Residual(kind="syntax.ellipsis_possible", description=desc)


def make_attachment_ambiguous(description: str = "") -> Residual:
    """Create residual for ambiguous attachment.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.attachment_ambiguous``.
    """
    desc = description or "Phrase attachment ambiguous (multiple attachment sites possible)"
    return Residual(kind="syntax.attachment_ambiguous", description=desc)


def make_relation_candidate(relation_types: str = "", description: str = "") -> Residual:
    """Create residual for relation type candidates.

    Args:
        relation_types: String listing possible relation types (e.g., "ISN/TADMN").
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.relation_candidate``.
    """
    if description:
        desc = description
    elif relation_types:
        desc = f"Relation type candidates: {relation_types}"
    else:
        desc = "Syntactic relation type (ISN/TADMN/TAQYID) not finalized"
    return Residual(kind="syntax.relation_candidate", description=desc)


def make_word_order_ambiguous(description: str = "") -> Residual:
    """Create residual for word order ambiguity.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``syntax.word_order_ambiguous``.
    """
    desc = description or "Word order allows multiple syntactic interpretations"
    return Residual(kind="syntax.word_order_ambiguous", description=desc)


__all__ = [
    "SYNTAX_RESIDUAL_KINDS",
    "make_context_absent",
    "make_operator_scope_unresolved",
    "make_case_missing",
    "make_case_estimated",
    "make_case_ambiguous",
    "make_governor_ambiguous",
    "make_ellipsis_possible",
    "make_attachment_ambiguous",
    "make_relation_candidate",
    "make_word_order_ambiguous",
]
