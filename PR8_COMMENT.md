PR #8 is directionally correct, but before marking the implementation complete we must add a final hardening layer that explicitly prepares `MufradProof` as the numerical foundation for later syntax operators and case-mark contracts.

The next phase will model the "العوامل النحوية المئة" as ranked `OperatorContract`s and the original/substitute case signs as non-semantic surface/case transition effects. Therefore `MufradProof` must be closed in a way that supports later composition without letting syntax or meaning leak into the singular word proof.

Please implement the following amendments in a follow-up PR.

---

## Required Additions

### 1. **PreSyntaxMufradVector Interface**
Add a typed, non-semantic export interface that later operator contracts can consume. Must NOT include: `meaning`, `semantic`, `madlul`, `murad`, `haqiqa`, `majaz`, `case_effect`, `syntax_role`, `faail`, `mafool`, `mubtada`, `khabar`.

**Test**: `test_presyntax_vector_has_no_semantic_or_syntax_role_fields`

### 2. **CaseSignPotential (not CaseEffect)**
Critical distinction:
- ✅ `CaseSignPotential` is ALLOWED in MufradProof (surface observations)
- ❌ `CaseEffect` is FORBIDDEN in MufradProof (grammatical judgments)

The potential only says: *"This visible or estimated surface sign may later support one or more case effects."*

It must NOT say: *"This word is marfu'/mansub/majrur because of operator X."*

**Tests**:
- `test_case_sign_potential_allowed_in_mufrad`
- `test_case_effect_still_forbidden_in_mufrad`
- `test_original_case_marks_are_surface_potentials_not_case_effects`
- `test_substitute_case_marks_are_surface_potentials_not_case_effects`

### 3. **Model Original and Substitute Signs**
Add enums for:
- **Original**: damma, fatha, kasra, sukun
- **Substitute**: alif, waw, ya, retained/deleted nun, deleted weak letter, fatha substituting kasra, estimated sign

Keep all under `SurfaceEffect/CaseSignPotential`, NOT under `CaseEffect`.

**Residuals**: `MUFRAD_CASE_SIGN_UNRESOLVED`, `MUFRAD_ORIGINAL_SIGN_UNRESOLVED`, `MUFRAD_SUBSTITUTE_SIGN_UNRESOLVED`, `MUFRAD_ESTIMATED_SIGN_REQUIRES_TRACE`

### 4. **OperatorReadiness (not Operator Application)**
Add readiness contract WITHOUT implementing the 100 syntax operators.

Shows whether MufradProof can be consumed by future operator contracts.

**Tests**:
- `test_operator_readiness_requires_mufrad_proof`
- `test_operator_readiness_requires_surface_or_case_sign_potential`
- `test_operator_readiness_rejects_unresolved_competitors_for_certificate`

### 5. **Stub Registry for Future Grammar Operators**
Create placeholder showing operators will be sourced, ranked, and school-bound.

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

Purpose: The hundred grammatical operators are not absolute rules—they are ranked future OperatorContracts.

**Tests**:
- `test_nahw_operator_registry_entry_has_source_school_rank`
- `test_nahw_operator_registry_does_not_apply_to_raw_token`
- `test_nahw_operator_registry_does_not_create_case_effect_inside_mufrad`

### 6. **Enforce Composition-Ready Requirements**
Strengthen: *"Operators consume only composition-ready MufradProof."*

Reject:
- MufradProof with `NOT_READY`
- Unresolved required morph slots
- Unresolved competitors
- Blocker residuals
- Missing trace to raw input

**Tests**:
- `test_operator_rejects_mufrad_not_ready`
- `test_operator_rejects_mufrad_with_unresolved_required_slots`
- `test_operator_rejects_mufrad_with_blockers`
- `test_operator_rejects_mufrad_without_raw_trace`

### 7. **Strengthen Competitor Handling**
Ensure `has_unresolved_competitors()` applies to ALL internal competitions: `root_candidates`, `wazn_candidates`, `derivation_status`, `jamid_mushtaq_status`, `mabni_murab_status`, `definiteness_status`, `gender_status`, `number_status`, `surface_effects/case_sign_potentials`.

**Tests**:
- `test_unresolved_root_competition_blocks_certificate_readiness`
- `test_unresolved_wazn_competition_blocks_certificate_readiness`
- `test_unresolved_mabni_murab_blocks_certificate_readiness`
- `test_unresolved_case_sign_potential_blocks_certificate_readiness`

### 8. **Composition Rank Ceiling Rule**
Add explicit helper:

```python
def composition_rank_ceiling(
    mufrad_nodes: tuple[MufradProof, ...],
    operator_rank: Rank,
    relation_rank: Rank,
) -> Rank:
    # Returns weakest rank
```

**Tests**:
- `test_composition_rank_ceiling_uses_weakest_mufrad`
- `test_composition_rank_ceiling_includes_operator_rank`
- `test_composition_rank_ceiling_includes_relation_rank`

### 9. **Documentation Update**
Add section: *"Why MufradProof must close before nahw operators"*

State clearly:
```text
D_mufrad is the numerical basis of D_murakkab.
Grammar operators work on MufradProof, not tokens.
SurfaceEffect is stored in MufradProof.
CaseEffect is produced only by composition.
MorphFeatures are candidates inside MufradProof.
SyntaxRole is forbidden inside MufradProof.
Composition inherits Mufrad residuals.
Composition cannot raise Mufrad rank.
Composition cannot certify if Mufrad competitors remain unresolved.
```

### 10. **Acceptance Criteria**
Follow-up PR remains Draft until:

1. ✅ All CI checks pass
2. ✅ All existing dal_core tests pass
3. ✅ New tests pass (20+)
4. ✅ No semantic leak
5. ✅ No syntax role leak
6. ✅ No CaseEffect leak
7. ✅ PreSyntaxMufradVector exists
8. ✅ CaseSignPotential exists
9. ✅ OperatorReadiness exists
10. ✅ Operator registry stub exists (source/school/rank-bound, no syntax application)

---

## Final Claims

**✅ Allowed after implementation:**
```text
dal_core produces governed MufradProof ready to be consumed by future syntax
OperatorContracts, preserving morphology, surface effects, case sign potentials,
rank, residuals, trace, and competitors.
```

**❌ Forbidden:**
```text
dal_core performs syntax composition.
dal_core interprets grammatical meaning or murad.
```

---

## الخلاصة

PR #8 جيد، لكنه قبل الاكتمال يحتاج طبقة **PreSyntaxMufradVector + CaseSignPotential + OperatorReadiness**.

هذه هي الجسر الضروري قبل الدخول إلى العوامل النحوية المئة والعلامات الأصلية والفرعية، بدون إدخال المعنى.

---

**Full specification**: See `PR8_HARDENING_REQUIREMENTS.md` and `GITHUB_ISSUE_PR8_HARDENING.md` in the repository root.
