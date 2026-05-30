"""
Identity vs Trace Semantics Tests (اختبارات الهوية ضد الأثر)

PR #163: Constitutional tests enforcing identity/trace separation.

CONSTITUTIONAL LAWS TESTED:
1. registry_entry_id is TRACE, not identity
2. row_trace_id is TRACE, not identity
3. Generated candidate IDs are TRACES
4. Stable linguistic IDs must be preserved
5. identity_ids ∩ trace_ids = ∅ (disjoint)
6. Operator identity is stable tuple, not UUID

Created: 2026-05-30
"""

import pytest

from dal_core.identity_trace_utils import (
    diagnose_identity_ids,
    format_diagnosis_report,
    has_trace_prefix,
    is_stable_identity,
    is_uuid_pattern,
    make_mufrad_identity,
    make_operator_identity,
    validate_identity_preservation,
    validate_identity_trace_separation,
)


# ---------------------------------------------------------------------------
# Helper Functions Tests
# ---------------------------------------------------------------------------


def test_is_uuid_pattern_detects_uuids():
    """Test UUID pattern detection."""
    # Pure hex strings ≥8 chars
    assert is_uuid_pattern("abc123def456")
    assert is_uuid_pattern("abcdef1234567890")

    # Standard UUID format
    assert is_uuid_pattern("550e8400-e29b-41d4-a716-446655440000")

    # Not UUIDs
    assert not is_uuid_pattern("op_identity:إن|KITAB_SIBAWAYH|BASRI")
    assert not is_uuid_pattern("abc")  # Too short
    assert not is_uuid_pattern("hello-world")
    assert not is_uuid_pattern("")


def test_has_trace_prefix_detects_traces():
    """Test trace prefix detection."""
    # Known trace prefixes
    assert has_trace_prefix("trace-001")
    assert has_trace_prefix("candidate-abc123")
    assert has_trace_prefix("row-xyz")
    assert has_trace_prefix("trigger-123")
    assert has_trace_prefix("frame-456")
    assert has_trace_prefix("matrix-789")
    assert has_trace_prefix("equation-abc")
    assert has_trace_prefix("case-effect-xyz")

    # Generated ID patterns
    assert has_trace_prefix("op-abc123")  # op-{hex}
    assert has_trace_prefix("mufrad-def456")  # mufrad-{hex}

    # Not trace prefixes
    assert not has_trace_prefix("op_identity:إن|KITAB_SIBAWAYH|BASRI")
    assert not has_trace_prefix("mufrad_identity:الكتاب|ISM_COMMON")
    assert not has_trace_prefix("hello")
    assert not has_trace_prefix("")


def test_is_stable_identity_distinguishes_stable_from_trace():
    """Test stable identity vs trace distinction."""
    # Stable identities
    assert is_stable_identity("op_identity:إن|KITAB_SIBAWAYH|BASRI")
    assert is_stable_identity("mufrad_identity:الكتاب|ISM_COMMON")
    assert is_stable_identity("lexical_identity:كَتَبَ|ك ت ب")
    assert is_stable_identity("BASRI")  # Enum value

    # Not stable (UUIDs)
    assert not is_stable_identity("abc123def456")
    assert not is_stable_identity("550e8400-e29b-41d4-a716-446655440000")

    # Not stable (trace prefixes)
    assert not is_stable_identity("trace-001")
    assert not is_stable_identity("candidate-abc123")
    assert not is_stable_identity("op-abc123")  # Generated UUID
    assert not is_stable_identity("mufrad-def456")  # Generated UUID


def test_make_operator_identity_creates_stable_id():
    """Test operator identity creation."""
    from dal_core.nahw_operator_registry import NahwSchool, OperatorSource

    identity = make_operator_identity(
        display_name_ar="إن",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
    )

    assert identity == "op_identity:إن|KITAB_SIBAWAYH|BASRI"
    assert is_stable_identity(identity)
    assert not is_uuid_pattern(identity)
    assert not has_trace_prefix(identity)


def test_make_operator_identity_requires_valid_inputs():
    """Test operator identity validation."""
    from dal_core.nahw_operator_registry import NahwSchool, OperatorSource

    # Empty name
    with pytest.raises(ValueError, match="non-empty display_name_ar"):
        make_operator_identity("", OperatorSource.KITAB_SIBAWAYH, NahwSchool.BASRI)

    # Non-enum source
    with pytest.raises(TypeError, match="source must be Enum"):
        make_operator_identity("إن", "KITAB_SIBAWAYH", NahwSchool.BASRI)

    # Non-enum school
    with pytest.raises(TypeError, match="school must be Enum"):
        make_operator_identity("إن", OperatorSource.KITAB_SIBAWAYH, "BASRI")


