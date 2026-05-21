"""Phase 4 tests: Algebraic syntax operations.

These tests prove the Phase 4 contracts:

1. **النحو يرخص علاقة** (Syntax licenses relations): Syntax operations
   license relational structure, not final meaning.
2. **No SYNTAX → HUKM jump**: Syntax never emits HUKM evidence.
3. **No SYNTAX → SEMANTICS certification**: Syntax with residuals stays
   LICENSED, never CERTIFIED.
4. **Governed operations**: All syntax operations return Result with
   full provenance (value + rank + evidence + residuals + failures + trace).
5. **Domain boundaries**: No SYNTAX → HUKM or uncertified SYNTAX → SEMANTICS
   jumps.
6. **Residual taxonomy**: Ten syntax-specific residual kinds.
7. **Fatal contradictions**: Fatal Failure forces REFUTED rank.

Test coverage:

- Residual taxonomy (10 residual kinds)
- MabniClosedOperatorOperation (مبني operators)
- MurabOpenCarrierOperation (معرب carriers)
- AmilFunctionOperation (عامل functions)
- IrabRelationEffectOperation (إعراب effects)
- NisbahBindingOperation (نسبة bindings)
- Evidence integration (SyntaxAdapter → governed operations)
- Domain boundary enforcement
- Rank invariants (LICENSED with residuals, CERTIFIED without)
- Regression tests (Phase 0-3 remain green)
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
from fvafk.algebra.syntax import (
    SYNTAX_RESIDUAL_KINDS,
    MabniClosedOperatorOperation,
    MurabOpenCarrierOperation,
    AmilFunctionOperation,
    IrabRelationEffectOperation,
    NisbahBindingOperation,
    governed_mabni_operator,
    governed_murab_carrier,
    governed_amil_function,
    governed_irab_effect,
    governed_nisbah_binding,
    make_context_absent,
    make_operator_scope_unresolved,
    make_case_missing,
    make_case_estimated,
    make_case_ambiguous,
    make_governor_ambiguous,
    make_ellipsis_possible,
    make_attachment_ambiguous,
    make_relation_candidate,
    make_word_order_ambiguous,
)


# ---------------------------------------------------------------------------
# Residual taxonomy tests
# ---------------------------------------------------------------------------


def test_syntax_residual_kinds_canonical_set():
    """SYNTAX_RESIDUAL_KINDS contains exactly 10 residual kinds."""
    assert len(SYNTAX_RESIDUAL_KINDS) == 10
    expected = {
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
    }
    assert SYNTAX_RESIDUAL_KINDS == expected


def test_make_context_absent_creates_residual():
    """make_context_absent() creates Residual with kind syntax.context_absent."""
    residual = make_context_absent()
    assert residual.kind == "syntax.context_absent"
    assert residual.description  # non-empty

    custom = make_context_absent("Custom description")
    assert custom.kind == "syntax.context_absent"
    assert custom.description == "Custom description"


def test_make_operator_scope_unresolved_creates_residual():
    """make_operator_scope_unresolved() creates proper Residual."""
    residual = make_operator_scope_unresolved()
    assert residual.kind == "syntax.operator_scope_unresolved"
    assert "scope" in residual.description.lower()

    with_operator = make_operator_scope_unresolved(operator="لم")
    assert with_operator.kind == "syntax.operator_scope_unresolved"
    assert "لم" in with_operator.description


def test_make_case_missing_creates_residual():
    """make_case_missing() creates proper Residual."""
    residual = make_case_missing()
    assert residual.kind == "syntax.case_missing"
    assert "case" in residual.description.lower() or "إعراب" in residual.description


def test_make_case_estimated_creates_residual():
    """make_case_estimated() creates proper Residual."""
    residual = make_case_estimated()
    assert residual.kind == "syntax.case_estimated"
    assert "estimated" in residual.description.lower() or "تقدير" in residual.description


def test_make_case_ambiguous_creates_residual():
    """make_case_ambiguous() creates proper Residual with cases."""
    residual = make_case_ambiguous()
    assert residual.kind == "syntax.case_ambiguous"
    assert "ambiguous" in residual.description.lower()

    with_cases = make_case_ambiguous(cases="رفع/نصب")
    assert with_cases.kind == "syntax.case_ambiguous"
    assert "رفع/نصب" in with_cases.description


def test_make_governor_ambiguous_creates_residual():
    """make_governor_ambiguous() creates proper Residual."""
    residual = make_governor_ambiguous()
    assert residual.kind == "syntax.governor_ambiguous"
    assert "governor" in residual.description.lower() or "عامل" in residual.description


def test_make_ellipsis_possible_creates_residual():
    """make_ellipsis_possible() creates proper Residual."""
    residual = make_ellipsis_possible()
    assert residual.kind == "syntax.ellipsis_possible"
    assert "ellipsis" in residual.description.lower() or "حذف" in residual.description


def test_make_attachment_ambiguous_creates_residual():
    """make_attachment_ambiguous() creates proper Residual."""
    residual = make_attachment_ambiguous()
    assert residual.kind == "syntax.attachment_ambiguous"
    assert "attachment" in residual.description.lower() or "ambiguous" in residual.description.lower()


def test_make_relation_candidate_creates_residual():
    """make_relation_candidate() creates proper Residual."""
    residual = make_relation_candidate()
    assert residual.kind == "syntax.relation_candidate"
    assert "relation" in residual.description.lower()

    with_types = make_relation_candidate(relation_types="ISN/TADMN")
    assert with_types.kind == "syntax.relation_candidate"
    assert "ISN/TADMN" in with_types.description


def test_make_word_order_ambiguous_creates_residual():
    """make_word_order_ambiguous() creates proper Residual."""
    residual = make_word_order_ambiguous()
    assert residual.kind == "syntax.word_order_ambiguous"
    assert "word" in residual.description.lower() or "order" in residual.description.lower()


# ---------------------------------------------------------------------------
# MabniClosedOperatorOperation tests
# ---------------------------------------------------------------------------


def test_mabni_operator_returns_result_with_provenance():
    """MabniClosedOperatorOperation returns Result with full provenance."""
    op = MabniClosedOperatorOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value="لم")
    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.value == "لم"
    assert result.rank == Rank.CANDIDATE  # No evidence yet
    assert len(result.residuals) > 0      # Has residuals
    assert result.trace.operation == "mabni_closed_operator"


def test_mabni_operator_stays_candidate_without_evidence():
    """Mabni operator stays CANDIDATE without Evidence."""
    result = governed_mabni_operator("إن")
    assert result.rank == Rank.CANDIDATE
    assert not result.evidence  # No evidence


def test_mabni_operator_never_certified_with_residuals():
    """Mabni operator never CERTIFIED while residuals remain."""
    result = governed_mabni_operator("لم")
    assert result.rank != Rank.CERTIFIED
    assert len(result.residuals) > 0


def test_mabni_operator_refutes_on_domain_mismatch():
    """Mabni operator refutes if domain is not SYNTAX."""
    op = MabniClosedOperatorOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="لم")
    result = op.run(carrier)

    assert result.rank == Rank.REFUTED
    assert len(result.failures) > 0
    assert any(f.fatal for f in result.failures)


def test_mabni_operator_convenience_wrapper():
    """governed_mabni_operator() convenience wrapper works."""
    result = governed_mabni_operator("لن")
    assert isinstance(result, Result)
    assert result.value == "لن"
    assert result.rank == Rank.CANDIDATE


def test_mabni_operator_promotes_to_licensed_with_evidence():
    """Mabni operator promotes to LICENSED when Evidence present."""
    evidence = (Evidence(kind="syntax.operator", source="test:Test:1"),)
    result = governed_mabni_operator("لا", evidence=evidence)

    assert result.rank == Rank.LICENSED
    assert len(result.evidence) > 0
    assert len(result.residuals) > 0  # Still has residuals


# ---------------------------------------------------------------------------
# MurabOpenCarrierOperation tests
# ---------------------------------------------------------------------------


def test_murab_carrier_returns_result():
    """MurabOpenCarrierOperation returns Result with provenance."""
    op = MurabOpenCarrierOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value="كاتبٌ")
    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.value == "كاتبٌ"
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0


def test_murab_carrier_requires_governor():
    """Mu'rab carrier creates governor_ambiguous residual."""
    result = governed_murab_carrier("الطالبُ")
    assert result.rank == Rank.CANDIDATE

    # Check for governor-related residual
    governor_residuals = [r for r in result.residuals if "governor" in r.kind]
    assert len(governor_residuals) > 0


