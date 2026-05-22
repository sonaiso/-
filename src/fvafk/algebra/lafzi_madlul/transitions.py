"""Algebraic Transitions Between Lafẓī Layers.

Implements the three governing laws for transitions:

1. **Internal Closure Law** (قانون الإغلاق الداخلي):
   No transition before internal algebra completion.

2. **Preservation Law** (قانون الحفظ):
   Every transition preserves trace, rank, and residuals.

3. **No Meaning Jump Law** (قانون منع القفز إلى المعنى):
   No lexical layer produces semantic meaning.

## Constraint-Preserving Binding (CPB)

CPB is the mechanism for transitions. It binds two layers while:
- Preserving constraints from both sources
- NOT generating new semantic meaning
- Accumulating residuals
- Downgrading rank if needed
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Tuple

from ..core import Evidence, Rank, Residual, Trace
from .fractal_algebra import (
    LayerType,
    validate_internal_closure,
    validate_no_meaning_field,
)
from .layer_algebras import (
    AtomAlgebra,
    BuiltFormAlgebra,
    HarakahAlgebra,
    LetterAlgebra,
    PatternTemplateAlgebra,
    RootCandidateAlgebra,
)


# ===========================================================================
# Algebraic Transition
# ===========================================================================


@dataclass(frozen=True)
class AlgebraicTransition:
    """A governed transition between two layers.

    Transitions must satisfy all three governing laws.

    Example::

        transition = AlgebraicTransition(
            source_layer=LayerType.LETTER,
            target_layer=LayerType.ATOM,
            operation="cpb_letter_harakah",
        )

        # Check laws before applying
        if transition.validate_internal_closure(letter_algebra):
            atom = transition.apply(letter_algebra, harakah_algebra)
    """

    source_layer: LayerType
    target_layer: LayerType
    operation: str

    # Transition metadata
    requires_complete_source: bool = True
    preserves_trace: bool = True
    preserves_rank: bool = True
    preserves_residuals: bool = True

    def validate_internal_closure(self, source: Any) -> Tuple[bool, List[str]]:
        """Check if source layer satisfies internal closure.

        Returns:
            (is_closed, incomplete_aspects)
        """
        if not self.requires_complete_source:
            return (True, [])

        return validate_internal_closure(source)

    def validate_no_meaning_jump(self, source: Any, target: Any) -> None:
        """Ensure neither source nor target carries semantic meaning.

        Raises:
            ValueError: If semantic field detected.
        """
        validate_no_meaning_field(source)
        validate_no_meaning_field(target)

    def preserve_trace(self, source_trace: Trace, operation: str) -> Trace:
        """Generate child trace preserving source provenance."""
        return source_trace.child(operation=operation)

    def preserve_rank(self, source_rank: Rank, target_rank: Rank) -> Rank:
        """Preserve rank: result rank ≤ min(source, target)."""
        return min(source_rank, target_rank)

    def preserve_residuals(
        self,
        source_residuals: List[str],
        target_residuals: List[str],
        new_residuals: Optional[List[str]] = None,
    ) -> List[str]:
        """Accumulate residuals from both sources plus new ones."""
        accumulated = list(source_residuals) + list(target_residuals)
        if new_residuals:
            accumulated.extend(new_residuals)
        return accumulated


# ===========================================================================
# Three Governing Laws (Validation Functions)
# ===========================================================================


def internal_closure_law(layer: Any) -> Tuple[bool, List[str]]:
    """Enforce Internal Closure Law.

    قانون الإغلاق الداخلي: لا انتقال قبل اكتمال الجبر الداخلي للطبقة

    No transition before internal algebra completion.

    Args:
        layer: Layer algebra to validate

    Returns:
        (is_complete, incomplete_aspects)

    Example::

        letter = LetterAlgebra.from_form("ك")
        is_complete, missing = internal_closure_law(letter)
        if not is_complete:
            print(f"Cannot transition: {missing}")
    """
    return validate_internal_closure(layer)


def preservation_law(
    source_trace: Trace,
    source_rank: Rank,
    source_residuals: List[str],
    target_trace: Trace,
    target_rank: Rank,
    target_residuals: List[str],
    operation: str,
) -> Tuple[Trace, Rank, List[str]]:
    """Enforce Preservation Law.

    قانون الحفظ: كل انتقال يحفظ الأثر والرتبة والبقايا

    Every transition preserves trace, rank, and residuals.

    Args:
        source_trace: Trace from source layer
        source_rank: Rank from source layer
        source_residuals: Residuals from source layer
        target_trace: Trace from target layer (or base trace)
        target_rank: Rank from target layer
        target_residuals: Residuals from target layer
        operation: Name of the transition operation

    Returns:
        (result_trace, result_rank, result_residuals)

    Example::

        result_trace, result_rank, result_residuals = preservation_law(
            letter.trace, letter.rank, letter.residuals,
            harakah.trace, harakah.rank, harakah.residuals,
            "cpb_letter_harakah",
        )
    """
    # Trace: child of source, referencing both parents
    result_trace = Trace(
        operation=operation,
        source_span=source_trace.source_span,
        parents=(source_trace.trace_id, target_trace.trace_id),
    )

    # Rank: conservative (minimum)
    result_rank = min(source_rank, target_rank)

    # Residuals: accumulate from both
    result_residuals = list(source_residuals) + list(target_residuals)

    return result_trace, result_rank, result_residuals


def no_meaning_jump_law(layer: Any) -> None:
    """Enforce No Meaning Jump Law.

    قانون منع القفز إلى المعنى: لا طبقة لفظية تصدر معنى

    No lexical layer produces semantic meaning.

    Args:
        layer: Layer algebra to validate

    Raises:
        ValueError: If forbidden semantic field detected.

    Example::

        atom = AtomAlgebra(letter=letter, harakah=harakah)
        no_meaning_jump_law(atom)  # Will raise if atom has semantic fields
    """
    validate_no_meaning_field(layer)


# ===========================================================================
# CPB Functions (Constraint-Preserving Binding)
# ===========================================================================


def cpb_letter_harakah(
    letter: LetterAlgebra,
    harakah: HarakahAlgebra,
) -> AtomAlgebra:
    """CPB binding: Letter + Harakah → Atom.

    الربط الحافظ: حرف + حركة → ذرة

    Preserves constraints from both without generating meaning.

    Args:
        letter: Letter algebra
        harakah: Harakah algebra

    Returns:
        AtomAlgebra with preserved properties

    Raises:
        ValueError: If internal closure law violated

    Example::

        letter = LetterAlgebra.from_form("ك")
        harakah = HarakahAlgebra.from_form("َ")
        atom = cpb_letter_harakah(letter, harakah)
        assert atom.letter == letter
        assert atom.harakah == harakah
        assert not hasattr(atom, "meaning")
    """
    # Check internal closure for both inputs
    letter_complete, letter_missing = internal_closure_law(letter)
    if not letter_complete:
        raise ValueError(
            f"Letter algebra incomplete: {letter_missing}. "
            f"Cannot transition to Atom."
        )

    harakah_complete, harakah_missing = internal_closure_law(harakah)
    if not harakah_complete:
        raise ValueError(
            f"Harakah algebra incomplete: {harakah_missing}. "
            f"Cannot transition to Atom."
        )

    # Preserve trace, rank, residuals
    result_trace, result_rank, result_residuals = preservation_law(
        letter.trace,
        letter.rank,
        letter.residuals,
        harakah.trace,
        harakah.rank,
        harakah.residuals,
        operation="cpb_letter_harakah",
    )

    # Build atom preserving both
    atom = AtomAlgebra(
        letter=letter,
        harakah=harakah,
        boundaries={
            "is_letter_from_root": letter.boundaries.get("is_from_root", False),
            "is_harakah_binaa": harakah.boundaries.get("is_binaa", False),
        },
        internal_bindings={
            "letter_harakah_pair": (letter.unit_value, harakah.unit_value),
        },
        rank=result_rank,
        residuals=result_residuals,
        trace=result_trace,
    )

    # Verify no meaning jump
    no_meaning_jump_law(atom)

    return atom


def cpb_root_pattern(
    root: RootCandidateAlgebra,
    pattern: PatternTemplateAlgebra,
) -> BuiltFormAlgebra:
    """CPB binding: Root ⊗ Pattern → BuiltForm.

    الربط الحافظ: جذر ⊗ وزن → صيغة

    Preserves constraints from both without generating meaning.

    **Critical**: Neither root nor pattern carries meaning alone.
    Their combination creates formal structure, not semantic content.

    Args:
        root: Root candidate algebra
        pattern: Pattern template algebra

    Returns:
        BuiltFormAlgebra with preserved properties

    Raises:
        ValueError: If internal closure law violated or meaning leak detected

    Example::

        root = RootCandidateAlgebra(root_letters=("ك", "ت", "ب"))
        pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")
        form = cpb_root_pattern(root, pattern)
        assert form.root == root
        assert form.pattern == pattern
        assert form.surface_form == "كَتَبَ"
        assert not hasattr(form, "meaning")
    """
    # Check internal closure for both inputs
    root_complete, root_missing = internal_closure_law(root)
    if not root_complete:
        raise ValueError(
            f"Root algebra incomplete: {root_missing}. "
            f"Cannot transition to BuiltForm."
        )

    pattern_complete, pattern_missing = internal_closure_law(pattern)
    if not pattern_complete:
        raise ValueError(
            f"Pattern algebra incomplete: {pattern_missing}. "
            f"Cannot transition to BuiltForm."
        )

    # Preserve trace, rank, residuals
    result_trace, result_rank, result_residuals = preservation_law(
        root.trace,
        root.rank,
        root.residuals,
        pattern.trace,
        pattern.rank,
        pattern.residuals,
        operation="cpb_root_pattern",
    )

    # Add new residuals for this level
    new_residuals = []
    if root.rank != Rank.CERTIFIED:
        new_residuals.append("root_unverified")
    if pattern.slot_count != len(root.consonants):
        new_residuals.append("slot_mismatch")

    result_residuals.extend(new_residuals)

    # Apply pattern to root (slot alignment)
    # This is FORMAL application, not semantic
    surface_form = _apply_pattern_to_root(root.consonants, pattern.pattern_form)

    # Build form preserving both
    form = BuiltFormAlgebra(
        root=root,
        pattern=pattern,
        surface_form=surface_form,
        boundaries={
            "root_verified": root.rank == Rank.CERTIFIED,
            "pattern_complete": pattern.is_complete,
        },
        internal_bindings={
            "root_pattern_alignment": _compute_alignment(root, pattern),
        },
        rank=result_rank,
        residuals=result_residuals,
        trace=result_trace,
    )

    # Verify no meaning jump
    no_meaning_jump_law(form)

    return form


# ===========================================================================
# Helper Functions
# ===========================================================================


def _apply_pattern_to_root(root_consonants: Tuple[str, ...], pattern_form: str) -> str:
    """Apply pattern template to root letters (slot alignment).

    This is FORMAL application (string manipulation), not semantic.

    Args:
        root_consonants: Root consonants (e.g., ("ك", "ت", "ب"))
        pattern_form: Pattern template (e.g., "فَعَلَ")

    Returns:
        Surface form after slot substitution (e.g., "كَتَبَ")
    """
    # Map فعل slots to root letters
    slot_map = {
        "ف": root_consonants[0] if len(root_consonants) > 0 else "",
        "ع": root_consonants[1] if len(root_consonants) > 1 else "",
        "ل": root_consonants[2] if len(root_consonants) > 2 else "",
    }

    result = pattern_form
    for slot, letter in slot_map.items():
        result = result.replace(slot, letter)

    return result


def _compute_alignment(
    root: RootCandidateAlgebra,
    pattern: PatternTemplateAlgebra,
) -> str:
    """Compute alignment metadata for root-pattern binding.

    Args:
        root: Root algebra
        pattern: Pattern algebra

    Returns:
        Alignment description string
    """
    return (
        f"root={root.consonants}:"
        f"pattern={pattern.pattern_form}:"
        f"slots={pattern.slot_count}"
    )


__all__ = [
    "AlgebraicTransition",
    "internal_closure_law",
    "preservation_law",
    "no_meaning_jump_law",
    "cpb_letter_harakah",
    "cpb_root_pattern",
]