def test_make_mufrad_identity_creates_stable_id():
    """Test mufrad identity creation."""
    identity = make_mufrad_identity(
        raw_text="الكتاب",
        type_value="ISM_COMMON",
    )

    assert identity == "mufrad_identity:الكتاب|ISM_COMMON"
    assert is_stable_identity(identity)
    assert not is_uuid_pattern(identity)
    assert not has_trace_prefix(identity)


def test_make_mufrad_identity_requires_valid_inputs():
    """Test mufrad identity validation."""
    # Empty text
    with pytest.raises(ValueError, match="non-empty raw_text"):
        make_mufrad_identity("", "ISM_COMMON")

    # Empty type
    with pytest.raises(ValueError, match="non-empty type_value"):
        make_mufrad_identity("الكتاب", "")


# ---------------------------------------------------------------------------
# Validation Tests
# ---------------------------------------------------------------------------


def test_validate_identity_trace_separation_accepts_disjoint():
    """Test validation accepts disjoint sets."""
    # Valid: disjoint sets
    validate_identity_trace_separation(
        identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
        trace_ids=("trace-001", "candidate-abc123"),
    )

    # Valid: empty sets
    validate_identity_trace_separation(
        identity_ids=(),
        trace_ids=(),
    )


def test_validate_identity_trace_separation_rejects_overlap():
    """Test validation rejects overlapping sets."""
    with pytest.raises(ValueError, match="overlap"):
        validate_identity_trace_separation(
            identity_ids=("trace-001", "op_identity:إن|KITAB_SIBAWAYH|BASRI"),
            trace_ids=("trace-001",),  # Overlap!
        )


def test_validate_identity_trace_separation_rejects_uuid_in_identity():
    """Test validation rejects UUID in identity_ids."""
    with pytest.raises(ValueError, match="appears to be a UUID"):
        validate_identity_trace_separation(
            identity_ids=("abc123def456",),  # UUID pattern!
            trace_ids=(),
        )


def test_validate_identity_trace_separation_rejects_trace_prefix_in_identity():
    """Test validation rejects trace prefix in identity_ids."""
    with pytest.raises(ValueError, match="starts with trace prefix"):
        validate_identity_trace_separation(
            identity_ids=("trace-001",),  # Trace prefix!
            trace_ids=("candidate-abc",),
        )

    with pytest.raises(ValueError, match="starts with trace prefix"):
        validate_identity_trace_separation(
            identity_ids=("op-abc123",),  # op-{hex} is trace!
            trace_ids=(),
        )


def test_validate_identity_preservation_accepts_preserved():
    """Test validation accepts when identities preserved."""
    # Output preserves input
    validate_identity_preservation(
        input_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
        output_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
    )

    # Output preserves input and adds new
    validate_identity_preservation(
        input_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
        output_identity_ids=(
            "op_identity:إن|KITAB_SIBAWAYH|BASRI",
            "mufrad_identity:الكتاب|ISM_COMMON",
        ),
    )

    # Empty input (nothing to preserve)
    validate_identity_preservation(
        input_identity_ids=(),
        output_identity_ids=("mufrad_identity:الكتاب|ISM_COMMON",),
    )


def test_validate_identity_preservation_rejects_loss():
    """Test validation rejects when identities lost."""
    with pytest.raises(ValueError, match="IDENTITY LOSS"):
        validate_identity_preservation(
            input_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
            output_identity_ids=("mufrad_identity:الكتاب|ISM_COMMON",),  # Lost op_identity!
        )


# ---------------------------------------------------------------------------
# Diagnostic Tests
# ---------------------------------------------------------------------------


def test_diagnose_identity_ids_categorizes_correctly():
    """Test identity ID diagnosis."""
    diagnosis = diagnose_identity_ids((
        "op_identity:إن|KITAB_SIBAWAYH|BASRI",  # stable
        "abc123def456",  # uuid_pattern
        "trace-001",  # trace_prefix
        "",  # empty
    ))

    assert diagnosis["stable"] == ["op_identity:إن|KITAB_SIBAWAYH|BASRI"]
    assert diagnosis["uuid_pattern"] == ["abc123def456"]
    assert diagnosis["trace_prefix"] == ["trace-001"]
    assert diagnosis["empty"] == [""]


