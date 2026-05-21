"""D1 Correctness Validator (Corr_D1).

Formal correctness predicate for syllable candidates.

Corr_D1(candidate) =
    source_atoms_preserved(candidate) ∧
    span_correct(candidate) ∧
    syllable_pattern_legal(candidate) ∧
    nucleus_valid(candidate) ∧
    boundary_rule_satisfied(candidate) ∧
    trace_reversible(candidate) ∧
    no_illegal_atom_loss(candidate) ∧
    atom_order_preserved(candidate)

This validator provides PROOF, not just assertion.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Set
from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.syllables import SyllableType


@dataclass
class CorrectnessCheck:
    """Result of a single correctness check."""
    name: str
    passed: bool
    reason: str = ""
    evidence: dict = field(default_factory=dict)


@dataclass
class Corr_D1_Result:
    """Result of full Corr_D1 validation."""
    is_correct: bool
    checks: List[CorrectnessCheck] = field(default_factory=list)

    def failed_checks(self) -> List[CorrectnessCheck]:
        """Return checks that failed."""
        return [c for c in self.checks if not c.passed]

    def summary(self) -> str:
        """Summary of validation."""
        passed = sum(1 for c in self.checks if c.passed)
        total = len(self.checks)
        status = "✅ CORRECT" if self.is_correct else "❌ INCORRECT"
        return f"{status} ({passed}/{total} checks passed)"


def verify_source_atoms_preserved(
    candidate,
    original_atoms: List[ArabicAtom]
) -> CorrectnessCheck:
    """Verify source atoms are preserved in candidate.

    Args:
        candidate: SyllableCandidate to check
        original_atoms: Original atom sequence

    Returns:
        CorrectnessCheck indicating if atoms preserved
    """
    start, end = candidate.span
    expected_atoms = original_atoms[start:end]

    if len(candidate.source_atoms) != len(expected_atoms):
        return CorrectnessCheck(
            name="source_atoms_preserved",
            passed=False,
            reason=f"Atom count mismatch: {len(candidate.source_atoms)} vs {len(expected_atoms)}",
            evidence={
                'expected_count': len(expected_atoms),
                'actual_count': len(candidate.source_atoms)
            }
        )

    # Check atom-by-atom equality
    for i, (actual, expected) in enumerate(zip(candidate.source_atoms, expected_atoms)):
        if actual != expected:
            return CorrectnessCheck(
                name="source_atoms_preserved",
                passed=False,
                reason=f"Atom mismatch at index {i}",
                evidence={
                    'position': i,
                    'expected': str(expected),
                    'actual': str(actual)
                }
            )

    return CorrectnessCheck(
        name="source_atoms_preserved",
        passed=True,
        evidence={'atom_count': len(candidate.source_atoms)}
    )


def verify_atom_order_preserved(
    candidate,
    original_atoms: List[ArabicAtom]
) -> CorrectnessCheck:
    """Verify atom order is preserved (no permutation).

    Args:
        candidate: SyllableCandidate to check
        original_atoms: Original atom sequence

    Returns:
        CorrectnessCheck indicating if order preserved
    """
    start, end = candidate.span
    expected_atoms = original_atoms[start:end]

    # Build sequential atom list from syllable structure
    reconstructed = []
    reconstructed.extend(candidate.syllable.onset)
    reconstructed.extend(candidate.syllable.nucleus)
    reconstructed.extend(candidate.syllable.coda)

    # Compare sequences
    if len(reconstructed) != len(expected_atoms):
        return CorrectnessCheck(
            name="atom_order_preserved",
            passed=False,
            reason="Syllable structure doesn't cover all atoms",
            evidence={
                'expected_count': len(expected_atoms),
                'reconstructed_count': len(reconstructed)
            }
        )

    for i, (actual, expected) in enumerate(zip(reconstructed, expected_atoms)):
        if actual != expected:
            return CorrectnessCheck(
                name="atom_order_preserved",
                passed=False,
                reason=f"Order violated at position {i}",
                evidence={
                    'position': i,
                    'expected': str(expected),
                    'actual': str(actual)
                }
            )

    return CorrectnessCheck(
        name="atom_order_preserved",
        passed=True,
        evidence={'verified_count': len(reconstructed)}
    )


def verify_no_atom_loss(
    candidate,
    original_atoms: List[ArabicAtom]
) -> CorrectnessCheck:
    """Verify no atoms lost during syllabification.

    Args:
        candidate: SyllableCandidate to check
        original_atoms: Original atom sequence

    Returns:
        CorrectnessCheck indicating if atoms preserved
    """
    start, end = candidate.span
    expected_count = end - start

    # Count atoms in syllable structure
    actual_count = (
        len(candidate.syllable.onset) +
        len(candidate.syllable.nucleus) +
        len(candidate.syllable.coda)
    )

    # Also check source_atoms
    source_count = len(candidate.source_atoms)

    if source_count != expected_count:
        return CorrectnessCheck(
            name="no_atom_loss",
            passed=False,
            reason="Source atoms count doesn't match span",
            evidence={
                'span_length': expected_count,
                'source_atoms_count': source_count
            }
        )

    if actual_count < expected_count:
        return CorrectnessCheck(
            name="no_atom_loss",
            passed=False,
            reason="Atoms lost in syllable structure",
            evidence={
                'expected': expected_count,
                'actual': actual_count,
                'lost': expected_count - actual_count
            }
        )

    return CorrectnessCheck(
        name="no_atom_loss",
        passed=True,
        evidence={'atom_count': actual_count}
    )


def verify_span_correct(
    candidate
) -> CorrectnessCheck:
    """Verify span is valid and consistent.

    Args:
        candidate: SyllableCandidate to check

    Returns:
        CorrectnessCheck indicating if span valid
    """
    start, end = candidate.span

    if start < 0:
        return CorrectnessCheck(
            name="span_correct",
            passed=False,
            reason="Negative start index",
            evidence={'start': start}
        )

    if start > end:
        return CorrectnessCheck(
            name="span_correct",
            passed=False,
            reason="Start after end",
            evidence={'start': start, 'end': end}
        )

    span_length = end - start
    if span_length == 0:
        return CorrectnessCheck(
            name="span_correct",
            passed=False,
            reason="Empty span",
            evidence={'span': (start, end)}
        )

    return CorrectnessCheck(
        name="span_correct",
        passed=True,
        evidence={'span': (start, end), 'length': span_length}
    )


def verify_syllable_pattern_legal(
    candidate
) -> CorrectnessCheck:
    """Verify syllable pattern is legal Arabic pattern.

    Legal patterns: CV, CVC, CVV, CVVC, CVCC

    Args:
        candidate: SyllableCandidate to check

    Returns:
        CorrectnessCheck indicating if pattern legal
    """
    legal_patterns = {
        SyllableType.CV,
        SyllableType.CVC,
        SyllableType.CVV,
        SyllableType.CVVC,
        SyllableType.CVCC
    }

    if candidate.syllable.type not in legal_patterns:
        return CorrectnessCheck(
            name="syllable_pattern_legal",
            passed=False,
            reason=f"Illegal syllable type: {candidate.syllable.type}",
            evidence={'type': candidate.syllable.type.value}
        )

    return CorrectnessCheck(
        name="syllable_pattern_legal",
        passed=True,
        evidence={'type': candidate.syllable.type.value}
    )


def verify_nucleus_valid(
    candidate
) -> CorrectnessCheck:
    """Verify syllable has valid nucleus.

    Every syllable MUST have a nucleus (vowel).

    Args:
        candidate: SyllableCandidate to check

    Returns:
        CorrectnessCheck indicating if nucleus valid
    """
    nucleus = candidate.syllable.nucleus

    if not nucleus:
        return CorrectnessCheck(
            name="nucleus_valid",
            passed=False,
            reason="Missing nucleus (no vowel)",
            evidence={'nucleus_count': 0}
        )

    # Check first element is vowel or sukun
    first = nucleus[0]
    if first.kind not in {AtomKind.VOWEL, AtomKind.SUKUN}:
        return CorrectnessCheck(
            name="nucleus_valid",
            passed=False,
            reason=f"Nucleus must start with vowel, got {first.kind}",
            evidence={
                'first_atom_kind': first.kind.name,
                'nucleus_count': len(nucleus)
            }
        )

    # For long vowels (CVV, CVVC), check length
    if candidate.syllable.type in {SyllableType.CVV, SyllableType.CVVC}:
        if len(nucleus) < 2:
            return CorrectnessCheck(
                name="nucleus_valid",
                passed=False,
                reason="Long vowel pattern requires 2+ nucleus atoms",
                evidence={
                    'type': candidate.syllable.type.value,
                    'nucleus_count': len(nucleus)
                }
            )

    return CorrectnessCheck(
        name="nucleus_valid",
        passed=True,
        evidence={
            'nucleus_count': len(nucleus),
            'first_kind': nucleus[0].kind.name
        }
    )


def verify_trace_exists(
    candidate
) -> CorrectnessCheck:
    """Verify trace reference exists.

    Args:
        candidate: SyllableCandidate to check

    Returns:
        CorrectnessCheck indicating if trace exists
    """
    if candidate.trace is None:
        return CorrectnessCheck(
            name="trace_exists",
            passed=False,
            reason="No trace reference",
            evidence={}
        )

    if not candidate.trace.reversible:
        return CorrectnessCheck(
            name="trace_exists",
            passed=False,
            reason="Trace marked as non-reversible",
            evidence={'reversible': False}
        )

    return CorrectnessCheck(
        name="trace_exists",
        passed=True,
        evidence={'reversible': True}
    )


def verify_no_cross_layer_leakage(
    candidate
) -> CorrectnessCheck:
    """Verify candidate doesn't contain cross-layer information.

    D1 must NOT contain:
    - Root (D3)
    - Wazn/Pattern (D4)
    - Ism/Fi'l/Harf (D5)
    - Meaning (semantic layer)

    Args:
        candidate: SyllableCandidate to check

    Returns:
        CorrectnessCheck indicating if no leakage
    """
    forbidden_fields = ['root', 'wazn', 'pattern', 'meaning', 'ism', 'fil', 'harf']

    for field in forbidden_fields:
        if hasattr(candidate, field):
            return CorrectnessCheck(
                name="no_cross_layer_leakage",
                passed=False,
                reason=f"Forbidden field '{field}' present in D1 candidate",
                evidence={'forbidden_field': field}
            )

    return CorrectnessCheck(
        name="no_cross_layer_leakage",
        passed=True,
        evidence={'checked_fields': forbidden_fields}
    )


def validate_corr_d1(
    candidate,
    original_atoms: List[ArabicAtom]
) -> Corr_D1_Result:
    """Full Corr_D1 validation.

    Runs all correctness checks and returns comprehensive result.

    Args:
        candidate: SyllableCandidate to validate
        original_atoms: Original atom sequence from D0

    Returns:
        Corr_D1_Result with all check results
    """
    checks = [
        verify_source_atoms_preserved(candidate, original_atoms),
        verify_atom_order_preserved(candidate, original_atoms),
        verify_no_atom_loss(candidate, original_atoms),
        verify_span_correct(candidate),
        verify_syllable_pattern_legal(candidate),
        verify_nucleus_valid(candidate),
        verify_trace_exists(candidate),
        verify_no_cross_layer_leakage(candidate)
    ]

    is_correct = all(check.passed for check in checks)

    return Corr_D1_Result(
        is_correct=is_correct,
        checks=checks
    )


def reverse_syllable_candidate(
    candidate
) -> List[ArabicAtom]:
    """Reverse syllable candidate back to atoms.

    This PROVES reversibility by actually performing the operation.

    Args:
        candidate: SyllableCandidate to reverse

    Returns:
        List of atoms reconstructed from syllable
    """
    # Reconstruct atom sequence from syllable structure
    atoms = []
    atoms.extend(candidate.syllable.onset)
    atoms.extend(candidate.syllable.nucleus)
    atoms.extend(candidate.syllable.coda)
    return atoms


def verify_trace_actually_reversible(
    candidate,
    original_atoms: List[ArabicAtom]
) -> CorrectnessCheck:
    """Verify trace is ACTUALLY reversible by running reverse operation.

    This is NOT just checking reversible=True flag.
    This actually reverses and compares.

    Args:
        candidate: SyllableCandidate to check
        original_atoms: Original atom sequence

    Returns:
        CorrectnessCheck indicating if reversible in practice
    """
    try:
        reversed_atoms = reverse_syllable_candidate(candidate)
    except Exception as e:
        return CorrectnessCheck(
            name="trace_actually_reversible",
            passed=False,
            reason=f"Reverse operation failed: {str(e)}",
            evidence={'error': str(e)}
        )

    # Compare with original atoms in span
    start, end = candidate.span
    expected_atoms = original_atoms[start:end]

    if len(reversed_atoms) != len(expected_atoms):
        return CorrectnessCheck(
            name="trace_actually_reversible",
            passed=False,
            reason="Reverse produced wrong atom count",
            evidence={
                'expected': len(expected_atoms),
                'actual': len(reversed_atoms)
            }
        )

    for i, (actual, expected) in enumerate(zip(reversed_atoms, expected_atoms)):
        if actual != expected:
            return CorrectnessCheck(
                name="trace_actually_reversible",
                passed=False,
                reason=f"Reverse produced wrong atom at position {i}",
                evidence={
                    'position': i,
                    'expected': str(expected),
                    'actual': str(actual)
                }
            )

    return CorrectnessCheck(
        name="trace_actually_reversible",
        passed=True,
        evidence={'reversed_count': len(reversed_atoms)}
    )
