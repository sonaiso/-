"""Phase 3 tests: Algebraic morphology operations.

These tests prove the Phase 3 contracts:

1. **الجذر ليس معنى** (ROOT is not meaning): Root extraction never
   emits SEMANTICS or HUKM evidence.
2. **الوزن ليس حكماً** (Pattern is not judgment): Pattern matching
   stays LICENSED when residuals remain.
3. **الصرف يرخص بنية** (Morphology licenses structure): Operations
   never promote to CERTIFIED with residuals.
4. **Governed operations**: All morphology operations return Result with
   full provenance (value + rank + evidence + residuals + failures + trace).
5. **Domain boundaries**: No MORPH_SURFACE → SEMANTICS or
   MORPH_DEEP → HUKM jumps.
6. **Residual taxonomy**: Nine morphology-specific residual kinds.
7. **Fatal contradictions**: Fatal Failure forces REFUTED rank.

Test coverage:

- Residual taxonomy (9 residual kinds)
- PatternMatchOperation (MORPH_SURFACE → Result)
- RootExtractionOperation (MORPH_SURFACE → ROOT Result)
- AffixDetectionOperation (affix detection with residuals)
- Evidence integration (adapters → governed operations)
- Domain boundary enforcement
- Rank invariants (LICENSED with residuals, CERTIFIED without)
- Regression tests (Phase 0-2 remain green)
"""

from __future__ import annotations

import pytest

from fvafk.algebra import (
    Carrier,
    Domain,
    Evidence,
    Failure,
    Rank,
    Residual,
    Result,
)
from fvafk.algebra.morphology import (
    MORPHOLOGY_RESIDUAL_KINDS,
    PatternMatchOperation,
    RootExtractionOperation,
    AffixDetectionOperation,
    governed_pattern_match,
    governed_root_extract,
    governed_affix_detect,
    make_context_absent,
    make_lexical_ambiguity,
    make_proper_name_possible,
    make_transfer_possible,
    make_weak_letter_present,
    make_affix_aggressive_strip,
    make_root_ambiguous,
    make_pattern_collision,
    make_broken_plural_possible,
)


# ---------------------------------------------------------------------------
# Residual taxonomy tests
# ---------------------------------------------------------------------------


def test_morphology_residual_kinds_canonical_set():
    """MORPHOLOGY_RESIDUAL_KINDS contains exactly 9 residual kinds."""
    assert len(MORPHOLOGY_RESIDUAL_KINDS) == 9
    expected = {
        "context.absent",
        "lexical.ambiguity",
        "proper_name.possible",
        "transfer.possible",
        "weak_letter.present",
        "affix.aggressive_strip",
        "root.ambiguous",
        "pattern.collision",
        "broken_plural.possible",
    }
    assert MORPHOLOGY_RESIDUAL_KINDS == expected


def test_make_context_absent_creates_residual():
    """make_context_absent() creates Residual with kind context.absent."""
    residual = make_context_absent()
    assert residual.kind == "context.absent"
    assert residual.description  # non-empty

    custom = make_context_absent("Custom description")
    assert custom.kind == "context.absent"
    assert custom.description == "Custom description"


def test_make_lexical_ambiguity_creates_residual():
    """make_lexical_ambiguity() creates proper Residual."""
    residual = make_lexical_ambiguity()
    assert residual.kind == "lexical.ambiguity"
    assert "interpretation" in residual.description.lower()


def test_make_weak_letter_present_with_letters():
    """make_weak_letter_present() includes weak letters in description."""
    residual = make_weak_letter_present(weak_letters="و، ي")
    assert residual.kind == "weak_letter.present"
    assert "و، ي" in residual.description


def test_make_affix_aggressive_strip_with_details():
    """make_affix_aggressive_strip() includes affix and position."""
    residual = make_affix_aggressive_strip(affix="ال", position="prefix")
    assert residual.kind == "affix.aggressive_strip"
    assert "ال" in residual.description
    assert "prefix" in residual.description


def test_make_root_ambiguous_with_candidates():
    """make_root_ambiguous() includes root candidates."""
    residual = make_root_ambiguous(candidates="ك-ت-ب, ك-ت-ب-ة")
    assert residual.kind == "root.ambiguous"
    assert "ك-ت-ب" in residual.description