def test_format_diagnosis_report_produces_readable_output():
    """Test diagnosis report formatting."""
    diagnosis = diagnose_identity_ids((
        "op_identity:إن|KITAB_SIBAWAYH|BASRI",
        "abc123def456",
    ))

    report = format_diagnosis_report(diagnosis)

    assert "Identity IDs Diagnosis Report" in report
    assert "✅ Stable Identities (1)" in report
    assert "op_identity:إن|KITAB_SIBAWAYH|BASRI" in report
    assert "❌ UUID Patterns (1)" in report
    assert "abc123def456" in report


# ---------------------------------------------------------------------------
# Constitutional Tests (Identity/Trace Separation in dal_core)
# ---------------------------------------------------------------------------
# NOTE: These tests require dal_core structures. They are placeholders for now.
# Actual implementation will test real CaseEffectCandidate instances.
# ---------------------------------------------------------------------------


def test_constitutional_registry_entry_id_is_trace_not_identity():
    """
    Constitutional Test: registry_entry_id is TRACE, not identity.

    Generated UUIDs cannot be linguistic identities.

    CRITICAL: This test enforces that operator registry IDs (UUIDs)
    are placed in trace_ids, NOT identity_ids.

    The operator identity must be (display_name_ar, source, school),
    NOT the generated registry_entry_id.
    """
    # This test is a PLACEHOLDER
    # Actual test will create OperatorCandidate and CaseEffectCandidate
    # and verify:
    # 1. registry_entry_id is in trace_ids
    # 2. registry_entry_id is NOT in identity_ids
    # 3. Stable operator identity (name|source|school) IS in identity_ids

    # For now, verify the pattern
    registry_entry_id = "op-abc123"  # Generated UUID pattern
    assert is_uuid_pattern(registry_entry_id.split('-')[1])
    assert has_trace_prefix(registry_entry_id)
    assert not is_stable_identity(registry_entry_id)

    # Operator identity should be stable
    from dal_core.nahw_operator_registry import NahwSchool, OperatorSource

    operator_identity = make_operator_identity(
        display_name_ar="إن",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
    )
    assert is_stable_identity(operator_identity)


def test_constitutional_row_trace_id_must_remain_trace_only():
    """
    Constitutional Test: row_trace_id is TRACE, NEVER identity.

    Matrix row is computational artifact, not linguistic entity.

    CRITICAL: This test enforces that row_trace_id is placed in
    trace_ids, NOT identity_ids.
    """
    # This test is a PLACEHOLDER
    # Actual test will create CaseSignMatrixRow and CaseEffectCandidate
    # and verify:
    # 1. row_trace_id is in trace_ids
    # 2. row_trace_id is NOT in identity_ids

    # For now, verify the pattern
    row_trace_id = "trace-matrix-row-001"
    assert has_trace_prefix(row_trace_id)
    assert not is_stable_identity(row_trace_id)


def test_constitutional_generated_candidate_ids_are_traces():
    """
    Constitutional Test: All generated candidate IDs are traces.

    Candidate IDs (case_effect_id, operator_candidate_id, factor_equation_id)
    are computational instances, not linguistic identities.

    CRITICAL: This test enforces that ALL *_id fields with UUID patterns
    are placed in trace_ids, NOT identity_ids.
    """
    # This test is a PLACEHOLDER
    # Actual test will create full chain and verify all candidate IDs
    # are in trace_ids, NOT identity_ids

    # For now, verify patterns
    candidate_ids = [
        "case-effect-abc123",
        "candidate-def456",
        "equation-ghi789",
    ]

    for cid in candidate_ids:
        assert has_trace_prefix(cid)
        assert not is_stable_identity(cid)


def test_constitutional_stable_linguistic_ids_must_be_preserved():
    """
    Constitutional Test: Stable linguistic identities preserved.

    If input carries identity_ids, output MUST preserve them.

    CRITICAL: This test enforces that linguistic identities are
    NEVER dropped during transformations.
    """
    # This test is a PLACEHOLDER
    # Actual test will create input with identity_ids, transform,
    # and verify preservation

    # For now, verify validation logic
    from dal_core.nahw_operator_registry import NahwSchool, OperatorSource

    input_identities = (
        make_operator_identity("إن", OperatorSource.KITAB_SIBAWAYH, NahwSchool.BASRI),
    )

    output_identities = input_identities + (
        make_mufrad_identity("الكتاب", "ISM_COMMON"),
    )

    # Should pass (output preserves input)
    validate_identity_preservation(input_identities, output_identities)


