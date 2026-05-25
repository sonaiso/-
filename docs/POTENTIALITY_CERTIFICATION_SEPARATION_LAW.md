# Potentiality-Certification Separation Law (قانون فصل الإمكان والشهادة)

## Constitutional Status

This is a **FOUNDATIONAL LAW** applying to ALL carrier layers from U₀ onward.

**NOT** a late weight-only concept.
**NOT** an optional enhancement.
**IS** the constitutional principle governing carrier-to-certificate transitions.

## Core Principle (المبدأ الأساسي)

### Arabic Formulation

```
الحامل لا يشهد
الحامل يفتح إمكانًا
الإمكان لا يصير شهادة إلا ببوابة
```

### English Formulation

```
Carrier does NOT certify
Carrier only opens possibility
Possibility becomes certificate only through gate
```

### Formal Statement

```
Carrierᵢ(x) ⊬ Certificateᵢ₊₁(x)
Carrierᵢ(x) ⊢ PotentialPathᵢ₊₁(x)

PotentialPathᵢ₊₁(x) + Gateᵢ₊₁ + Evidence + Rank + Residuals + Trace
⇒ Certificateᵢ₊₁(x)
```

## Why This Law Is Foundational

### Problem Without This Law

**Direct Certification** (forbidden):
```python
UnicodeCarrier(ك) → GraphemeCertificate  # ❌ NO GATE
```

This allows carriers to **usurp epistemic authority** without evidence, gates, or validation.

**Example Violations**:
- Unicode → Grapheme (skips grapheme cluster validation)
- Grapheme → Phonetic (skips phonetic projection gates)
- Syllable → Weight (skips 7 intermediate layers!)
- ANY Carrier → Certificate (skips ALL validation)

### Solution With This Law

**Potential Path** (required):
```python
UnicodeCarrier(ك)
→ PotentialArabicBaseLetterPath  # Opens possibility
→ GraphemeBaseGate  # Validates
→ GraphemeCertificate  # Only if gate passes ✅
```

**Example Correct Paths**:
```
U₀ UnicodeCarrier(ك)
→ PotentialArabicBaseLetterPath
→ GraphemeBaseGate
→ U₁ GraphemeCertificate

U₁ GraphemeCarrier(كَ)
→ PotentialCVPhoneticPath
→ PhoneticProjectionGate
→ U₂p PhoneticProjectionCertificate

U₂p PhoneticProjection(C=/k/, V=/a/)
→ PotentialCVSyllablePath
→ SyllableGate(requires_nucleus=True)
→ U₂s SyllableCertificate

U₂s SyllableCarrier([كَ,تَ,بَ])
→ PotentialBoundaryPath
→ BoundaryGate
→ U₃ BoundaryAndAttachmentCertificate

U₈ RootStemCarrier(كتب)
→ PotentialWeightedPath
→ WeightGate
→ U₉ WeightCertificate
```

## Architectural Implications

### Every Layer Must Have

1. **Carrier** - Holds value, does NOT certify
2. **PotentialPath** - Opens possibility, holds requirements
3. **Gate** - Validates requirements
4. **Certificate** - Certified result (only after gate)

### Every Transition Must Follow

```
Carrierᵢ → PotentialPathᵢ₊₁ → Gateᵢ₊₁ → Certificateᵢ₊₁
```

### Forbidden Patterns

```python
# ❌ Direct certification
carrier.certify()  # NO! Carrier cannot certify itself

# ❌ Automatic certification
potential_path.status = CERTIFICATE  # NO! Must go through gate

# ❌ Skipping gate
carrier → certificate  # NO! Must pass through potential path + gate
```

### Required Patterns

```python
# ✅ Create potential path
path = make_potential_path(
    source_carrier_id=carrier.uid,
    source_layer="U0_UNICODE",
    target_layer="U1_GRAPHEME",
    path_name="ArabicBaseLetter",
    path_family="grapheme",
    required_gates=("grapheme_base_gate",),
    evidence=("unicode_category=Lo",),
    rank=Rank.CANDIDATE,
    trace=(carrier.uid,)
)

# ✅ Pass through gate
gate_result = grapheme_base_gate.validate(path)

# ✅ Certify only if gate passes
if gate_result.passed:
    certified_path = certify_potential_path(
        path=path,
        passed_gates=("grapheme_base_gate",),
        evidence=gate_result.evidence,
        residuals=gate_result.residuals,
        rank=Rank.CERTIFICATE
    )
```

