"""Residual Taxonomy for General Learning.

Residuals specific to rule-learning operations. These track what remains
unresolved during the learning process.

Core Principle:
    البقايا في التعلم ليست فشلاً، بل هي ما لم يُتعلم بعد.
    "Residuals in learning are not failures; they are what has not been learned yet."

Learning Residual Categories:
    1. **Origin residuals** — Not enough positive examples
    2. **Invariant residuals** — Pattern unclear or unstable
    3. **Manaat residuals** — Scope/basis ambiguous
    4. **Counterexample residuals** — Unresolved contradictions
    5. **Refinement residuals** — Rule modification incomplete
    6. **Evidence residuals** — Supporting evidence insufficient
    7. **Generalization residuals** — Over-generalization suspected
    8. **Specialization residuals** — Over-specialization suspected
"""

from __future__ import annotations

from enum import Enum, auto
from typing import FrozenSet

from fvafk.algebra import Residual


# ===========================================================================
# Learning Residual Kinds
# ===========================================================================


class LearningResidual(Enum):
    """Residual types specific to rule-learning operations.

    These residuals prevent a learned rule from reaching CERTIFIED rank.
    Each residual represents an aspect of the learning process that
    remains unresolved.
    """

    # Origin residuals (أصول)
    ORIGIN_INSUFFICIENT = auto()        # أصول غير كافية
    ORIGIN_CONFLICTING = auto()         # أصول متعارضة
    ORIGIN_UNVERIFIED = auto()          # أصول غير محققة

    # Invariant residuals (ثوابت)
    INVARIANT_UNCLEAR = auto()          # ثابت غير واضح
    INVARIANT_UNSTABLE = auto()         # ثابت غير مستقر
    INVARIANT_MULTIPLE = auto()         # ثوابت متعددة

    # Manaat residuals (مناط)
    MANAAT_AMBIGUOUS = auto()           # مناط ملتبس
    MANAAT_TOO_BROAD = auto()           # مناط واسع جداً
    MANAAT_TOO_NARROW = auto()          # مناط ضيق جداً

    # Counterexample residuals (أمثلة مضادة)
    COUNTEREXAMPLE_UNRESOLVED = auto()  # مثال مضاد غير محسوم
    COUNTEREXAMPLE_IGNORED = auto()     # مثال مضاد مُهمل
    COUNTEREXAMPLE_EXPLAINED = auto()   # مثال مضاد مُفسّر (but not integrated)
    COUNTEREXAMPLE_SEARCH_INCOMPLETE = auto()  # بحث الأمثلة المضادة ناقص

    # Refinement residuals (تعديل)
    REFINEMENT_INCOMPLETE = auto()      # تعديل ناقص
    REFINEMENT_UNVERIFIED = auto()      # تعديل غير محقق
    REFINEMENT_CYCLIC = auto()          # تعديل دوري (unstable)

    # Evidence residuals (دليل)
    EVIDENCE_INSUFFICIENT = auto()      # دليل غير كافٍ
    EVIDENCE_WEAK = auto()              # دليل ضعيف
    EVIDENCE_CONFLICTING = auto()       # دليل متعارض

    # Generalization residuals (تعميم)
    OVERGENERALIZATION = auto()         # تعميم زائد
    HASTY_GENERALIZATION = auto()       # تعميم متسرع
    GENERALIZATION_UNTESTED = auto()    # تعميم غير مختبر

    # Specialization residuals (تخصيص)
    OVERSPECIALIZATION = auto()         # تخصيص زائد
    SPECIALIZATION_UNJUSTIFIED = auto() # تخصيص غير مبرر
    SPECIALIZATION_UNTESTED = auto()    # تخصيص غير مختبر

    # Trace residuals (أثر)
    MODIFICATION_HISTORY_INCOMPLETE = auto()  # تاريخ التعديل ناقص
    RANK_DEMOTION_UNEXPLAINED = auto()        # تخفيض الرتبة غير مفسر
    RANK_PROMOTION_UNJUSTIFIED = auto()       # ترقية الرتبة غير مبررة