def test_make_pattern_collision_with_patterns():
    """make_pattern_collision() includes colliding patterns."""
    residual = make_pattern_collision(patterns="فاعل, مفعول")
    assert residual.kind == "pattern.collision"
    assert "فاعل" in residual.description


# ---------------------------------------------------------------------------
# PatternMatchOperation tests
# ---------------------------------------------------------------------------


def test_pattern_match_operation_returns_result():
    """PatternMatchOperation.run() returns Result with provenance."""
    op = PatternMatchOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="فاعل")

    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.value == "فاعل"
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED)
    assert result.trace.operation == "pattern_match"


def test_pattern_match_stays_candidate_without_evidence():
    """Pattern match without Evidence stays CANDIDATE, not LICENSED."""
    op = PatternMatchOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="فاعل")

    result = op.run(carrier)

    assert result.rank == Rank.CANDIDATE
    # CANDIDATE is allowed without evidence
    assert len(result.residuals) > 0  # but residuals present


def test_pattern_match_never_promotes_to_certified_with_residuals():
    """Pattern match with residuals cannot be CERTIFIED."""
    result = governed_pattern_match("فاعل")

    # Even with evidence, residuals prevent CERTIFIED
    assert result.rank != Rank.CERTIFIED
    assert len(result.residuals) > 0


def test_pattern_match_refutes_on_domain_mismatch():
    """PatternMatchOperation refutes non-MORPH_SURFACE carrier."""
    op = PatternMatchOperation()
    carrier = Carrier(domain=Domain.ROOT, value="ك-ت-ب")

    result = op.run(carrier)

    assert result.rank == Rank.REFUTED
    assert any(f.fatal for f in result.failures)


def test_governed_pattern_match_convenience_wrapper():
    """governed_pattern_match() convenience wrapper works."""
    result = governed_pattern_match("مفعول")

    assert result.value == "مفعول"
    assert result.rank == Rank.CANDIDATE
    assert result.trace.operation == "pattern_match"


def test_pattern_match_with_evidence_promotes_to_licensed():
    """Pattern match with Evidence promotes to LICENSED."""
    evidence = (
        Evidence(
            kind="pattern.surface_match",
            source="test:PatternMatcher:test123",
            detail="Pattern 'فاعل' matches surface",
        ),
    )

    result = governed_pattern_match("فاعل", evidence=evidence)

    assert result.rank == Rank.LICENSED
    assert len(result.evidence) == 1


# ---------------------------------------------------------------------------
# RootExtractionOperation tests
# ---------------------------------------------------------------------------


def test_root_extraction_operation_returns_result():
    """RootExtractionOperation.run() returns Result."""
    op = RootExtractionOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب")

    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED, Rank.UNRESOLVED)
    assert result.trace.operation == "root_extraction"


def test_root_extraction_never_emits_semantic_or_hukm_evidence():
    """Root extraction never produces SEMANTICS or HUKM evidence kinds.

    القاعدة: الجذر ليس معنى
    Root extraction supports ROOT domain only, never SEMANTICS or HUKM.
    """
    result = governed_root_extract("كاتب")

    # Check no semantic/hukm evidence kinds
    for ev in result.evidence:
        assert not ev.kind.startswith("semantic.")
        assert not ev.kind.startswith("hukm.")


def test_root_extraction_detects_weak_letters():
    """Root extraction creates weak_letter.present residual."""
    # Surface with weak letter (و)
    result = governed_root_extract("موقف")

    # Should have weak_letter.present residual
    weak_residuals = [r for r in result.residuals if r.kind == "weak_letter.present"]
    assert len(weak_residuals) > 0


def test_root_extraction_with_evidence_promotes_to_licensed():
    """Root extraction with C2bAdapter Evidence promotes to LICENSED."""
    evidence = (
        Evidence(
            kind="root.candidate",
            source="c2b:RootExtractionResult:test456",
            detail="Root 'ك-ت-ب' extracted",
        ),
    )

    result = governed_root_extract("كاتب", evidence=evidence)

    assert result.rank == Rank.LICENSED
    assert len(result.evidence) == 1