def test_murab_carrier_detects_missing_case():
    """Mu'rab carrier creates case_missing residual."""
    result = governed_murab_carrier("كتاب")

    # Check for case-related residual
    case_residuals = [r for r in result.residuals if "case" in r.kind]
    assert len(case_residuals) > 0


def test_murab_carrier_promotes_with_evidence():
    """Mu'rab carrier promotes to LICENSED with Evidence."""
    evidence = (Evidence(kind="syntax.murab", source="test:Test:1"),)
    result = governed_murab_carrier("القلمُ", evidence=evidence)

    assert result.rank == Rank.LICENSED
    assert len(result.evidence) > 0


# ---------------------------------------------------------------------------
# AmilFunctionOperation tests
# ---------------------------------------------------------------------------


def test_amil_function_returns_result():
    """AmilFunctionOperation returns Result with provenance."""
    op = AmilFunctionOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value="كان")
    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.value == "كان"
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0


def test_amil_function_needs_governed_element():
    """Amil function creates residuals for governed element."""
    result = governed_amil_function("إن")

    # Check for scope or attachment residuals
    scope_residuals = [
        r for r in result.residuals
        if "scope" in r.kind or "attachment" in r.kind
    ]
    assert len(scope_residuals) > 0


def test_amil_function_never_claims_semantics():
    """Amil function never emits semantic.* evidence."""
    evidence = (Evidence(kind="syntax.amil", source="test:Test:1"),)
    result = governed_amil_function("كان", evidence=evidence)

    for ev in result.evidence:
        assert not ev.kind.startswith("semantic.")
        assert not ev.kind.startswith("hukm.")


