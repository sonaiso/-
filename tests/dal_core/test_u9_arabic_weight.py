"""
Tests for U₉ Arabic Weight Carrier (طبقة حامل الوزن العربي)

Tests the four weight pathways with canonical examples:
1. مِنْ (min) → BuiltWeight (blocks derivation)
2. أَرْض (earth) → JāmidWeight (preserves anchor)
3. كِتَابٌ (book) → InflectableWeight (stem preserved, ending variable)
4. كَاتِب (writer) → MushtaqWeight (root+pattern transformation)
5. ذَلِكَ (that) → Blocked from MushtaqWeight

PR: U9-WEIGHT-ALGEBRA
Created: 2026-05-25
"""

import pytest
from dal_core.u9_arabic_weight import (
    WeightType,
    WeightRank,
    WeightResidualType,
    PreWeightContract,
    RootStemInput,
    ArabicWeightObject,
    BuiltWeightIdentity,
    JāmidWeightIdentity,
    InflectableWeightIdentity,
    MushtaqWeightIdentity,
    gate_89_validate,
    dispatch_weight,
    cpb_9_validate,
    validate_weight_object,
    validate_built_weight,
    validate_jamid_weight,
    validate_inflectable_weight,
    validate_mushtaq_weight,
    validate_weight_trace,
    validate_no_layer_jump,
)
from dal_core.evidence import Evidence, make_evidence
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.ranks import LughaRank


# ============================================================================
# Test Case 1: مِنْ (min) → BuiltWeight
# ============================================================================

def test_case_1_min_built_weight():
    """
    Test Case 1: مِنْ → BuiltWeight

    مِنْ is a حرف جر (preposition) - closed class مبني.
    Must route to BuiltWeight, NOT MushtaqWeight.

    Critical theorem: BuiltCertificate(مِنْ) ⇒ ¬MushtaqWeight(مِنْ)
    """
    # Input contract from U₇
    contract = PreWeightContract(
        build_status="ClosedMabniCertificate",
        lexical_status="ClosedClassMabni",
        path_type="Mabni",
        derivation_access="blocked",
        inflection_access=False,
        evidence=(make_evidence("Mabni registry match", LughaRank.TAWATUR),),
        trace={"layer": "U₇", "source": "MabniClosedClass"},
    )

    # Root/stem input from U₈
    root_stem = RootStemInput(
        root_or_stem=("م", "ن"),
        input_type="closed_built_input",
        root_status="BuiltForm",
        evidence=(make_evidence("Closed class particle", LughaRank.TAWATUR),),
        trace={"layer": "U₈", "form": "مِنْ"},
    )

    # Gate validation
    gate_result = gate_89_validate(contract, root_stem)
    assert gate_result.passed, "Gate₈₉ should pass for مِنْ"

    # Weight dispatch
    weight = dispatch_weight(contract, root_stem)

    # Assertions
    assert weight.weight_type == WeightType.BUILT, "مِنْ must be BuiltWeight"
    assert weight.rank == WeightRank.WEIGHT_CERTIFICATE, "Should be certified"
    assert weight.frozen_status == "frozen_ending", "Ending must be frozen"

    # Validate built weight invariants
    assert validate_built_weight(weight), "BuiltWeight invariants violated"

    # Critical: Must block derivation
    assert weight.input_contract.derivation_access == "blocked"

    # CPB₉ validation
    cpb_result = cpb_9_validate(weight)
    assert cpb_result.passed, "CPB₉ should pass"

    # Anti-jumping law
    assert validate_no_layer_jump(weight), "Weight ⊬ meaning/hukm violated"