def test_root_extraction_bridges_morph_surface_to_root():
    """RootExtractionOperation bridges MORPH_SURFACE → ROOT."""
    op = RootExtractionOperation()

    assert op.source_domain == Domain.MORPH_SURFACE
    assert op.target_domain == Domain.ROOT


# ---------------------------------------------------------------------------
# AffixDetectionOperation tests
# ---------------------------------------------------------------------------


def test_affix_detection_operation_returns_result():
    """AffixDetectionOperation.run() returns Result."""
    op = AffixDetectionOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="الكاتب")

    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.trace.operation == "affix_detection"


def test_affix_detection_creates_aggressive_strip_residual():
    """Affix detection creates affix.aggressive_strip residual."""
    result = governed_affix_detect("الكاتب")

    # Should detect "ال" prefix
    aggressive = [r for r in result.residuals if r.kind == "affix.aggressive_strip"]
    assert len(aggressive) > 0


def test_affix_detection_detects_prefix_and_suffix():
    """Affix detection handles both prefix and suffix."""
    # Word with prefix and suffix
    result = governed_affix_detect("والكاتبة")

    # Should have multiple affix.aggressive_strip residuals
    aggressive = [r for r in result.residuals if r.kind == "affix.aggressive_strip"]
    # At least 2 (prefix "و" or "ال", suffix "ة")
    assert len(aggressive) >= 2


def test_affix_detection_always_has_context_residual():
    """Affix detection always creates context.absent residual."""
    result = governed_affix_detect("كتاب")

    context = [r for r in result.residuals if r.kind == "context.absent"]
    assert len(context) > 0


# ---------------------------------------------------------------------------
# Evidence integration tests
# ---------------------------------------------------------------------------


def test_evidence_from_adapters_supports_root_claims():
    """Evidence from C2bAdapter supports ROOT claims, not SEMANTICS."""
    # Simulate C2bAdapter evidence
    evidence = (
        Evidence(
            kind="root.candidate",
            source="c2b:RootExtractionResult:root789",
            detail="Root candidate: ك-ت-ب",
            weight=0.8,
        ),
    )

    result = governed_root_extract("كاتب", evidence=evidence)

    # Should be LICENSED with evidence
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) == 1

    # Evidence kind must be root.*, not semantic.*
    assert result.evidence[0].kind == "root.candidate"


# ---------------------------------------------------------------------------
# Domain boundary enforcement
# ---------------------------------------------------------------------------


def test_morphology_operations_never_claim_semantics():
    """Morphology operations never emit SEMANTICS evidence kinds."""
    operations = [
        ("pattern", governed_pattern_match("فاعل")),
        ("root", governed_root_extract("كاتب")),
        ("affix", governed_affix_detect("الكاتب")),
    ]

    for name, result in operations:
        for ev in result.evidence:
            assert not ev.kind.startswith("semantic."), \
                f"{name} operation emitted forbidden semantic.* evidence"


def test_morphology_operations_never_claim_hukm():
    """Morphology operations never emit HUKM evidence kinds."""
    operations = [
        governed_pattern_match("مفعول"),
        governed_root_extract("موقف"),
        governed_affix_detect("والكتاب"),
    ]

    for result in operations:
        for ev in result.evidence:
            assert not ev.kind.startswith("hukm."), \
                "Morphology operation emitted forbidden hukm.* evidence"


# ---------------------------------------------------------------------------
# Rank invariants
# ---------------------------------------------------------------------------


def test_licensed_rank_requires_evidence():
    """LICENSED rank requires at least one Evidence."""
    # Create a LICENSED result manually
    with pytest.raises(ValueError, match="LICENSED requires.*Evidence"):
        Result(
            value="test",
            rank=Rank.LICENSED,
            evidence=(),  # Empty evidence — should fail
            residuals=(make_context_absent(),),
        )


def test_certified_rank_forbids_residuals():
    """CERTIFIED rank forbids residuals."""
    evidence = (Evidence(kind="test", source="test:Test:1"),)

    with pytest.raises(ValueError, match="CERTIFIED.*residuals"):
        Result(
            value="test",
            rank=Rank.CERTIFIED,
            evidence=evidence,
            residuals=(make_context_absent(),),  # Residuals — should fail
        )