# ---------------------------------------------------------------------------
# IrabRelationEffectOperation tests
# ---------------------------------------------------------------------------


def test_irab_effect_returns_result():
    """IrabRelationEffectOperation returns Result with provenance."""
    op = IrabRelationEffectOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value="الكاتبُ")
    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.value == "الكاتبُ"
    assert result.rank == Rank.CANDIDATE


def test_irab_effect_detects_visible_case():
    """I'rab effect detects visible case marks."""
    result = governed_irab_effect("الكاتبُ")  # Has damma

    # Should have case-related residuals
    case_residuals = [r for r in result.residuals if "case" in r.kind]
    assert len(case_residuals) > 0


def test_irab_effect_detects_missing_case():
    """I'rab effect detects missing case marks."""
    result = governed_irab_effect("كتاب")  # No diacritics

    # Should have case_missing and case_estimated residuals
    missing_residuals = [r for r in result.residuals if r.kind == "syntax.case_missing"]
    estimated_residuals = [r for r in result.residuals if r.kind == "syntax.case_estimated"]

    assert len(missing_residuals) > 0
    assert len(estimated_residuals) > 0


def test_irab_effect_is_relational_not_bare_vowel():
    """I'rab effect represents relation, not bare vowel marking."""
    result = governed_irab_effect("الطالبُ")

    # I'rab as relational effect requires context
    context_residuals = [r for r in result.residuals if r.kind == "syntax.context_absent"]
    assert len(context_residuals) > 0