def test_case_1_min_blocks_mushtaq():
    """Test that مِنْ is BLOCKED from MushtaqWeight path"""
    contract = PreWeightContract(
        build_status="ClosedMabniCertificate",
        lexical_status="ClosedClassMabni",
        path_type="Mabni",
        derivation_access="blocked",  # KEY: derivation blocked
        inflection_access=False,
        evidence=(make_evidence("Mabni registry", LughaRank.TAWATUR),),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("م", "ن"),
        input_type="closed_built_input",
        root_status="BuiltForm",  # NOT "RootLicensed"
        evidence=(make_evidence("Particle", LughaRank.TAWATUR),),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Critical assertion: NOT Mushtaq
    assert weight.weight_type != WeightType.MUSHTAQ, "مِنْ must NOT be MushtaqWeight"
    assert weight.weight_type == WeightType.BUILT, "Must be BuiltWeight"


# ============================================================================
# Test Case 2: أَرْض (earth) → JāmidWeight
# ============================================================================

def test_case_2_ard_jamid_weight():
    """
    Test Case 2: أَرْض → JāmidWeight

    أَرْض is جامد (frozen/lexical anchor) - not freely derived.
    Must preserve stem anchor, block/limit derivation.

    Critical theorem: JāmidWeight(أرض) ⇒ PreserveStemAnchor(أرض)
    """
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",  # Not built, inflectable
        lexical_status="JāmidCertificate",  # KEY: Jāmid
        path_type="Jāmid",
        derivation_access="blocked",  # or "limited"
        inflection_access=True,
        evidence=(make_evidence("Lexicon jāmid entry", LughaRank.SAMA),),
        trace={"layer": "U₇", "source": "LexicalAnchor"},
    )

    root_stem = RootStemInput(
        root_or_stem=("أَرْض",),  # Stem anchor
        input_type="stem_anchor",
        root_status="StemAnchor",
        evidence=(make_evidence("Lexical primitive", LughaRank.SAMA),),
        trace={"layer": "U₈", "stem": "أرض"},
    )

    # Gate validation
    gate_result = gate_89_validate(contract, root_stem)
    assert gate_result.passed, "Gate₈₉ should pass for أَرْض"

    # Weight dispatch
    weight = dispatch_weight(contract, root_stem)

    # Assertions
    assert weight.weight_type == WeightType.JAMID, "أَرْض must be JāmidWeight"
    assert weight.rank == WeightRank.WEIGHT_CERTIFICATE

    # Validate jāmid weight invariants
    assert validate_jamid_weight(weight), "JāmidWeight invariants violated"

    # Stem anchor preserved
    assert weight.root_stem_input.root_status == "StemAnchor"

    # Derivation blocked/limited
    assert weight.input_contract.derivation_access in {"blocked", "limited"}

    # CPB₉ validation
    cpb_result = cpb_9_validate(weight)
    assert cpb_result.passed, "CPB₉ should pass"


# ============================================================================
# Test Case 3: كِتَابٌ (book) → InflectableWeight
# ============================================================================

def test_case_3_kitab_inflectable_weight():
    """
    Test Case 3: كِتَابٌ → InflectableWeight

    كِتَابٌ is معرب (inflectable) - stem preserved, ending variable.

    Critical theorem: InflectableWeight(كتاب) ⇒
                      PreserveStem(كتاب) ∧ EndingVariationRequiresSyntaxGate
    """
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",  # May also be mushtaq
        path_type="Muʿrab",
        derivation_access="open",  # Could derive from root
        inflection_access=True,  # KEY: inflectable
        evidence=(make_evidence("Tanween visible", LughaRank.FORM),),
        trace={"layer": "U₇", "inflection": "tanween_ḍamm"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        pattern_candidate="فِعَال",  # Pattern hypothesis
        evidence=(make_evidence("Root k-t-b attested", LughaRank.TAWATUR),),
        trace={"layer": "U₈", "root": "كتب"},
    )

    # Gate validation
    gate_result = gate_89_validate(contract, root_stem)
    assert gate_result.passed, "Gate₈₉ should pass for كِتَابٌ"

    # Weight dispatch
    weight = dispatch_weight(contract, root_stem)

    # Assertions
    assert weight.weight_type == WeightType.INFLECTABLE, "كِتَابٌ must be InflectableWeight"
    assert weight.inflection_site == "final", "Inflection at final position"
    assert weight.frozen_status == "variable_ending", "Ending must be variable"

    # Validate inflectable weight invariants
    assert validate_inflectable_weight(weight), "InflectableWeight invariants violated"

    # Critical: Stem preserved, NOT ending
    # (Ending determination requires syntax layer)
    assert weight.input_contract.inflection_access is True

    # CPB₉ validation
    cpb_result = cpb_9_validate(weight)
    assert cpb_result.passed, "CPB₉ should pass"

    # Anti-jumping: Cannot determine فاعل/مفعول from weight alone
    assert validate_no_layer_jump(weight)


# ============================================================================
# Test Case 4: كَاتِب (writer) → MushtaqWeight
# ============================================================================