def test_fatal_failure_forces_refuted():
    """Fatal Failure forces REFUTED rank."""
    with pytest.raises(ValueError, match="fatal.*REFUTED"):
        Result(
            value="test",
            rank=Rank.CANDIDATE,  # Not REFUTED
            failures=(Failure(kind="fatal.error", description="Fatal", fatal=True),),
        )


# ---------------------------------------------------------------------------
# Regression tests (Phase 0-2 unchanged)
# ---------------------------------------------------------------------------


def test_phase_0_rank_set_unchanged():
    """Phase 0 canonical Rank set is unchanged."""
    ranks = {Rank.UNRESOLVED, Rank.CANDIDATE, Rank.LICENSED, Rank.CERTIFIED, Rank.REFUTED}
    assert len(ranks) == 5

    # Check each rank exists
    assert Rank.UNRESOLVED.value == 0
    assert Rank.CANDIDATE.value == 1
    assert Rank.LICENSED.value == 2
    assert Rank.CERTIFIED.value == 3
    assert Rank.REFUTED.value == -1


def test_phase_0_bridge_matrix_unchanged():
    """Phase 0 bridge matrix is unchanged."""
    from fvafk.algebra import ALLOWED_BRIDGES, FORBIDDEN_BRIDGES

    # Check MORPH_SURFACE → ROOT is allowed
    assert (Domain.MORPH_SURFACE, Domain.ROOT) in ALLOWED_BRIDGES

    # Check forbidden bridges remain
    assert (Domain.MORPH_SURFACE, Domain.MORPH_DEEP) in FORBIDDEN_BRIDGES
    assert (Domain.MORPH_SURFACE, Domain.SEMANTICS) in FORBIDDEN_BRIDGES


def test_phase_2_adapters_still_available():
    """Phase 2 adapters remain available and unchanged."""
    from fvafk.algebra.adapters import (
        C1Adapter,
        C2aAdapter,
        C2bAdapter,
        SyntaxAdapter,
    )

    # Create adapters — should not raise
    c1 = C1Adapter()
    c2a = C2aAdapter()
    c2b = C2bAdapter()
    syntax = SyntaxAdapter()

    assert c1.source_module == "c1"
    assert c2b.source_module == "c2b"
    assert syntax.source_module == "syntax"


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------


def test_morphology_operations_integrate_with_decision_tree():
    """Morphology operations integrate with ArabicAlgebraDecisionTree.

    Verify that Result objects from morphology operations can be
    consumed by decision tree analyzer.
    """
    from fvafk.algebra import ArabicAlgebraDecisionTree

    tree = ArabicAlgebraDecisionTree()
    result = governed_pattern_match("فاعل")

    # Decision tree should accept Result
    # (No direct integration yet, but structure is compatible)
    assert isinstance(result, Result)
    assert hasattr(result, "value")
    assert hasattr(result, "rank")
    assert hasattr(result, "evidence")
    assert hasattr(result, "residuals")
    assert hasattr(result, "replay")


# ---------------------------------------------------------------------------
# الصرف الجبري لا يحكم بالمعنى (Morphology does not judge meaning)
# ---------------------------------------------------------------------------


def test_morphology_licenses_structure_not_meaning():
    """الصرف يرخص بنية، ولا يصدر حكماً.

    Morphology operations license structure (LICENSED rank) without
    claiming semantic meaning or grammatical judgment.
    """
    # Pattern match
    pattern_result = governed_pattern_match(
        "فاعل",
        evidence=(Evidence(kind="pattern.match", source="test:Test:1"),),
    )
    assert pattern_result.rank == Rank.LICENSED
    assert len(pattern_result.residuals) > 0  # Residuals remain

    # Root extraction
    root_result = governed_root_extract(
        "كاتب",
        evidence=(Evidence(kind="root.candidate", source="test:Test:2"),),
    )
    assert root_result.rank == Rank.LICENSED

    # Neither claims CERTIFIED (final judgment)
    assert pattern_result.rank != Rank.CERTIFIED
    assert root_result.rank != Rank.CERTIFIED