# ---------------------------------------------------------------------------
# NisbahBindingOperation tests
# ---------------------------------------------------------------------------


def test_nisbah_binding_returns_result():
    """NisbahBindingOperation returns Result with provenance."""
    op = NisbahBindingOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value="ISN")
    result = op.run(carrier)

    assert isinstance(result, Result)
    assert result.value == "ISN"
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0


def test_nisbah_binding_creates_relation_candidate_residual():
    """Nisbah binding creates relation_candidate residual."""
    result = governed_nisbah_binding("TADMN")

    relation_residuals = [r for r in result.residuals if r.kind == "syntax.relation_candidate"]
    assert len(relation_residuals) > 0


def test_nisbah_binding_may_license_but_not_certify_with_residuals():
    """Nisbah binding may license SYNTAX but not certify with residuals."""
    evidence = (Evidence(kind="syntax.relation", source="test:Test:1"),)
    result = governed_nisbah_binding("ISN", evidence=evidence)

    assert result.rank == Rank.LICENSED  # Not CERTIFIED
    assert len(result.residuals) > 0     # Has residuals


def test_nisbah_binding_cannot_jump_to_hukm():
    """Nisbah binding never emits hukm.* evidence."""
    evidence = (Evidence(kind="syntax.relation", source="test:Test:1"),)
    result = governed_nisbah_binding("TAQYID", evidence=evidence)

    for ev in result.evidence:
        assert not ev.kind.startswith("hukm.")


# ---------------------------------------------------------------------------
# Evidence integration tests
# ---------------------------------------------------------------------------


def test_evidence_from_syntax_adapter_supports_syntax_claims():
    """Evidence from SyntaxAdapter supports syntax claims."""
    # Simulate SyntaxAdapter evidence
    evidence = (
        Evidence(
            kind="syntax.relation_candidate",
            source="adapter:SyntaxAdapter:1",
            detail="link_type=ISNADI",
        ),
    )

    result = governed_nisbah_binding("ISN", evidence=evidence)
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) > 0


# ---------------------------------------------------------------------------
# Domain boundary enforcement tests
# ---------------------------------------------------------------------------


def test_syntax_operations_never_claim_semantics():
    """Syntax operations never emit semantic.* evidence."""
    evidence = (Evidence(kind="syntax.test", source="test:Test:1"),)

    results = [
        governed_mabni_operator("لم", evidence=evidence),
        governed_murab_carrier("كاتب", evidence=evidence),
        governed_amil_function("كان", evidence=evidence),
        governed_irab_effect("الكتابُ", evidence=evidence),
        governed_nisbah_binding("ISN", evidence=evidence),
    ]

    for result in results:
        for ev in result.evidence:
            assert not ev.kind.startswith("semantic."), \
                f"Operation {result.trace.operation} emitted semantic.* evidence"


def test_syntax_operations_never_claim_hukm():
    """Syntax operations never emit hukm.* evidence."""
    evidence = (Evidence(kind="syntax.test", source="test:Test:1"),)

    results = [
        governed_mabni_operator("لم", evidence=evidence),
        governed_murab_carrier("كاتب", evidence=evidence),
        governed_amil_function("كان", evidence=evidence),
        governed_irab_effect("الكتابُ", evidence=evidence),
        governed_nisbah_binding("ISN", evidence=evidence),
    ]

    for result in results:
        for ev in result.evidence:
            assert not ev.kind.startswith("hukm."), \
                f"Operation {result.trace.operation} emitted hukm.* evidence"


# ---------------------------------------------------------------------------
# Rank invariants tests
# ---------------------------------------------------------------------------


def test_licensed_rank_requires_evidence():
    """LICENSED rank requires at least one Evidence."""
    with pytest.raises(ValueError, match="LICENSED requires at least one Evidence"):
        Result(value="test", rank=Rank.LICENSED, evidence=())


