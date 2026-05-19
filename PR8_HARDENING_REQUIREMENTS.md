# PR #8 Hardening Requirements: Pre-Syntax Interface Layer

**Reference**: PR #8 (merged) - "Implement MufradProof: composition-ready D_mufrad with morphological and surface proof"

PR #8 is directionally correct, but before marking the implementation complete we must add a final hardening layer that explicitly prepares `MufradProof` as the numerical foundation for later syntax operators and case-mark contracts.

The next phase will model the "العوامل النحوية المئة" as ranked `OperatorContract`s and the original/substitute case signs as non-semantic surface/case transition effects. Therefore `MufradProof` must be closed in a way that supports later composition without letting syntax or meaning leak into the singular word proof.

Please implement the following amendments in a follow-up PR.

---

## 1. Add explicit PreSyntax Interface

Add a typed, non-semantic interface exported from `MufradProof`, for example:

```python
@dataclass(frozen=True)
class PreSyntaxMufradVector:
    mufrad_id: str
    raw_span: tuple[int, int]
    type_value: str
    type_rank: Rank

    mabni_murab_status: CandidateStatus
    noun_inflection_class: CandidateStatus | None
    verb_features: VerbFeatureProof | None
    particle_operator_potential: CandidateStatus | None

    surface_effects: tuple[SurfaceEffect, ...]
    morph_rank: Rank
    final_rank: Rank
    residuals: tuple[Residual, ...]
    trace_id: str
    competitors_count: int
    composition_readiness: CompositionReadiness
```

Purpose:

```text
MufradProof is not merely a dataclass.
It must expose a stable pre-syntax vector that later operator contracts can consume.
```

This vector must not include:

```text
meaning
semantic
madlul
murad
haqiqa
majaz
case_effect
syntax_role
faail
mafool
mubtada
khabar
```

Add a test:

```text
test_presyntax_vector_has_no_semantic_or_syntax_role_fields
```

---

## 2. Add CaseSignPotential, not CaseEffect

Do not put `CaseEffect` in `MufradProof`.

But we need the singular word to preserve original/substitute surface signs so later syntax can interpret them.

Add a proof type such as:

```python
@dataclass(frozen=True)
class CaseSignPotential:
    observed_surface: SurfaceEffect
    sign_family: CaseSignFamily  # ORIGINAL | SUBSTITUTE | BUILDING | ESTIMATED | UNRESOLVED
    sign_value: CaseSignValue    # DAMMA, FATHA, KASRA, SUKUN, ALIF, WAW, YA, NUN_RETAINED, NUN_DELETED, WEAK_LETTER_DELETED, etc.
    compatible_case_effects: tuple[str, ...]  # names only, not applied case judgments
    evidence: Evidence
    rank: Rank
    residuals: tuple[Residual, ...]
    trace: Trace
```

Important distinction:

```text
CaseSignPotential is allowed in MufradProof.
CaseEffect is forbidden in MufradProof.
```

The potential only says:

```text
This visible or estimated surface sign may later support one or more case effects.
```

It must not say:

```text
This word is marfu' / mansub / majrur / majzum because of operator X.
```

Add tests:

```text
test_case_sign_potential_allowed_in_mufrad
test_case_effect_still_forbidden_in_mufrad
test_original_case_marks_are_surface_potentials_not_case_effects
test_substitute_case_marks_are_surface_potentials_not_case_effects
```

---

## 3. Model original and substitute signs explicitly

Add enums or typed constants for:

```text
Original signs:
- damma
- fatha
- kasra
- sukun

Substitute signs:
- alif
- waw
- ya
- retained nun
- deleted nun
- deleted weak letter
- fatha substituting kasra where governed by a later contract
- estimated sign
```

But keep all of these under:

```text
SurfaceEffect / CaseSignPotential
```

not under:

```text
CaseEffect
```

Add residuals:

```text
MUFRAD_CASE_SIGN_UNRESOLVED
MUFRAD_ORIGINAL_SIGN_UNRESOLVED
MUFRAD_SUBSTITUTE_SIGN_UNRESOLVED
MUFRAD_ESTIMATED_SIGN_REQUIRES_TRACE
CASE_SIGN_POTENTIAL_TRACE_MISSING
```

---

## 4. Add Operator Readiness, not Operator Application

This PR must not implement the 100 syntax operators yet.

But it must add a readiness contract showing whether a `MufradProof` can later be consumed by operator contracts.

Add:

```python
@dataclass(frozen=True)
class OperatorReadiness:
    accepts_as_operator_input: bool
    required_slots_present: bool
    missing_slots: tuple[str, ...]
    blocker_residuals: tuple[Residual, ...]
    rank: Rank
    trace: Trace
```

Rules:

```text
operator readiness requires:
- closed form
- closed/ranked lugha
- closed/ranked type
- morph proof present
- surface/case sign potential present or explicitly unresolved with residual
- no blockers
- unresolved competitors must prevent certificate readiness
```