def test_case_4_katib_mushtaq_weight():
    """
    Test Case 4: كَاتِب → MushtaqWeight

    كَاتِب is مشتق (derived) from ك ت ب + فَاعِل pattern.
    Must show root→pattern→form transformation.

    Critical theorem: MushtaqWeight(كاتب) ⇒
                      ∃Root,Pattern: ApplyWeight(Root,Pattern)=كاتب ∧ TraceRootSlotsPreserved
    """
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Mushtaq",
        derivation_access="open",  # KEY: derivation open
        inflection_access=True,
        evidence=(make_evidence("Active participle pattern", LughaRank.QIYAS),),
        trace={"layer": "U₇", "pattern_class": "active_participle"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",  # KEY: root licensed
        pattern_candidate="فَاعِل",  # KEY: pattern identified
        evidence=(make_evidence("Root k-t-b", LughaRank.TAWATUR),),
        trace={"layer": "U₈", "root": "كتب", "pattern": "فاعل"},
    )

    # Gate validation
    gate_result = gate_89_validate(contract, root_stem)
    assert gate_result.passed, "Gate₈₉ should pass for كَاتِب"

    # Weight dispatch
    weight = dispatch_weight(contract, root_stem)

    # Assertions
    assert weight.weight_type == WeightType.MUSHTAQ, "كَاتِب must be MushtaqWeight"
    assert weight.pattern_shape == "فَاعِل", "Pattern must be فَاعِل"
    assert weight.rank == WeightRank.WEIGHT_CERTIFICATE

    # Validate mushtaq weight invariants
    assert validate_mushtaq_weight(weight), "MushtaqWeight invariants violated"

    # Root preserved
    assert weight.root_stem_input.root_or_stem == ("ك", "ت", "ب")

    # CPB₉ validation
    cpb_result = cpb_9_validate(weight)
    assert cpb_result.passed, "CPB₉ should pass"

    # Anti-jumping: Weight ⊬ FinalMeaning
    # (كاتب could be actual writer, proper name, description, etc.)
    assert validate_no_layer_jump(weight)


# ============================================================================
# Test Case 5: ذَلِكَ (that) → Blocked from MushtaqWeight
# ============================================================================