## Critical Laws

### Law 1: No Direct Certification

```
Carrierᵢ ⊬ Certificateᵢ₊₁
```

**Meaning**: Carrier NEVER directly produces certificate for next layer.

**Enforcement**: `validate_no_direct_certificate()` function raises `DirectCertificationError`.

**Example**:
```python
# ❌ FORBIDDEN
unicode_carrier.produce_grapheme_certificate()

# ✅ REQUIRED
unicode_carrier.produce_potential_grapheme_paths()
```

### Law 2: Potential Opens, Does Not Certify

```
Carrierᵢ ⊢ PotentialPathᵢ₊₁
PotentialPath ≠ Certificate
```

**Meaning**: Carrier produces PotentialPath, which is NOT yet certified.

**Enforcement**: `PotentialPathStatus.CANDIDATE` is initial state, NOT `CERTIFICATE`.

**Example**:
```python
# ✅ Carrier produces CANDIDATE
path = PotentialPath(
    status=PotentialPathStatus.CANDIDATE,  # Not CERTIFICATE!
    ...
)
```

### Law 3: Certification Requires Gate Passage

```
PotentialPath + Gate + Evidence → Certificate
```

**Meaning**: Only gates can certify paths, and only with evidence.

**Enforcement**: `certify_potential_path()` validates all requirements.

**Requirements**:
- All `required_gates` must be in `passed_gates`
- No `failed_gates`
- No blocking `residuals`
- Has `evidence`
- `rank` = CERTIFICATE

**Example**:
```python
# ❌ Cannot certify without gate passage
path.status = PotentialPathStatus.CERTIFICATE  # Validation error!

# ✅ Must certify through function with validation
certified = certify_potential_path(
    path=path,
    passed_gates=all_required_gates,  # All must pass
    evidence=gate_evidence,  # Must have evidence
    residuals=no_blockers,  # No blockers
    rank=Rank.CERTIFICATE
)
```

### Law 4: Blocking Terminates Path

```
failed_gate ∨ blocking_residual → status=BLOCKED
```

**Meaning**: Gate failure or blocking residuals terminate path.

**Enforcement**: `block_potential_path()` sets status to BLOCKED.

**Example**:
```python
# Unattached mark fails gate
path = PotentialPath(...)  # َكتب (mark before letter)
gate_result = attachment_gate.validate(path)
if gate_result.failed:
    blocked = block_potential_path(
        path=path,
        failed_gates=("attachment_gate",),
        residuals=gate_result.residuals,
        reason="Unattached mark"
    )
```

## Application to All Layers

### U₀ → U₁ (Unicode → Grapheme)

```python
UnicodeCarrier(ك)
→ PotentialArabicBaseLetterPath
→ GraphemeBaseGate(validates: unicode_category, script, composition)
→ GraphemeCertificate

UnicodeCarrier(َ)
→ PotentialAttachedMarkPath
→ AttachmentGate(requires: base_letter)
→ BLOCKED if unattached
```

### U₁ → U₂p (Grapheme → PhoneticProjection)

```python
GraphemeCluster(كَ)
→ PotentialCVPhoneticPath(C=/k/, V=/a/)
→ PhoneticProjectionGate(validates: phoneme_mapping)
→ PhoneticProjectionCertificate

GraphemeCluster(و)
→ PotentialConsonantPath(/w/)
→ PotentialLongVowelCarrierPath(/ū/)
→ ContextGate(decides based on context)
→ Certificate for one path, BLOCKED for others
```

### U₂p → U₂s (PhoneticProjection → Syllable)

```python
PhoneticProjection(C=/k/, V=/a/)
→ PotentialCVSyllablePath
→ SyllableGate(requires_nucleus=True)
→ SyllableCertificate

PhoneticProjection(C=/b/, SUKUN)
→ PotentialCodaPath
→ SyllableGate(requires_nucleus=True)
→ BLOCKED (no nucleus)
```