# Canonical set of learning residual kinds (as strings for Residual creation)
LEARNING_RESIDUAL_KINDS: FrozenSet[str] = frozenset({
    "origin.insufficient",
    "origin.conflicting",
    "origin.unverified",
    "invariant.unclear",
    "invariant.unstable",
    "invariant.multiple",
    "manaat.ambiguous",
    "manaat.too_broad",
    "manaat.too_narrow",
    "counterexample.unresolved",
    "counterexample.ignored",
    "counterexample.explained",
    "counterexample.search_incomplete",
    "refinement.incomplete",
    "refinement.unverified",
    "refinement.cyclic",
    "evidence.insufficient",
    "evidence.weak",
    "evidence.conflicting",
    "overgeneralization",
    "hasty_generalization",
    "generalization.untested",
    "overspecialization",
    "specialization.unjustified",
    "specialization.untested",
    "modification_history.incomplete",
    "rank_demotion.unexplained",
    "rank_promotion.unjustified",
})


# ===========================================================================
# Residual Constructors
# ===========================================================================


def make_origin_insufficient(count: int = 0, description: str = "") -> Residual:
    """Create residual for insufficient origin examples.

    Args:
        count: Number of origin examples found (if known).
        description: Custom description (optional).

    Returns:
        Residual with kind ``origin.insufficient``.

    Example:
        >>> r = make_origin_insufficient(count=2)
        >>> r.kind
        'origin.insufficient'
        >>> 'Need at least 3' in r.description
        True
    """
    if not description:
        if count > 0:
            description = (
                f"Only {count} origin example(s) found; "
                f"need at least 3 for stable pattern extraction"
            )
        else:
            description = "Insufficient positive origin examples for pattern extraction"
    return Residual(kind="origin.insufficient", description=description)


def make_origin_conflicting(description: str = "") -> Residual:
    """Create residual for conflicting origin examples.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``origin.conflicting``.
    """
    if not description:
        description = "Origin examples show conflicting patterns; invariant unclear"
    return Residual(kind="origin.conflicting", description=description)


def make_origin_unverified(description: str = "") -> Residual:
    """Create residual for unverified origin examples.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``origin.unverified``.
    """
    if not description:
        description = "Origin examples not verified in lexicon/corpus"
    return Residual(kind="origin.unverified", description=description)


def make_invariant_unclear(description: str = "") -> Residual:
    """Create residual for unclear invariant.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``invariant.unclear``.
    """
    if not description:
        description = "Invariant pattern not clearly identifiable across examples"
    return Residual(kind="invariant.unclear", description=description)


def make_invariant_unstable(description: str = "") -> Residual:
    """Create residual for unstable invariant.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``invariant.unstable``.
    """
    if not description:
        description = "Invariant pattern changes when new examples added"
    return Residual(kind="invariant.unstable", description=description)


def make_invariant_multiple(count: int = 0, description: str = "") -> Residual:
    """Create residual for multiple competing invariants.

    Args:
        count: Number of competing invariants (if known).
        description: Custom description (optional).

    Returns:
        Residual with kind ``invariant.multiple``.
    """
    if not description:
        if count > 0:
            description = f"{count} competing invariant patterns detected; need disambiguation"
        else:
            description = "Multiple invariant patterns compete; need disambiguation"
    return Residual(kind="invariant.multiple", description=description)


def make_manaat_ambiguous(description: str = "") -> Residual:
    """Create residual for ambiguous manaat (scope/basis).

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``manaat.ambiguous``.

    Example:
        >>> r = make_manaat_ambiguous()
        >>> r.kind
        'manaat.ambiguous'
    """
    if not description:
        description = "Rule scope/basis (المناط) ambiguous; need constraining examples"
    return Residual(kind="manaat.ambiguous", description=description)


def make_manaat_too_broad(description: str = "") -> Residual:
    """Create residual for overly broad manaat.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``manaat.too_broad``.
    """
    if not description:
        description = "Rule scope too broad; over-generalizes to non-examples"
    return Residual(kind="manaat.too_broad", description=description)


def make_manaat_too_narrow(description: str = "") -> Residual:
    """Create residual for overly narrow manaat.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``manaat.too_narrow``.
    """
    if not description:
        description = "Rule scope too narrow; misses valid examples"
    return Residual(kind="manaat.too_narrow", description=description)