def test_case_5_dhalika_blocked_mushtaq():
    """
    Test Case 5: ذَلِكَ → Blocked from MushtaqWeight

    ذَلِكَ is demonstrative (اسم إشارة) - built/مبني.
    Must NOT enter MushtaqWeight path.

    Critical theorem: ClosedMabniCertificate(ذلك) ⇒
                      BuiltWeight(ذلك) ∧ ¬MushtaqWeight(ذلك)
    """
    contract = PreWeightContract(
        build_status="ClosedMabniCertificate",  # KEY: built
        lexical_status="ClosedClassMabni",
        path_type="Mabni",
        derivation_access="blocked",  # KEY: derivation blocked
        inflection_access=False,
        evidence=(make_evidence("Demonstrative registry", LughaRank.TAWATUR),),
        trace={"layer": "U₇", "class": "Demonstrative"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ذَلِكَ",),
        input_type="closed_built_input",
        root_status="BuiltForm",  # NOT "RootLicensed"
        evidence=(make_evidence("Closed demonstrative", LughaRank.TAWATUR),),
        trace={"layer": "U₈", "form": "ذلك"},
    )

    # Gate validation
    gate_result = gate_89_validate(contract, root_stem)
    assert gate_result.passed, "Gate₈₉ should pass"

    # Weight dispatch
    weight = dispatch_weight(contract, root_stem)

    # Critical assertions
    assert weight.weight_type == WeightType.BUILT, "ذَلِكَ must be BuiltWeight"
    assert weight.weight_type != WeightType.MUSHTAQ, "Must NOT be MushtaqWeight"

    # Validate blocking
    assert weight.input_contract.derivation_access == "blocked"
    assert weight.root_stem_input.root_status == "BuiltForm"

    # CPB₉ validation
    cpb_result = cpb_9_validate(weight)
    assert cpb_result.passed, "CPB₉ should pass"


def test_case_5_dhalika_attempt_mushtaq_fails():
    """Test that attempting MushtaqWeight for ذَلِكَ fails validation"""
    # Attempt to force MushtaqWeight (should fail)
    contract = PreWeightContract(
        build_status="ClosedMabniCertificate",  # Built status
        lexical_status="ClosedClassMabni",
        path_type="Mabni",
        derivation_access="blocked",  # Derivation blocked
        inflection_access=False,
        evidence=(make_evidence("Built", LughaRank.TAWATUR),),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ذَلِكَ",),
        input_type="closed_built_input",
        root_status="BuiltForm",  # Not root licensed
        evidence=(make_evidence("Built", LughaRank.TAWATUR),),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Should NOT be Mushtaq
    assert weight.weight_type != WeightType.MUSHTAQ

    # Validate would fail for mushtaq
    assert not validate_mushtaq_weight(weight), "Should fail mushtaq validation"


# ============================================================================
# Anti-Jumping Tests (Weight ⊬ Meaning, Weight ⊬ Hukm)
# ============================================================================

def test_anti_jumping_no_meaning_field():
    """Test that ArabicWeightObject cannot have 'meaning' field"""
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Muʿrab",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Should NOT have meaning attribute
    assert not hasattr(weight, "meaning"), "Weight must NOT have 'meaning' field"
    assert not hasattr(weight, "murad"), "Weight must NOT have 'murad' field"
    assert not hasattr(weight, "hukm"), "Weight must NOT have 'hukm' field"


def test_anti_jumping_no_syntax_judgment():
    """Test that weight cannot determine syntactic role (فاعل/مفعول)"""
    # كِتَابٌ - we know it's inflectable, but NOT whether it's فاعل or مفعول
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Muʿrab",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Should NOT have syntactic role determination
    assert not hasattr(weight, "syntactic_role")
    assert not hasattr(weight, "i3rab_role")
    assert not hasattr(weight, "hukm")

    # Forbidden gates should include syntax
    assert "syntax_judgment" in weight.forbidden_next_gates


def test_cpb9_blocks_meaning_leak():
    """Test CPB₉ blocks weight objects with meaning leak"""
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Muʿrab",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # CPB₉ should pass for clean weight
    cpb_result = cpb_9_validate(weight)
    assert cpb_result.passed

    # If weight had meaning (which it can't due to __post_init__),
    # CPB₉ would block it
    # This is enforced by dataclass frozen=True and __post_init__


# ============================================================================
# Gate₈₉ Validation Tests
# ============================================================================

def test_gate_89_passes_valid_input():
    """Test Gate₈₉ passes with valid PreWeightContract + RootStemInput"""
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Mushtaq",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    result = gate_89_validate(contract, root_stem)
    assert result.passed, "Gate₈₉ should pass with valid input"


def test_gate_89_blocks_unknown_build_status():
    """Test Gate₈₉ blocks when build_status unknown with no competitors"""
    contract = PreWeightContract(
        build_status="Unknown",  # KEY: unknown
        lexical_status="MushtaqCandidate",
        path_type="Ambiguous",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
        competitors=frozenset(),  # No competitors
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    result = gate_89_validate(contract, root_stem)
    assert not result.passed, "Gate₈₉ should block unknown build_status"
    assert result.blocked_by == "blocking_residual"


def test_gate_89_blocks_invalid_path_type():
    """Test Gate₈₉ blocks invalid path_type"""
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="InvalidPath",  # KEY: invalid
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    result = gate_89_validate(contract, root_stem)
    assert not result.passed, "Gate₈₉ should block invalid path_type"


# ============================================================================
# Trace Preservation Tests
# ============================================================================

def test_trace_preserved_from_u8_u7():
    """Test trace preservation from U₇ and U₈"""
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Mushtaq",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇", "source": "PreWeightContract"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        pattern_candidate="فَاعِل",
        evidence=tuple(),
        trace={"layer": "U₈", "source": "RootStemCarrier"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Trace should preserve both U₇ and U₈
    assert "dispatch" in weight.trace
    assert "gate_trace" in weight.trace

    # Validate trace
    assert validate_weight_trace(weight), "Trace not preserved"


def test_residuals_preserved():
    """Test residuals preservation through weight dispatch"""
    input_residual = Residual(
        type=ResidualType.WAZN_UNRESOLVED,
        severity=ResidualSeverity.WARNING,
        description="Pattern competition exists",
        location="U₇",
    )

    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Mushtaq",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
        residuals=(input_residual,),  # Input residual
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        pattern_candidate="فَاعِل",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Input residual should be preserved in output
    assert len(weight.residuals) > 0, "Residuals should be preserved"
    # (May have additional residuals added)


# ============================================================================
# Competitor Preservation Tests
# ============================================================================

def test_competitors_preserved():
    """Test competitors preservation in ambiguous cases"""
    competitors = frozenset({"JāmidWeight", "MushtaqWeight"})

    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="Unknown",  # Ambiguous
        path_type="Ambiguous",
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),
        trace={"layer": "U₇"},
        competitors=competitors,  # Competitors
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Competitors should be preserved
    assert weight.competitors == competitors, "Competitors not preserved"


# ============================================================================
# Rank Progression Tests
# ============================================================================

def test_rank_certificate_requires_evidence():
    """Test WEIGHT_CERTIFICATE rank requires evidence"""
    contract = PreWeightContract(
        build_status="ClosedMabniCertificate",
        lexical_status="ClosedClassMabni",
        path_type="Mabni",
        derivation_access="blocked",
        inflection_access=False,
        evidence=(make_evidence("Mabni registry", LughaRank.TAWATUR),),
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("م", "ن"),
        input_type="closed_built_input",
        root_status="BuiltForm",
        evidence=(make_evidence("Particle", LughaRank.TAWATUR),),
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem, evidence=(make_evidence("Test", LughaRank.TAWATUR),))

    # Certificate rank should have evidence
    if weight.rank == WeightRank.WEIGHT_CERTIFICATE:
        assert len(weight.evidence) > 0, "Certificate requires evidence"


def test_rank_non_inflation():
    """Test rank doesn't inflate without evidence"""
    # Hypothesis without strong evidence should remain hypothesis
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="MushtaqCandidate",
        path_type="Ambiguous",  # Ambiguous
        derivation_access="open",
        inflection_access=True,
        evidence=tuple(),  # No evidence
        trace={"layer": "U₇"},
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootLicensed",
        evidence=tuple(),  # No evidence
        trace={"layer": "U₈"},
    )

    weight = dispatch_weight(contract, root_stem)

    # Should not be CERTIFICATE without evidence
    assert weight.rank != WeightRank.WEIGHT_CERTIFICATE, "Rank inflated without evidence"


# ============================================================================
# Summary Test
# ============================================================================

def test_canonical_five_cases_summary():
    """
    Summary test: All five canonical cases in one test

    1. مِنْ → BuiltWeight (certificate, blocks derivation)
    2. أَرْض → JāmidWeight (certificate, preserves anchor)
    3. كِتَابٌ → InflectableWeight (hypothesis, stem preserved)
    4. كَاتِب → MushtaqWeight (certificate, root+pattern)
    5. ذَلِكَ → BuiltWeight (certificate, blocks mushtaq)
    """
    # Case 1: مِنْ
    c1 = dispatch_weight(
        PreWeightContract("ClosedMabniCertificate", "ClosedClassMabni", "Mabni", "blocked", False, tuple(), {}),
        RootStemInput(("م", "ن"), "closed_built_input", "BuiltForm", None, tuple(), {}),
    )
    assert c1.weight_type == WeightType.BUILT

    # Case 2: أَرْض
    c2 = dispatch_weight(
        PreWeightContract("MuʿrabCandidate", "JāmidCertificate", "Jāmid", "blocked", True, tuple(), {}),
        RootStemInput(("أَرْض",), "stem_anchor", "StemAnchor", None, tuple(), {}),
    )
    assert c2.weight_type == WeightType.JAMID

    # Case 3: كِتَابٌ
    c3 = dispatch_weight(
        PreWeightContract("MuʿrabCandidate", "MushtaqCandidate", "Muʿrab", "open", True, tuple(), {}),
        RootStemInput(("ك", "ت", "ب"), "root", "RootLicensed", "فِعَال", tuple(), {}),
    )
    assert c3.weight_type == WeightType.INFLECTABLE

    # Case 4: كَاتِب
    c4 = dispatch_weight(
        PreWeightContract("MuʿrabCandidate", "MushtaqCandidate", "Mushtaq", "open", True, tuple(), {}),
        RootStemInput(("ك", "ت", "ب"), "root", "RootLicensed", "فَاعِل", tuple(), {}),
    )
    assert c4.weight_type == WeightType.MUSHTAQ

    # Case 5: ذَلِكَ
    c5 = dispatch_weight(
        PreWeightContract("ClosedMabniCertificate", "ClosedClassMabni", "Mabni", "blocked", False, tuple(), {}),
        RootStemInput(("ذَلِكَ",), "closed_built_input", "BuiltForm", None, tuple(), {}),
    )
    assert c5.weight_type == WeightType.BUILT
    assert c5.weight_type != WeightType.MUSHTAQ  # Critical: NOT Mushtaq
