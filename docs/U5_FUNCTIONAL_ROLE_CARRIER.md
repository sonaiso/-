# U₅ Functional Role Carrier

## Constitutional Law

**U₅ opens functional role paths. U₅ does NOT certify roles, root, weight, meaning, or hukm.**

```
U₅ يفتح مسارات الأدوار الوظيفية، ولا يشهد بجذر ولا وزن ولا معنى ولا حكم.
```

## Core Principle

U₅ assigns **role candidates**, not **role certificates**:
- Verb surface candidates (not tense)
- Noun surface candidates (not semantic categories)
- Closed-class candidates (not lexicon-certified particles)
- Pronoun candidates (not resolved reference)
- Operator/operand candidates (not grammatical case)

## Architecture

```
U₄ (TrueSingularLafẓ) → U₅ (FunctionalRole) → U₆ (MabniClosedClass)
```

**Input**: U₄ `TrueLafzLayerObject` with surface potentials
**Output**: U₅ `FunctionalRoleLayerObject` with role candidates
**Next Layer**: U₆ MabniClosedClass (closed-class certification)

## Role Candidate Taxonomy

### 1. Closed-Class Role Candidates

```python
class ClosedClassRoleCandidate(Enum):
    HARF_JARR_CANDIDATE = "حرف جر محتمل"              # Preposition candidate
    HARF_ATF_CANDIDATE = "حرف عطف محتمل"              # Conjunction candidate
    HARF_NASB_CANDIDATE = "حرف نصب محتمل"             # Accusative particle
    HARF_JAZM_CANDIDATE = "حرف جزم محتمل"             # Jussive particle
    HARF_NAFY_CANDIDATE = "حرف نفي محتمل"             # Negation
    HARF_ISTIFHAM_CANDIDATE = "حرف استفهام محتمل"    # Interrogative
    PARTICLE_CANDIDATE = "أداة محتملة"                # Generic particle
```

**Source**: U₄ unit_type (BOUND_PROCLITIC) + surface pattern matching
**NOT**: Lexicon-certified particles (requires U₆)

### 2. Pronoun Role Candidates

```python
class PronounRoleCandidate(Enum):
    ATTACHED_PRONOUN_CANDIDATE = "ضمير متصل محتمل"
    DETACHED_PRONOUN_CANDIDATE = "ضمير منفصل محتمل"
    SUBJECT_PRONOUN_CANDIDATE = "ضمير رفع محتمل"
    POSSESSIVE_PRONOUN_CANDIDATE = "ضمير ملكية محتمل"
    GENITIVE_PRONOUN_CANDIDATE = "ضمير جر محتمل"
```