def make_counterexample_unresolved(example: str = "", description: str = "") -> Residual:
    """Create residual for unresolved counterexample.

    Args:
        example: The counterexample surface form (if known).
        description: Custom description (optional).

    Returns:
        Residual with kind ``counterexample.unresolved``.

    Example:
        >>> r = make_counterexample_unresolved(example="طاهر")
        >>> r.kind
        'counterexample.unresolved'
        >>> 'طاهر' in r.description
        True
    """
    if not description:
        if example:
            description = f"Counterexample '{example}' contradicts current rule; needs refinement"
        else:
            description = "Counterexample contradicts current rule; needs refinement"
    return Residual(kind="counterexample.unresolved", description=description)


def make_counterexample_ignored(example: str = "", description: str = "") -> Residual:
    """Create residual for ignored counterexample.

    Args:
        example: The ignored counterexample (if known).
        description: Custom description (optional).

    Returns:
        Residual with kind ``counterexample.ignored``.
    """
    if not description:
        if example:
            description = f"Counterexample '{example}' ignored without justification"
        else:
            description = "Counterexample ignored without explicit justification"
    return Residual(kind="counterexample.ignored", description=description)


def make_counterexample_search_incomplete(scope: str = "", description: str = "") -> Residual:
    """Create residual for incomplete counterexample search.

    Args:
        scope: The search scope (e.g., "tested 5 examples").
        description: Custom description (optional).

    Returns:
        Residual with kind ``counterexample.search_incomplete``.

    Example:
        >>> r = make_counterexample_search_incomplete(scope="5 examples")
        >>> r.kind
        'counterexample.search_incomplete'
    """
    if not description:
        if scope:
            description = f"Counterexample search incomplete (scope: {scope}); absence of counterexamples does not prove completeness"
        else:
            description = "Counterexample search incomplete; absence does not equal proof of correctness"
    return Residual(kind="counterexample.search_incomplete", description=description)


def make_refinement_incomplete(description: str = "") -> Residual:
    """Create residual for incomplete refinement.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``refinement.incomplete``.
    """
    if not description:
        description = "Rule refinement incomplete; awaiting verification"
    return Residual(kind="refinement.incomplete", description=description)


def make_evidence_insufficient(description: str = "") -> Residual:
    """Create residual for insufficient evidence.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``evidence.insufficient``.
    """
    if not description:
        description = "Insufficient evidence to support learned rule"
    return Residual(kind="evidence.insufficient", description=description)


def make_overgeneralization(description: str = "") -> Residual:
    """Create residual for suspected over-generalization.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``overgeneralization``.
    """
    if not description:
        description = "Rule may over-generalize; needs constraining examples"
    return Residual(kind="overgeneralization", description=description)


def make_hasty_generalization(count: int = 0, description: str = "") -> Residual:
    """Create residual for hasty generalization.

    Args:
        count: Number of examples used (if known).
        description: Custom description (optional).

    Returns:
        Residual with kind ``hasty_generalization``.
    """
    if not description:
        if count > 0:
            description = f"Rule generalized from only {count} example(s); may be premature"
        else:
            description = "Rule generalized from too few examples"
    return Residual(kind="hasty_generalization", description=description)


def make_overspecialization(description: str = "") -> Residual:
    """Create residual for suspected over-specialization.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``overspecialization``.
    """
    if not description:
        description = "Rule may be over-specialized to training examples"
    return Residual(kind="overspecialization", description=description)


__all__ = [
    "LearningResidual",
    "LEARNING_RESIDUAL_KINDS",
    "make_origin_insufficient",
    "make_origin_conflicting",
    "make_origin_unverified",
    "make_invariant_unclear",
    "make_invariant_unstable",
    "make_invariant_multiple",
    "make_manaat_ambiguous",
    "make_manaat_too_broad",
    "make_manaat_too_narrow",
    "make_counterexample_unresolved",
    "make_counterexample_ignored",
    "make_counterexample_search_incomplete",
    "make_refinement_incomplete",
    "make_evidence_insufficient",
    "make_overgeneralization",
    "make_hasty_generalization",
    "make_overspecialization",
]