def test_certified_rank_forbids_residuals():
    """CERTIFIED rank forbids residuals."""
    with pytest.raises(ValueError, match="CERTIFIED cannot have residuals"):
        Result(
            value="test",
            rank=Rank.CERTIFIED,
            evidence=(Evidence(kind="test", source="test"),),
            residuals=(Residual(kind="test", description="test"),),
        )


def test_fatal_failure_forces_refuted():
    """Fatal Failure forces REFUTED rank."""
    with pytest.raises(ValueError, match="fatal Failure"):
        Result(
            value="test",
            rank=Rank.CANDIDATE,  # Not REFUTED
            failures=(Failure(kind="error", description="fatal", fatal=True),),
        )


# ---------------------------------------------------------------------------
# Regression tests
# ---------------------------------------------------------------------------


def test_phase0_rank_set_unchanged():
    """Phase 0 Rank set unchanged (5 ranks)."""
    assert len(Rank) == 5
    assert Rank.UNRESOLVED in Rank
    assert Rank.CANDIDATE in Rank
    assert Rank.LICENSED in Rank
    assert Rank.CERTIFIED in Rank
    assert Rank.REFUTED in Rank


def test_phase0_bridge_matrix_unchanged():
    """Phase 0 bridge matrix unchanged."""
    from fvafk.algebra.arabic_layers import ALLOWED_BRIDGES, FORBIDDEN_BRIDGES

    # Basic allowed bridges
    assert (Domain.MORPH_DEEP, Domain.SYNTAX) in ALLOWED_BRIDGES
    assert (Domain.SYNTAX, Domain.SEMANTICS) in ALLOWED_BRIDGES

    # Forbidden jumps
    assert (Domain.MORPH_SURFACE, Domain.SEMANTICS) in FORBIDDEN_BRIDGES
    assert (Domain.MORPH_DEEP, Domain.HUKM) in FORBIDDEN_BRIDGES


def test_phase2_adapters_still_available():
    """Phase 2 adapters still available."""
    from fvafk.algebra.adapters import SyntaxAdapter

    adapter = SyntaxAdapter()
    assert adapter is not None


def test_phase3_morphology_operations_still_available():
    """Phase 3 morphology operations still available."""
    from fvafk.algebra.morphology import (
        governed_pattern_match,
        governed_root_extract,
        governed_affix_detect,
    )

    result = governed_pattern_match("فاعل")
    assert isinstance(result, Result)


# ---------------------------------------------------------------------------
# النحو الجبري test
# ---------------------------------------------------------------------------


def test_syntax_licenses_structure_not_meaning():
    """النحو الجبري يرخص علاقة تركيبية، لا يحكم بالمعنى النهائي.

    Syntax operations license relational structure with residuals.
    They do NOT certify final meaning or jump to HUKM.
    """
    # Operator identification
    operator_result = governed_mabni_operator(
        "لم",
        evidence=(Evidence(kind="syntax.operator", source="test:Test:1"),),
    )
    assert operator_result.rank == Rank.LICENSED  # Not CERTIFIED
    assert len(operator_result.residuals) > 0     # Residuals present

    # Mu'rab carrier
    murab_result = governed_murab_carrier(
        "كاتبٌ",
        evidence=(Evidence(kind="syntax.murab", source="test:Test:1"),),
    )
    assert murab_result.rank == Rank.LICENSED     # Not CERTIFIED
    assert len(murab_result.residuals) > 0        # Residuals present

    # Nisbah binding
    nisbah_result = governed_nisbah_binding(
        "ISN",
        evidence=(Evidence(kind="syntax.relation", source="test:Test:1"),),
    )
    assert nisbah_result.rank == Rank.LICENSED    # Not CERTIFIED
    assert len(nisbah_result.residuals) > 0       # Residuals present

    # No HUKM evidence
    for result in [operator_result, murab_result, nisbah_result]:
        for ev in result.evidence:
            assert not ev.kind.startswith("hukm.")