### U₂s → U₃ (Syllable → Boundary)

```python
SyllableSequence([وَ, بِ, كِ, تَا, بِ, هِمْ])
→ PotentialBoundaryPaths:
   - [وَ] [بِكِتَابِهِمْ]
   - [وَ] [بِـ] [كِتَابِـهِمْ]
   - [وَ] [بِـ] [كِتَاب] [ـهِمْ]
→ BoundaryGate(validates: morphology, lexicon)
→ BoundaryAndAttachmentCertificate
```

### U₈ → U₉ (RootStem → Weight)

```python
RootStemCarrier(كتب)
→ PotentialVerbWeightedPath(فعل pattern)
→ PotentialNounWeightedPath(فعال pattern)
→ PotentialCurvedWeightedPath(قال → فعل with curvature)
→ WeightGate(validates: pattern_fit, phonetic_curvature)
→ WeightCertificate
```

**Note**: Weight is NOT special! It's just U₉ application of the same foundational law.

## Violations and Enforcement

### Violation Type 1: Direct Certification

```python
# ❌ VIOLATION
class UnicodeCarrier:
    def to_grapheme(self) -> GraphemeCertificate:
        return GraphemeCertificate(...)  # Direct jump!

# ✅ CORRECT
class UnicodeCarrier:
    def to_potential_grapheme_paths(self) -> List[PotentialPath]:
        return [PotentialPath(...)]  # Opens possibilities
```

**Enforcement**: Code review + `validate_no_direct_certificate()` in tests.

### Violation Type 2: Auto-Certification

```python
# ❌ VIOLATION
path = PotentialPath(
    status=PotentialPathStatus.CERTIFICATE,  # Immediate certification!
    passed_gates=(),  # No gates passed!
    evidence=(),  # No evidence!
    ...
)

# ✅ CORRECT
path = make_potential_path(...)  # Starts as CANDIDATE
# ... gate validation ...
certified = certify_potential_path(
    path=path,
    passed_gates=all_gates,
    evidence=evidence
)
```

**Enforcement**: `PotentialPath.__post_init__()` validation.

### Violation Type 3: Gate Bypass

```python
# ❌ VIOLATION
carrier → certificate  # Skips PotentialPath + Gate

# ✅ CORRECT
carrier → potential_path → gate → certificate
```

**Enforcement**: Architecture tests + integration tests.

## Implementation Checklist

### Foundation (Complete)

- [x] `PotentialPath` dataclass
- [x] `PotentialPathStatus` enum
- [x] `certify_path()` validator
- [x] `validate_no_direct_certificate()` guard
- [x] Factory functions (`make_potential_path`, `certify_potential_path`, `block_potential_path`)
- [x] `__post_init__()` validation

### Integration (To Do)

- [ ] U₀ Unicode → PotentialGraphemePath adapter
- [ ] U₁ Grapheme → PotentialPhoneticPath adapter
- [ ] U₂p PhoneticProjection → PotentialSyllablePath adapter
- [ ] U₂s Syllable → PotentialBoundaryPath adapter
- [ ] U₃+ Higher layers → PotentialPath adapters

### Tests (To Do)

- [ ] Test: Unicode cannot directly certify Grapheme
- [ ] Test: Grapheme cannot directly certify PhoneticProjection
- [ ] Test: PhoneticProjection cannot directly certify Syllable
- [ ] Test: Syllable cannot directly certify Boundary
- [ ] Test: PotentialPath requires gate passage for certification
- [ ] Test: PotentialPath blocks on gate failure
- [ ] Test: PotentialWeightedCarrier is same law as all others

## Summary

**THIS IS NOT A WEIGHT-ONLY CONCEPT.**

**THIS IS A FOUNDATIONAL CONSTITUTIONAL LAW.**

Every carrier at every layer must follow:

```
Carrier → PotentialPath → Gate → Certificate
```

The weight layer is just one late instance of this universal principle that begins at Unicode.

**الإمكان ليس شهادة** - Possibility is not certification.

**PR**: FOUNDATION-POTENTIALITY-LAW
**Created**: 2026-05-25
**Status**: Constitutional Law (applies to all layers)
