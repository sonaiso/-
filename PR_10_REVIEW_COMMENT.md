# PR #10 Review: Required Hardening Before Ready for Review

PR #10 is directionally correct and establishes the required bridge between `MufradProof` and future syntax. However, before this PR is moved out of Draft, please harden four points so that the pre-syntax interface does not become an accidental syntax layer.

## Required hardening before Ready for Review

### 1. `allows_operator_consumption()` must be conditional

Do not allow operator consumption merely because a `PreSyntaxMufradVector` exists.

It should return `True` only if:

* source `MufradProof` has acceptable `composition_readiness`
* no blocking residuals
* unresolved competitors do not allow certificate readiness
* required type/morph/surface/case-sign slots are present or explicitly residualized
* trace reaches raw input
* rank obeys weakest-link ceiling

Add tests:

```python
test_presyntax_vector_does_not_allow_operator_consumption_by_default
test_presyntax_vector_rejects_blockers
test_presyntax_vector_rejects_unresolved_competitors_for_certificate
test_presyntax_vector_requires_trace_to_raw_input
```

### 2. `CaseSignPotential` must not become disguised `CaseEffect`

The field `compatible_case_effects=("rafa_candidate", ...)` is acceptable only if these are names of future candidates, not judgments.

Please enforce:

* no operator id inside `CaseSignPotential`
* no `marfoo_by`, `mansub_by`, `majroor_by`, `majzum_by`
* no syntax role
* no final case judgment

Add tests:

```python
test_case_sign_potential_contains_no_operator_binding
test_case_sign_potential_contains_no_final_case_judgment
test_case_sign_potential_contains_no_syntax_role
```

### 3. Type IDs must remain operational, not semantic

`NounTypeID`, `VerbTypeID`, and `ParticleTypeID` must be documented and tested as operator-matching codes, not meanings.

Add tests:

```python
test_type_id_is_operational_code_not_meaning
test_particle_type_id_does_not_emit_semantic_value
test_verb_type_id_does_not_emit_intended_time
```

### 4. PreSyntax rank must not raise MufradProof rank

`PreSyntaxMufradVector` is an extraction interface, not a proof upgrade.

Rank rule:

```text
rank(PreSyntaxMufradVector) <= rank(MufradProof)
```

Add tests:

```python
test_presyntax_vector_rank_cannot_exceed_mufrad_rank
test_presyntax_vector_preserves_mufrad_residuals
test_presyntax_vector_preserves_mufrad_trace
```

## Scientific boundary

**Allowed claim after this PR:**

```text
dal_core can export a governed PreSyntaxMufradVector from MufradProof for future syntax operators.
```

**Forbidden claims:**

```text
dal_core performs syntax.
```

```text
CaseSignPotential is CaseEffect.
```

```text
Operators may consume raw tokens or incomplete MufradProof.
```

Please keep this PR in Draft until the above hardening tests pass.

---

## القرار النهائي

```text
PR #10 = خطوة صحيحة جدًا.
لكن لا يُدمج حتى نضمن أن PreSyntaxMufradVector ليس مجرد data export،
بل بوابة حاكمة تمنع العامل من العمل على مفرد ناقص.
```

بعد تشديد هذه النقاط، يصبح PR #10 صالحًا كأساس مباشر لـ:

```text
PR #11: SentenceFrameProof
PR #12: CaseSignMatrix
PR #13: NahwOperatorRegistry
```