**Source**: U₄ unit_type (ATTACHED_PRONOUN_CANDIDATE) + surface patterns
**NOT**: Resolved reference (that's U₁₅)

### 3. Verb Role Candidates

```python
class VerbRoleCandidate(Enum):
    PAST_VERB_SURFACE_CANDIDATE = "فعل ماض سطحي محتمل"
    PRESENT_VERB_SURFACE_CANDIDATE = "فعل مضارع سطحي محتمل"
    IMPERATIVE_VERB_SURFACE_CANDIDATE = "فعل أمر سطحي محتمل"
    VERBAL_NOUN_CANDIDATE = "مصدر محتمل"
    ACTIVE_PARTICIPLE_CANDIDATE = "اسم فاعل محتمل"
    VERB_SURFACE_CANDIDATE = "مرشح فعلي سطحي"
```

**Source**: U₄ `VerbSurfacePotential` (verb_surface_hint, past/present/imperative hints)
**NOT**: Tense certificates, aspect, mood (that's U₇+)

### 4. Noun Role Candidates

```python
class NounRoleCandidate(Enum):
    NOUN_SURFACE_CANDIDATE = "اسم سطحي محتمل"
    DEFINITE_NOUN_CANDIDATE = "اسم معرف سطحي محتمل"
    INDEFINITE_NOUN_CANDIDATE = "اسم نكرة سطحي محتمل"
    DUAL_NOUN_CANDIDATE = "مثنى سطحي محتمل"
    PLURAL_NOUN_CANDIDATE = "جمع سطحي محتمل"
    SINGULAR_NOUN_CANDIDATE = "مفرد سطحي محتمل"
```

**Source**: U₄ `DefinitenessSurfacePotential` + `QuantitySurfacePotential`
**NOT**: Semantic noun categories, counted reality (that's U₁₅)

### 5. Operator/Operand Candidates

```python
class OperatorRoleCandidate(Enum):
    OPERATOR_CANDIDATE = "عامل محتمل"
    OPERAND_CANDIDATE = "معمول محتمل"
    GOVERNOR_CANDIDATE = "حاكم محتمل"
    GOVERNED_CANDIDATE = "محكوم محتمل"
```

**Source**: Future implementation (compositional analysis)
**NOT**: Grammatical case assignment (that's U₇+)

## Examples

### Example 1: كَتَبَ (Past Verb)

**U₄ Input**:
```python
TrueLafzUnit(
    surface="كَتَبَ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,
    verb_surface_potential=VerbSurfacePotential(
        verb_surface_hint="possible",
        past_surface_hint="possible"
    )
)
```

**U₅ Output**:
```python
FunctionalRoleUnit(
    surface="كَتَبَ",
    role_candidates=[
        VERB_SURFACE_CANDIDATE (surface_support=0.6),
        PAST_VERB_SURFACE_CANDIDATE (surface_support=0.7),
        SINGULAR_NOUN_CANDIDATE (surface_support=0.6)  # Ambiguity
    ]
)
```

**Note**: Both verb AND noun candidates present. Disambiguation requires evidence.

### Example 2: بِكِتَابٍ (Preposition + Indefinite Noun)

**U₄ Input**:
```python
# Unit 1: بِ
TrueLafzUnit(
    surface="بِ",
    unit_type=BOUND_PROCLITIC
)

# Unit 2: كِتَابٍ
TrueLafzUnit(
    surface="كِتَابٍ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,
    definiteness_surface_potential=DefinitenessSurfacePotential(
        has_tanwin_surface=True,
        indefinite_surface_hint="possible"
    )
)
```

**U₅ Output**:
```python
# Unit 1: بِ
FunctionalRoleUnit(
    surface="بِ",
    role_candidates=[
        HARF_JARR_CANDIDATE (surface_support=0.8)
    ]
)

# Unit 2: كِتَابٍ
FunctionalRoleUnit(
    surface="كِتَابٍ",
    role_candidates=[
        NOUN_SURFACE_CANDIDATE (surface_support=0.6),
        INDEFINITE_NOUN_CANDIDATE (surface_support=0.7),
        SINGULAR_NOUN_CANDIDATE (surface_support=0.6)
    ]
)
```

### Example 3: وَبِكِتَابِهِمْ (Complex Composition)

**U₄ Input**: 4 units [وَ, بِ, كِتَابِ, ـهِمْ]

**U₅ Output**:
```python
# وَ
FunctionalRoleUnit(
    surface="وَ",
    role_candidates=[HARF_ATF_CANDIDATE (surface_support=0.9)]
)

# بِ
FunctionalRoleUnit(
    surface="بِ",
    role_candidates=[HARF_JARR_CANDIDATE (surface_support=0.8)]
)

# كِتَابِ
FunctionalRoleUnit(
    surface="كِتَابِ",
    role_candidates=[NOUN_SURFACE_CANDIDATE, ...]
)

# ـهِمْ
FunctionalRoleUnit(
    surface="ـهِمْ",
    role_candidates=[
        ATTACHED_PRONOUN_CANDIDATE (surface_support=0.9),
        GENITIVE_PRONOUN_CANDIDATE (surface_support=0.7)
    ]
)
```

## Candidate vs Certificate

**Critical Law**: All U₅ assignments are **candidates**, not **certificates**.

```python
@dataclass(frozen=True)
class FunctionalRoleCandidate:
    uid: str
    role: Enum  # Role type (verb, noun, particle, etc.)
    sort: RoleSort  # Category (VERB_CANDIDATE, NOUN_CANDIDATE, etc.)
    surface_support: float  # [0.0, 1.0] - Surface evidence strength, NOT epistemic certificate
    evidence: Tuple[str, ...]  # Why this candidate
    source_u4_unit_id: str  # Trace to U₄
    residuals: FrozenSet[Residual]
    rank: Rank  # Always CANDIDATE at U₅
```

**Certification requires**:
1. Evidence blocking competitors
2. Rank progression: CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE
3. Later layers (U₆+) with more context

## Forbidden Fields

U₅ MUST NOT contain:

### Morphological (U₈/U₉)
- `root`
- `weight`
- `pattern`

### Semantic (U₁₅)
- `meaning`
- `dalālah`
- `haqīqa_majāz`

### Syntactic (U₇+)
- `hukm`
- `iʿrāb_status`
- `case_marking`
- `mood_marking`

### Reference (U₁₅)
- `resolved_reference`
- `referent`

### Quantity (U₁₅)
- `counted_entities`

### Verbal (U₇+)
- `tense` (certificate)
- `voice`
- `valency`
- `aspect`

## CPB₅ - Completeness Predicate

```python
@dataclass(frozen=True)
class CPB5:
    @staticmethod
    def is_complete(layer_obj: FunctionalRoleLayerObject) -> bool:
        """Check completeness."""
        if not layer_obj.units:
            return False
        if not layer_obj.source_lafz_layer_id:
            return False
        # Check no forbidden fields
        for unit in layer_obj.units:
            for candidate in unit.role_candidates:
                if hasattr(candidate, 'root') or hasattr(candidate, 'weight'):
                    return False
        return True

    @staticmethod
    def build_proof(layer_obj: FunctionalRoleLayerObject) -> ProofObject:
        """Build proof with guards."""
        return make_proof_object(
            claim="U₅ functional role candidate paths opened",
            allowed_next_gates=frozenset({"mabni_closed_class_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
            limitations=frozenset([
                "no_root_extraction",
                "no_weight_determination",
                "candidates_not_certificates",
            ])
        )
```

## Evidence Model

All role candidates must have evidence tracing to U₄:

```python
# Example: Verb candidate evidence
FunctionalRoleCandidate(
    role=PAST_VERB_SURFACE_CANDIDATE,
    evidence=(
        "u4_past_surface_hint_possible",  # From U₄ VerbSurfacePotential
    )
)

# Example: Noun candidate evidence
FunctionalRoleCandidate(
    role=INDEFINITE_NOUN_CANDIDATE,
    evidence=(
        "u4_indefinite_surface_hint_possible",
        "has_tanwin=True"  # From U₄ DefinitenessSurfacePotential
    )
)

# Example: Particle candidate evidence
FunctionalRoleCandidate(
    role=HARF_JARR_CANDIDATE,
    evidence=(
        "surface_match_preposition",
        "surface=بِ"  # Surface pattern matching
    )
)
```

## Usage

```python
from dal_core.u5_functional_role_carrier import functional_role_5

# After U₀→U₁→U₂p→U₂s→U₃→U₄ pipeline
u4_result = true_lafz_4(boundary_layer)

# Assign functional role candidates
u5_result = functional_role_5(u4_result.layer_object)

if u5_result.success:
    for unit in u5_result.layer_object.units:
        print(f"Surface: {unit.surface}")
        for candidate in unit.role_candidates:
            print(f"  - {candidate.role.value} (surface_support={candidate.surface_support:.2f})")
```

## Execution Layer Status

After U₅ implementation:

```
U₀ Unicode ✅
U₁ Grapheme ✅
U₂p PhoneticProjection ✅
U₂s ArabicSyllable ✅
U₃ BoundaryAndAttachment ✅
U₄ TrueSingularLafẓ ✅
U₅ FunctionalRole ✅ COMPLETE
U₆ MabniClosedClass ⏸ (next)
```

## Testing

See `tests/dal_core/test_u5_functional_role_carrier.py` for:

1. **Prohibition tests** (6 tests)
   - No root field
   - No weight field
   - No meaning field
   - No hukm field
   - Candidates not certificates
   - CPB₅ completeness

2. **Role candidate tests** (4 tests)
   - Verb candidates from U₄ potentials
   - Noun candidates from U₄ potentials
   - Closed-class candidates
   - Pronoun candidates

3. **Golden cases** (3 tests)
   - كَتَبَ (past verb)
   - بِكِتَابٍ (preposition + noun)
   - وَبِكِتَابِهِمْ (complex composition)

4. **Trace and evidence tests** (2 tests)
   - Trace preservation to U₄
   - Evidence referencing U₄

5. **Execution tests** (2 tests)
   - Runs without errors
   - Handles edge cases

## Summary

**U₅ Achievement**:

```
✅ Reads U₄ surface potentials
✅ Opens functional role paths
✅ Assigns candidates (NOT certificates)
✅ Preserves trace/residuals/rank
✅ No forbidden fields (root, weight, meaning, hukm)
✅ Ready for U₆ MabniClosedClass
```

**Constitutional Compliance**:

```
U₅ لا يستخرج الجذر.
U₅ لا يحدد الوزن.
U₅ لا يعيّن المعنى.
U₅ لا يحكم بإعراب ولا بناء.
U₅ يفتح مسارات وظيفية محتملة فقط.
```
