# Identity vs Trace Semantics Audit

**Date**: 2026-05-30
**Status**: 🔍 AUDIT IN PROGRESS
**Purpose**: Pre-AmilMamulEquation identity/trace classification
**Branch**: `claude/pr-162-fix-rank-inflation-issue`

---

## Executive Summary

PR #162 resolved rank inflation (`LughaRank.FORM` vs `LughaRank.QIYAS`).
PR #163 resolves **identity vs trace** semantics before `AmilMamulEquation`.

**Critical Question**:
> What preserves **linguistic identity** (ثبات هوية لغوية)?
> What records **computational provenance** (أثر حسابي فقط)?

**Constitutional Law**:
```
identity_id ≠ trace_id
identity_id → linguistic entity that must be preserved
trace_id → computational path that must NOT become identity
```

---

## The Five Questions (from PR #162)

### Question 1: `registry_entry_id` - Identity or Trace?

**Field**: `operator_candidate.registry_entry_id`

**Current Usage** (from PR #161):
```python
# src/dal_core/case_effect_candidate.py:946
identity_ids_set.add(operator_candidate.registry_entry_id)
```

**Analysis**:
- `NahwOperatorEntry.operator_id` is generated: `f"op-{uuid.uuid4().hex[:8]}"`
- `registry_entry_id` references this generated UUID
- Generated IDs are **NOT linguistic identities**
- They are **administrative keys** for registry lookup

**Decision**: **TRACE, NOT IDENTITY**

**Reason**:
- The operator identity is **"إن" as a linguistic entity**, not `op-abc12345`
- The linguistic identity should be: `operator_name_ar` + `source` + `school`
- Example: `("إن", "KITAB_SIBAWAYH", "BASRI")` = linguistic identity
- `registry_entry_id` = computational key for retrieval

**Correction Required**:
```python
# ❌ WRONG (current)
identity_ids_set.add(operator_candidate.registry_entry_id)

# ✅ CORRECT (should be)
# Use linguistic tuple as identity, NOT generated UUID
operator_identity = (
    operator_candidate.registry_entry.display_name_ar,
    operator_candidate.registry_entry.source.value,
    operator_candidate.registry_entry.school.value,
)
identity_ids_set.add(str(operator_identity))  # Stable linguistic identity

# registry_entry_id goes to trace_ids, NOT identity_ids
trace_ids_set.add(operator_candidate.registry_entry_id)
```

---

### Question 2: `operator_id` - Stable or Generated?

**Field**: `NahwOperatorEntry.operator_id`

**Current Implementation**:
```python
# src/dal_core/nahw_operator_registry.py
operator_id: str = field(default_factory=lambda: f"op-{uuid.uuid4().hex[:8]}")
```

**Decision**: **GENERATED TRACE, NOT STABLE IDENTITY**

**Reason**:
- UUIDs are **non-deterministic** across runs
- Cannot be used for linguistic identity (no stability guarantee)
- Purely administrative for registry internal indexing

**Action**: Same as Question 1 — use `(display_name_ar, source, school)` as identity.

---

### Question 3: `mufrad_id` - Identity or Trace?

**Field**: `PreSyntaxMufradVector.mufrad_id`

**Current Usage** (from PR #161):
```python
# src/dal_core/case_effect_candidate.py:948
# Note: affected_vector.mufrad_id is a trace, not an identity
# If affected_vector has explicit identity_ids, add them
if hasattr(affected_vector, 'identity_ids'):
    identity_ids_set.update(affected_vector.identity_ids)
```

**Analysis**:
- `mufrad_id` = `f"mufrad-{uuid.uuid4().hex[:12]}"`
- Generated per vector construction
- Does NOT represent stable linguistic unit

**Decision**: **TRACE, NOT IDENTITY**

**Reason**:
- The linguistic identity of a mufrad is its **lexeme + surface form + type**
- Example: `("الكتاب", "ISM_COMMON")` = linguistic identity
- `mufrad_id` = computational key for this specific vector instance

**However**:
- If `PreSyntaxMufradVector` carries `identity_ids` (from lexical layer), those ARE identities
- The vector itself is a trace container

**Correction**: ✅ Already correct in PR #161

---

### Question 4: `affected_vector.identity_ids` - Always Present?

**Field**: `PreSyntaxMufradVector.identity_ids`

**Current Check**:
```python
if hasattr(affected_vector, 'identity_ids'):
    identity_ids_set.update(affected_vector.identity_ids)
```

**Decision**: **OPTIONAL, NOT ALWAYS PRESENT**

**Reason**:
- `PreSyntaxMufradVector` is pre-lexical layer
- Lexical identities come from **later** `LexicalEntry` layer (U₁₃)
- At pre-syntax stage, we may NOT yet have lexical identities

**Action**: ✅ Already correct — `hasattr` check is appropriate

---

### Question 5: `row_trace_id` - Must Remain Trace Only?

**Field**: `CaseSignMatrixRow.row_trace_id`

**Current Usage** (from PR #161):
```python
# src/dal_core/case_effect_candidate.py:969-970
if hasattr(matrix_row, 'row_trace_id'):
    trace_ids_set.add(matrix_row.row_trace_id)
```

**Decision**: **TRACE ONLY, NEVER IDENTITY**

**Reason**:
- Matrix row is a **computational artifact** (observation + compatibility)
- No linguistic entity corresponds to "this specific row"
- Row identity would be: `(vector_id, sign_observations, compatibility_families)`
- `row_trace_id` = UUID for this computation instance

**Action**: ✅ Already correct — only added to `trace_ids`, not `identity_ids`

---

## Identity vs Trace Classification Table

| Field | Type | Consumer | Reason | Allowed in identity_ids? | Allowed in trace_ids? |
|-------|------|----------|--------|--------------------------|----------------------|
| `registry_entry_id` | **TRACE** | Registry lookup | Generated UUID, non-deterministic | ❌ NO | ✅ YES |
| `operator_id` | **TRACE** | Registry internal | Generated UUID, non-deterministic | ❌ NO | ✅ YES |
| `(display_name_ar, source, school)` | **IDENTITY** | Linguistic reference | Stable operator identity | ✅ YES | ❌ NO |
| `mufrad_id` | **TRACE** | Vector linking | Generated UUID, instance-specific | ❌ NO | ✅ YES |
| `PreSyntaxMufradVector.identity_ids` | **IDENTITY** | Lexical preservation | Stable lexical identities (if available) | ✅ YES | ❌ NO |
| `row_trace_id` | **TRACE** | Matrix computation | Generated UUID, computational artifact | ❌ NO | ✅ YES |
| `factor_source.identity_ids` | **IDENTITY** | Factor linguistic identity | Stable factor identities | ✅ YES | ❌ NO |
| `factor_source.trace_ids` | **TRACE** | Factor provenance | Computational path | ❌ NO | ✅ YES |
| `candidate_id` (any layer) | **TRACE** | Candidate tracking | Generated UUID, instance-specific | ❌ NO | ✅ YES |
| `trigger_id` | **TRACE** | Trigger provenance | Generated UUID, computational | ❌ NO | ✅ YES |
| `frame_id` | **TRACE** | Frame provenance | Generated UUID, computational | ❌ NO | ✅ YES |
| `matrix_id` | **TRACE** | Matrix provenance | Generated UUID, computational | ❌ NO | ✅ YES |

---

## Constitutional Laws

### Law 1: Disjoint Sets
```python
identity_ids ∩ trace_ids = ∅

# Identity IDs and trace IDs MUST be disjoint
# A field cannot be both identity and trace
```

### Law 2: Stability Requirement
```python
# Identity IDs MUST be stable across runs
# Generated UUIDs CANNOT be identities

def is_stable_identity(field_value: str) -> bool:
    """Check if field is stable linguistic identity."""
    # ✅ Stable: tuple of (name, source, school)
    # ✅ Stable: lexeme + type
    # ❌ NOT stable: UUID
    # ❌ NOT stable: timestamp
    # ❌ NOT stable: generated hash
    return not any([
        "uuid" in field_value.lower(),
        re.match(r'^[a-f0-9-]{8,}$', field_value),  # UUID pattern
        field_value.startswith(("trace-", "candidate-", "op-")),
    ])
```

### Law 3: Trace Must Not Become Identity
```python
# Trace IDs MUST NOT leak into identity_ids
# Adding a trace_id to identity_ids is CONSTITUTIONAL VIOLATION

def validate_identity_trace_separation(
    identity_ids: tuple[str, ...],
    trace_ids: tuple[str, ...]
) -> None:
    """Validate identity/trace separation."""
    overlap = set(identity_ids) & set(trace_ids)
    if overlap:
        raise ValueError(
            f"CONSTITUTIONAL VIOLATION: identity_ids and trace_ids overlap: {overlap}"
        )

    for iid in identity_ids:
        if not is_stable_identity(iid):
            raise ValueError(
                f"CONSTITUTIONAL VIOLATION: identity_id '{iid}' is not stable"
            )
```

### Law 4: Identity Preservation
```python
# Linguistic identities MUST be preserved across layers
# If input carries identity_ids, output MUST preserve them

def preserve_identities(
    input_identity_ids: tuple[str, ...],
    output_identity_ids: tuple[str, ...]
) -> None:
    """Verify identity preservation."""
    input_set = set(input_identity_ids)
    output_set = set(output_identity_ids)

    if not input_set.issubset(output_set):
        missing = input_set - output_set
        raise ValueError(
            f"IDENTITY LOSS: Input identities {missing} not preserved in output"
        )
```

---

## Critical Fixes Required

### Fix 1: Operator Identity (URGENT)

**Current** (PR #161):
```python
# ❌ WRONG - Using generated UUID as identity
identity_ids_set.add(operator_candidate.registry_entry_id)
```

**Corrected**:
```python
# ✅ CORRECT - Using stable linguistic identity
operator_identity = make_operator_identity(
    operator_candidate.registry_entry.display_name_ar,
    operator_candidate.registry_entry.source,
    operator_candidate.registry_entry.school,
)
identity_ids_set.add(operator_identity)

# registry_entry_id is trace, not identity
trace_ids_set.add(operator_candidate.registry_entry_id)
```

### Fix 2: Identity Helper Functions

Add to `src/dal_core/identity_trace_utils.py`:
```python
def make_operator_identity(
    display_name_ar: str,
    source: OperatorSource,
    school: NahwSchool,
) -> str:
    """
    Create stable linguistic identity for operator.

    Returns: "op_identity:{name}|{source}|{school}"
    Example: "op_identity:إن|KITAB_SIBAWAYH|BASRI"
    """
    return f"op_identity:{display_name_ar}|{source.value}|{school.value}"


def make_mufrad_identity(
    raw_text: str,
    type_value: str,
) -> str:
    """
    Create stable linguistic identity for mufrad.

    Returns: "mufrad_identity:{text}|{type}"
    Example: "mufrad_identity:الكتاب|ISM_COMMON"
    """
    return f"mufrad_identity:{raw_text}|{type_value}"


def validate_identity_trace_separation(
    identity_ids: tuple[str, ...],
    trace_ids: tuple[str, ...],
) -> None:
    """
    Validate constitutional law: identity_ids ∩ trace_ids = ∅

    Raises:
        ValueError: If identity_ids and trace_ids overlap
        ValueError: If identity_ids contain generated UUIDs
    """
    # Check disjoint
    overlap = set(identity_ids) & set(trace_ids)
    if overlap:
        raise ValueError(
            f"CONSTITUTIONAL VIOLATION: identity_ids and trace_ids overlap: {overlap}. "
            f"Identity IDs and trace IDs must be disjoint sets."
        )

    # Check stability
    import re
    for iid in identity_ids:
        # Check for UUID patterns
        if re.match(r'^[a-f0-9-]{8,}$', iid):
            raise ValueError(
                f"CONSTITUTIONAL VIOLATION: identity_id '{iid}' appears to be a UUID. "
                f"Generated UUIDs cannot be linguistic identities."
            )
        # Check for trace prefixes
        if iid.startswith(("trace-", "candidate-", "op-", "mufrad-", "row-")):
            raise ValueError(
                f"CONSTITUTIONAL VIOLATION: identity_id '{iid}' starts with trace prefix. "
                f"Trace IDs cannot be linguistic identities."
            )
```

---

## Test Requirements

All tests in `tests/dal_core/test_identity_trace_semantics.py`:

### Test 1: Registry Entry ID is Not Identity
```python
def test_registry_entry_id_is_trace_not_identity():
    """
    Constitutional Test: registry_entry_id is trace, NOT identity.

    Generated UUIDs cannot be linguistic identities.
    """
    # Create operator candidate
    # Verify registry_entry_id is in trace_ids
    # Verify registry_entry_id is NOT in identity_ids
    assert registry_entry_id in case_effect.trace_ids
    assert registry_entry_id not in case_effect.identity_ids
```

### Test 2: Row Trace ID Remains Trace Only
```python
def test_row_trace_id_must_remain_trace_only():
    """
    Constitutional Test: row_trace_id is trace, NEVER identity.

    Matrix row is computational artifact, not linguistic entity.
    """
    # Create case effect candidate
    # Verify row_trace_id is in trace_ids
    # Verify row_trace_id is NOT in identity_ids
    assert row_trace_id in case_effect.trace_ids
    assert row_trace_id not in case_effect.identity_ids
```

### Test 3: Generated Candidate IDs are Traces
```python
def test_generated_candidate_ids_are_traces():
    """
    Constitutional Test: All generated candidate IDs are traces.

    Candidate IDs (case_effect_id, operator_candidate_id, etc.)
    are computational instances, not linguistic identities.
    """
    # Create case effect candidate
    # Verify all candidate IDs are in trace_ids
    # Verify all candidate IDs are NOT in identity_ids
    for cid in [case_effect_id, operator_candidate_id, factor_equation_id]:
        assert cid in case_effect.trace_ids or appears_in_chain_traces(cid)
        assert cid not in case_effect.identity_ids
```

### Test 4: Stable Linguistic IDs Preserved
```python
def test_stable_linguistic_ids_must_be_preserved():
    """
    Constitutional Test: Stable linguistic identities preserved.

    If input carries identity_ids, output MUST preserve them.
    """
    # Create input with identity_ids
    # Build case effect candidate
    # Verify all input identity_ids preserved in output identity_ids
    assert set(input_identity_ids).issubset(set(output.identity_ids))
```

### Test 5: Identity and Trace Sets are Disjoint
```python
def test_identity_and_trace_sets_disjoint():
    """
    Constitutional Test: identity_ids ∩ trace_ids = ∅

    Identity IDs and trace IDs must be disjoint sets.
    No ID can be both identity and trace.
    """
    # Create case effect candidate
    # Verify disjoint
    overlap = set(case_effect.identity_ids) & set(case_effect.trace_ids)
    assert overlap == set(), f"Identity/trace overlap: {overlap}"
```

### Test 6: Operator Identity is Stable Tuple
```python
def test_operator_identity_is_stable_not_uuid():
    """
    Constitutional Test: Operator identity is stable linguistic tuple.

    Operator identity MUST be (name, source, school), NOT UUID.
    """
    # Create case effect candidate with operator
    # Extract operator identity from identity_ids
    # Verify format is "op_identity:{name}|{source}|{school}"
    # Verify NOT UUID pattern
    op_identities = [i for i in case_effect.identity_ids if i.startswith("op_identity:")]
    assert len(op_identities) >= 1
    assert not any(re.match(r'^[a-f0-9-]{8,}$', i) for i in op_identities)
```

---

## Kana/Inna Slot Semantics (From PR #162)

**Critical for AmilMamulEquation**:

```python
# Constitutional Law: Slot determines case, NOT compatibility alone

# كان
ISM_KANA_SLOT → RAFʿ_EFFECT_CANDIDATE   # اسم كان: مرفوع
KHABAR_KANA_SLOT → NASB_EFFECT_CANDIDATE # خبر كان: منصوب

# إن
ISM_INNA_SLOT → NASB_EFFECT_CANDIDATE    # اسم إن: منصوب
KHABAR_INNA_SLOT → RAFʿ_EFFECT_CANDIDATE # خبر إن: مرفوع
```

**Why Critical**:
- `MIXED_RAFI_NASB_POLICY_FAMILY` requires **slot information**
- PR #161 correctly defers without slot: `DEFERRED_EFFECT_CANDIDATE`
- AmilMamulEquation MUST provide slot before resolving

**Test Required**:
```python
def test_kana_inna_slot_semantics():
    """
    Constitutional Test: Kana/Inna slots produce correct case effect candidates.

    This test enforces the constitutional law that slot determines case,
    not just compatibility.
    """
    # Create كان operator with MIXED_RAFI_NASB_POLICY_FAMILY
    # Provide ISM_KANA_SLOT → expect RAFʿ_EFFECT_CANDIDATE
    # Provide KHABAR_KANA_SLOT → expect NASB_EFFECT_CANDIDATE

    # Create إن operator with MIXED_RAFI_NASB_POLICY_FAMILY
    # Provide ISM_INNA_SLOT → expect NASB_EFFECT_CANDIDATE
    # Provide KHABAR_INNA_SLOT → expect RAFʿ_EFFECT_CANDIDATE
```

---

## Next Steps

### Immediate Actions (PR #163 Scope)

1. ✅ Create `docs/IDENTITY_VS_TRACE_SEMANTICS.md` (this document)
2. ⏳ Create `src/dal_core/identity_trace_utils.py` with helper functions
3. ⏳ Create `tests/dal_core/test_identity_trace_semantics.py` with 6 tests
4. ⏳ Fix `src/dal_core/case_effect_candidate.py` operator identity handling
5. ⏳ Update `docs/PRE_AMIL_MAMUL_EQUATION_AUDIT_COMPLETE.md` title to qualify scope

### Forbidden (NOT in PR #163 Scope)

❌ Do NOT implement `AmilMamulEquation`
❌ Do NOT implement `AmilMamulFitCandidate`
❌ Do NOT add `RelationCandidate` integration
❌ Do NOT add `IfadahCandidate` layer
❌ Do NOT add `HukmCandidate` layer
❌ Do NOT add slot resolution logic (that belongs in AmilMamulEquation)
❌ Do NOT change `CaseEffectCandidate` behavior beyond identity/trace fix

### After PR #163 Approval

Only then may we proceed with:
- `AmilMamulFitCandidate` (NOT full "equation")
- Use `relation_readiness_family_hint` (NOT `relation_family`)
- Produce `*_EFFECT_CANDIDATE` only (NOT final judgments)

---

## Summary Status

| Audit Area | Status | PR |
|------------|--------|-----|
| Rank Inflation (FORM vs QIYAS) | ✅ COMPLETE | PR #162 |
| LughaRank vs Foundation.Rank | ✅ COMPLETE | PR #162 |
| Identity vs Trace Semantics | 🔍 IN PROGRESS | PR #163 (this) |
| AmilMamulEquation Implementation | ⏸️ PENDING | After PR #163 |

**Correct Formulation**:
```diff
- Pre-AmilMamulEquation Audit: Complete
+ Pre-AmilMamulEquation Rank Audit: ✅ Complete (PR #162)
+ Pre-AmilMamulEquation Identity/Trace Audit: 🔍 In Progress (PR #163)
```

---

**Prepared by**: Claude (Anthropic Code Agent)
**Reviewed by**: [Pending @sonaiso review]
**Approved for AmilMamulEquation**: [Blocked until PR #163 complete]