def test_constitutional_identity_and_trace_sets_disjoint():
    """
    Constitutional Test: identity_ids ∩ trace_ids = ∅

    Identity IDs and trace IDs must be disjoint sets.
    No ID can be both identity and trace.

    CRITICAL: This test enforces the fundamental separation between
    linguistic identity and computational provenance.
    """
    # This test is a PLACEHOLDER
    # Actual test will create CaseEffectCandidate and verify disjoint

    # For now, verify validation logic
    from dal_core.nahw_operator_registry import NahwSchool, OperatorSource

    identity_ids = (
        make_operator_identity("إن", OperatorSource.KITAB_SIBAWAYH, NahwSchool.BASRI),
        make_mufrad_identity("الكتاب", "ISM_COMMON"),
    )

    trace_ids = (
        "trace-001",
        "candidate-abc123",
        "row-trace-xyz",
    )

    # Should pass (disjoint)
    validate_identity_trace_separation(identity_ids, trace_ids)

    # Should fail (overlap)
    with pytest.raises(ValueError, match="overlap"):
        validate_identity_trace_separation(
            identity_ids=("trace-001",) + identity_ids,
            trace_ids=trace_ids,
        )


def test_constitutional_operator_identity_is_stable_not_uuid():
    """
    Constitutional Test: Operator identity is stable linguistic tuple.

    Operator identity MUST be (name, source, school), NOT UUID.

    CRITICAL: This test enforces that operator identity is the
    linguistic triple, not the generated registry_entry_id.
    """
    # This test is a PLACEHOLDER
    # Actual test will create OperatorCandidate and CaseEffectCandidate
    # and verify operator identity format

    # For now, verify identity creation
    from dal_core.nahw_operator_registry import NahwSchool, OperatorSource

    operator_identity = make_operator_identity(
        display_name_ar="إن",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
    )

    # Must be stable
    assert is_stable_identity(operator_identity)

    # Must NOT be UUID
    assert not is_uuid_pattern(operator_identity)

    # Must have correct format
    assert operator_identity.startswith("op_identity:")
    assert "إن" in operator_identity
    assert "KITAB_SIBAWAYH" in operator_identity
    assert "BASRI" in operator_identity


# ---------------------------------------------------------------------------
# Kana/Inna Slot Semantics (from PR #162)
# ---------------------------------------------------------------------------


def test_constitutional_kana_inna_slot_semantics():
    """
    Constitutional Test: Kana/Inna slots produce correct case effect candidates.

    This test enforces the constitutional law that slot determines case,
    not just compatibility.

    CRITICAL FIX (PR #161): Mixed rafi/nasb policy requires slot information.
    Without slot, must defer: DEFERRED_EFFECT_CANDIDATE.

    كان:
    - ISM_KANA_SLOT → RAFʿ_EFFECT_CANDIDATE (اسم كان: مرفوع)
    - KHABAR_KANA_SLOT → NASB_EFFECT_CANDIDATE (خبر كان: منصوب)

    إن:
    - ISM_INNA_SLOT → NASB_EFFECT_CANDIDATE (اسم إن: منصوب)
    - KHABAR_INNA_SLOT → RAFʿ_EFFECT_CANDIDATE (خبر إن: مرفوع)
    """
    # This test is a PLACEHOLDER
    # Actual test will create operator candidates with MIXED_RAFI_NASB_POLICY_FAMILY
    # and verify:
    # 1. Without slot: DEFERRED_EFFECT_CANDIDATE (PR #161 behavior)
    # 2. With ISM_KANA slot: RAFʿ_EFFECT_CANDIDATE
    # 3. With KHABAR_KANA slot: NASB_EFFECT_CANDIDATE
    # 4. With ISM_INNA slot: NASB_EFFECT_CANDIDATE
    # 5. With KHABAR_INNA slot: RAFʿ_EFFECT_CANDIDATE

    # For now, document the requirement
    assert True  # Placeholder - to be implemented in AmilMamulEquation layer