Add tests:

```text
test_operator_readiness_requires_mufrad_proof
test_operator_readiness_requires_surface_or_case_sign_potential
test_operator_readiness_rejects_unresolved_competitors_for_certificate
```

---

## 5. Add a stub registry for future grammar operators

Do not implement full syntax.

But create a placeholder registry interface showing that later operators will be sourced, ranked, and school-bound.

Example:

```python
@dataclass(frozen=True)
class NahwOperatorRegistryEntry:
    operator_id: str
    label: str
    school: str
    source: str
    rank: Rank
    required_input_types: tuple[str, ...]
    expected_surface_policy: str
    forbidden_in_mufrad: bool = True
```

This must remain outside actual `MufradProof` interpretation.

Purpose:

```text
The hundred grammatical operators are not absolute rules.
They are ranked future OperatorContracts with source, school, rank, conditions, residuals.
```

Add tests:

```text
test_nahw_operator_registry_entry_has_source_school_rank
test_nahw_operator_registry_does_not_apply_to_raw_token
test_nahw_operator_registry_does_not_create_case_effect_inside_mufrad
```

---

## 6. Enforce that composition cannot consume incomplete MufradProof

The current PR says operators consume only `MufradProof`. Strengthen it:

```text
Operators consume only composition-ready MufradProof.
```

Add explicit rejection for:

```text
MufradProof with NOT_READY
MufradProof with unresolved required morph slots
MufradProof with unresolved competitors
MufradProof with blocker residuals
MufradProof missing trace to raw input
```

Add tests:

```text
test_operator_rejects_mufrad_not_ready
test_operator_rejects_mufrad_with_unresolved_required_slots
test_operator_rejects_mufrad_with_blockers
test_operator_rejects_mufrad_without_raw_trace
```

---

## 7. Strengthen competitor handling

Current PR mentions `has_unresolved_competitors()`. Please ensure this applies not only to whole `MufradProof` competitors but also to internal competitions:

```text
root_candidates
wazn_candidates
derivation_status
jamid_mushtaq_status
mabni_murab_status
definiteness_status
gender_status
number_status
surface_effects / case sign potentials
```

If any required competition remains unresolved:

```text
composition_readiness cannot be READY_FOR_CERTIFICATE_COMPOSITION
```

Add tests:

```text
test_unresolved_root_competition_blocks_certificate_readiness
test_unresolved_wazn_competition_blocks_certificate_readiness
test_unresolved_mabni_murab_blocks_certificate_readiness
test_unresolved_case_sign_potential_blocks_certificate_readiness
```

---

## 8. Add rank rule for future composition

The PR already says composition never raises rank. Make the rule explicit in a shared helper:

```python
def composition_rank_ceiling(
    mufrad_nodes: tuple[MufradProof, ...],
    operator_rank: Rank,
    relation_rank: Rank,
) -> Rank:
    ...
```

It must return the weakest rank.

Add tests:

```text
test_composition_rank_ceiling_uses_weakest_mufrad
test_composition_rank_ceiling_includes_operator_rank
test_composition_rank_ceiling_includes_relation_rank
```

---

## 9. Add documentation section: "Why MufradProof must close before nahw operators"

Update docs to state:

```text
D_mufrad is the numerical basis of D_murakkab.
The grammar operator does not work on a token.
The grammar operator works on MufradProof.
SurfaceEffect is stored in MufradProof.
CaseEffect is produced only by composition.
MorphFeatures are candidates inside MufradProof.
SyntaxRole is forbidden inside MufradProof.
Composition inherits Mufrad residuals.
Composition cannot raise Mufrad rank.
Composition cannot certify if Mufrad competitors remain unresolved.
```

---

## 10. Required final acceptance before ready-for-review

This follow-up PR should remain Draft until:

```text
1. All CI checks finish successfully.
2. All existing dal_core tests pass.
3. New tests above pass.
4. No semantic leak exists.
5. No syntax role leak exists.
6. No CaseEffect leak exists.
7. PreSyntaxMufradVector exists.
8. CaseSignPotential exists.
9. OperatorReadiness exists.
10. Future nahw operator registry/stub is source/school/rank-bound but does not apply syntax.
```

Final allowed claim after this PR:

```text
dal_core produces a governed MufradProof ready to be consumed by future syntax OperatorContracts, preserving morphology, surface effects, case sign potentials, rank, residuals, trace, and competitors.
```

Forbidden claim:

```text
dal_core performs syntax composition.
```

Forbidden claim:

```text
dal_core interprets grammatical meaning or murad.
```

---

## الخلاصة

PR #8 جيد، لكنه قبل الدمج يحتاج طبقة **PreSyntaxMufradVector + CaseSignPotential + OperatorReadiness**. هذه هي الجسر الضروري قبل الدخول إلى العوامل النحوية المئة والعلامات الأصلية والفرعية، بدون إدخال المعنى.
