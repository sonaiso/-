# DAL_CORE MufradProof Documentation

**برهان المفرد - Composition-Ready Signifier Proof**

## Overview

`MufradProof` is the composition-ready closed signifier structure that extends basic `DClosed` with complete morphological and surface phonological analysis. It is the **mandatory input** for all syntax composition operations.

## Core Principle

```
D_mufrad هو أساس أرقام التركيب
(D_mufrad is the foundation of composition ranks)
```

Before moving to تركيب (syntax/composition), the Arabic singular signifier must be closed as a **جامع مانع مفردي proof object** (comprehensive and exclusive singular proof).

### Why MufradProof is Required

The syntax layer must NOT work on:
- Raw tokens
- Raw strings
- `Carrier`
- `ArabicAtom`
- `DForm`
- `DType`
- `DClosed` (basic, without morph proof)

The syntax layer must ONLY work on:
- `MufradProof` (composition-ready singular word proof)

## Architecture

```
Unicode → Carrier → ArabicAtom → OperativeUnit → Syllable
  → DForm → DLugha → DType → DClosed → MufradProof
                                         ↓
                                  [Syntax Composition]
```

## The 10 Non-Negotiable Theorems

### Theorem 1: No composition before MufradProof

Syntax/composition must not accept raw tokens, raw strings, `Carrier`, `ArabicAtom`, `DForm`, or `DType` as direct nodes.

**Only `MufradProof` may be a syntax node.**

**Enforcement**: `OperatorContract.apply()` rejects any non-MufradProof input with `OPERATOR_ON_TOKEN_FORBIDDEN` residual.

### Theorem 2: SurfaceEffect belongs to MufradProof

`SurfaceEffect` enters the singular word proof.

**Allowed in MufradProof**:
- Final damma/fatha/kasra/sukun
- Tanwin (damm, fath, kasr)
- Final alif/waw/ya
- Nun retained/deleted
- Weak letter deleted/replaced
- Visible vs hidden/estimated marks

**Critical**: SurfaceEffect is not meaning and not syntax role.

### Theorem 3: CaseEffect does not enter MufradProof

`CaseEffect` belongs to later composition/syntax contracts.

**Forbidden in MufradProof**:
- `case_effect`
- `syntax_role`
- `faail`, `mafool`, `mubtada`, `khabar`
- `majroor_by`, `mansub_by`, `marfoo_by`
- `governed_by_operator`

**Allowed in MufradProof**:
- `surface_effects` (what is visible)
- `case_potential` (capacity to receive case)
- `inflection_potential` (capacity to inflect)

### Theorem 4: MorphFeatures belong to MufradProof as candidates

Morphological features enter `MufradProof` as governed candidates, not as semantic meaning.

**Allowed**:
- `segmentation` (stem + clitics)
- `stem`
- `clitics`
- `root_candidates`
- `wazn_candidates`
- `derivation_status`
- `jamid_mushtaq_status`
- `mabni_murab_status`
- `definiteness_status`
- `gender_status`
- `number_status`
- `verb_features` (if FIIL)
- `noun_inflection_class` (if ISM)
- `particle_operator_potential` (if HARF)
- `surface_effects`
- `composition_readiness`

Every feature must have:
- `evidence`
- `rank`
- `residuals`
- `trace`
- `competitors` (if applicable)

### Theorem 5: SyntaxRole does not enter MufradProof

Syntax roles are composition outputs only.

**Forbidden**:
- `subject`, `object`, `agent`, `patient`
- `faail`, `naib_faail`, `mafool`
- `mubtada`, `khabar`
- `hal`, `tamyiz`, `badal`, `naat`, `mudaf_ilayh`

These emerge ONLY from composition, never from MufradProof.

### Theorem 6: Operators do not work on tokens

An `OperatorContract` must consume `MufradProof`, not raw tokens.

**Forbidden**:
```python
operator.apply(token)
operator.apply(raw_string)
operator.apply(DForm)
operator.apply(Carrier)
```

**Allowed**:
```python
operator.apply(mufrad_proof)
operator.apply(mufrad_proof_a, mufrad_proof_b, context)
```

### Theorem 7: Composition never raises MufradProof rank

If later composition exists, its rank must be bounded by the weakest participating `MufradProof`.

```
composition_rank <= min(mufrad_proof.rank, operator.rank, relation.rank)
```

**Enforcement**: `MufradProof.get_weakest_rank()` calculates minimum across all components.

### Theorem 8: Composition inherits MufradProof residuals

Any later composition candidate must preserve all residuals from its input `MufradProof` nodes.

**No residual erasure.**

**Enforcement**: `MufradProof.collect_all_residuals()` gathers all residuals from all components.

### Theorem 9: No certificate with incomplete MufradProof

If a `MufradProof` has blockers, unresolved required features, or unresolved competitors, then:

```
composition_readiness != READY_FOR_CERTIFICATE_COMPOSITION
```

and later composition cannot issue certificate from it.

### Theorem 10: No certificate with unresolved competitors

If multiple `MufradProof` candidates remain and none is resolved by a governed comparison, then final output is `HYPOTHESIS`, not `CERTIFICATE`.

**Check**: `mufrad_proof.has_unresolved_competitors()`

## MufradProof Structure

```python
@dataclass(frozen=True)
class MufradProof:
    # Core dal-mufrad data (required)
    form: FormCandidate
    lugha: LughaAttestation
    type: TypedDal

    # Morphological proof (required for composition)
    segmentation: SegmentationProof
    stem: StemProof
    clitics: tuple[CliticProof, ...]

    # Root and pattern candidates (may have competition)
    root_candidates: tuple[RootCandidate, ...]
    wazn_candidates: tuple[WaznCandidate, ...]

    # Morphological feature status
    derivation_status: CandidateStatus
    jamid_mushtaq_status: CandidateStatus
    mabni_murab_status: CandidateStatus
    definiteness_status: CandidateStatus
    gender_status: CandidateStatus
    number_status: CandidateStatus

    # Type-specific features
    verb_features: Optional[VerbFeatureProof] = None
    noun_inflection_class: Optional[NounInflectionClass] = None
    particle_operator_potential: Optional[ParticleOperatorPotential] = None

    # Surface effects (ALLOWED)
    surface_effects: tuple[SurfaceEffect, ...] = ()

    # Composition readiness
    composition_readiness: CompositionReadiness = NOT_READY

    # Proof metadata
    rank: LughaRank = ZERO
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}

    # Competing analyses
    competitors: tuple[MufradProof, ...] = ()
```

## Supporting Types

### SegmentationProof

Proves word segmentation into stem + clitics.

```python
@dataclass(frozen=True)
class SegmentationProof:
    segments: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}
```

### StemProof

The core inflectable part after removing clitics.

```python
@dataclass(frozen=True)
class StemProof:
    stem: str
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}
```

### CliticProof

Proof of attached particle (prefix/suffix).

Examples: ال، ب، ك، ل، و، ف، ها، هم، كم

```python
@dataclass(frozen=True)
class CliticProof:
    clitic: str
    position: str  # "prefix" | "suffix"
    clitic_type: str  # "definite_article" | "preposition" | "pronoun" | etc
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}
```

### RootCandidate

Root extraction candidate with evidence.

```python
@dataclass(frozen=True)
class RootCandidate:
    root: tuple[str, ...]  # e.g., ("ك", "ت", "ب")
    root_type: str  # "trilateral" | "quadrilateral" | etc
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    confidence: float
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}
```

### WaznCandidate

Morphological pattern candidate.

Examples: فَعَلَ، فاعِل، مَفعول، فَعّال

```python
@dataclass(frozen=True)
class WaznCandidate:
    wazn: str
    pattern_class: str  # "verb_form_I" | "active_participle" | etc
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    confidence: float
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}
```

### SurfaceEffect

A phonological/orthographic effect visible on word surface.

```python
@dataclass(frozen=True)
class SurfaceEffect:
    effect_type: SurfaceEffectType
    visibility: SurfaceEffectVisibility
    location: str  # "final" | "penultimate" | "position_N"
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = ()
    trace: dict = {}
    alternatives: tuple[SurfaceEffect, ...] = ()
```

**Surface Effect Types**:
- `FINAL_DAMMA`, `FINAL_FATHA`, `FINAL_KASRA`, `FINAL_SUKUN`
- `TANWIN_DAMM`, `TANWIN_FATH`, `TANWIN_KASR`
- `FINAL_ALIF`, `FINAL_WAW`, `FINAL_YA`
- `NUN_RETAINED`, `NUN_DELETED`
- `WEAK_LETTER_DELETED`, `WEAK_LETTER_REPLACED`
- `VISIBLE_FINAL_MARK`, `HIDDEN_FINAL_MARK`, `ESTIMATED_EFFECT_CANDIDATE`

## Composition Readiness

Explicit readiness states:

### NOT_READY

Missing basic requirements:
- Missing form/lugha/type
- Blocker residuals present
- Required feature slots empty

### READY_AS_HYPOTHESIS

Basic proof exists but:
- Some required morphological features unresolved
- Some surface effects untraced
- Rank insufficient for certificate
- Can participate in composition but output will be hypothesis

### READY_FOR_COMPOSITION

Sufficient features for syntax to consume:
- Form/lugha/type present
- No blocker residuals
- Essential morph features resolved
- But some competitors or residuals remain
- Composition output will inherit limitations

### READY_FOR_CERTIFICATE_COMPOSITION

Highest readiness:
- No blockers
- Required morph slots fully resolved
- Surface effects fully traced
- Competitors resolved or ranked
- Rank sufficient (SAMA, AHAD, or TAWATUR)
- Composition can issue certificate (if other constraints met)

## Required Feature Slots

`MufradProof` is not composition-ready unless these slots are present or explicitly unresolved with residuals:

**Always required**:
- `segmentation`
- `stem`
- `clitics`
- `root_candidates`
- `wazn_candidates`
- `derivation_status`
- `jamid_mushtaq_status`
- `mabni_murab_status`
- `definiteness_status`
- `gender_status`
- `number_status`
- `surface_effects`

**If type == FIIL**:
- `verb_features`

**If type == ISM**:
- `noun_inflection_class`

**If type == HARF**:
- `particle_operator_potential`

## Important Distinctions

### SurfaceEffect vs CaseEffect

**SurfaceEffect** (ALLOWED in MufradProof):
- Visible final damma
- Visible final fatha
- Visible final kasra
- Visible final sukun
- Final alif/waw/ya
- Nun retained/deleted
- Estimated effect candidate

**CaseEffect** (FORBIDDEN in MufradProof):
- Operator + relation + governed word + surface effect + residuals
- Requires composition context

### MorphFeatures vs SyntaxRole

**Morph features** (ALLOWED as candidates):
- `mabni_candidate`, `murab_candidate`
- `mufrad_candidate`, `dual_candidate`, `plural_candidate`
- `feminine_candidate`, `masculine_candidate`
- `definite_candidate`, `indefinite_candidate`
- `verb_madi_form`, `verb_mudari_form`, `verb_amr_form`
- `majhul_form`, `malum_form`

**Syntax roles** (FORBIDDEN):
- `faail`, `mafool`, `mubtada`, `khabar`
- `mudaf_ilayh`, `jar_majroor_role`

## Residuals

New MufradProof-specific residuals:

- `MUFRAD_MORPH_PROOF_MISSING`
- `MUFRAD_SURFACE_PROOF_MISSING`
- `MUFRAD_SEGMENTATION_UNRESOLVED`
- `MUFRAD_STEM_UNRESOLVED`
- `MUFRAD_CLITICS_UNRESOLVED`
- `MUFRAD_ROOT_COMPETITION_UNRESOLVED`
- `MUFRAD_WAZN_COMPETITION_UNRESOLVED`
- `MUFRAD_DERIVATION_UNRESOLVED`
- `MUFRAD_JAMID_MUSHTAQ_UNRESOLVED`
- `MUFRAD_MABNI_MURAB_UNRESOLVED`
- `MUFRAD_DEFINITENESS_UNRESOLVED`
- `MUFRAD_GENDER_UNRESOLVED`
- `MUFRAD_NUMBER_UNRESOLVED`
- `MUFRAD_VERB_FEATURES_REQUIRED`
- `MUFRAD_NOUN_INFLECTION_REQUIRED`
- `MUFRAD_PARTICLE_OPERATOR_POTENTIAL_REQUIRED`
- `MUFRAD_COMPETITORS_UNRESOLVED`
- `MUFRAD_NOT_READY_FOR_COMPOSITION`
- `CASE_EFFECT_LEAK_IN_MUFRAD`
- `SYNTAX_ROLE_LEAK_IN_MUFRAD`
- `OPERATOR_ON_TOKEN_FORBIDDEN`
- `COMPOSITION_RANK_OVER_MUFRAD`
- `COMPOSITION_ERASED_MUFRAD_RESIDUAL`

## No Semantic Leak

The following fields are **forbidden** anywhere in `MufradProof`:

- `meaning`, `semantic`, `madlul`, `murad`
- `haqiqa`, `majaz`, `reality_ref`, `grounding`
- `intended_meaning`, `referent`, `denotation`
- `subject`, `object`, `agent`, `patient`
- `faail`, `mafool`, `mubtada`, `khabar`

**Enforcement**:
- `MufradProof.__post_init__()` validates field absence
- `verify_no_semantic_leak()` checks proof
- `verify_no_syntax_role_leak()` checks proof
- `verify_no_case_effect_leak()` checks proof

## Tests

All 15 theorem tests passing:

- `test_mufrad_proof_has_required_fields`
- `test_mufrad_proof_requires_form_lugha_type`
- `test_mufrad_proof_requires_morph_proof_for_composition`
- `test_surface_effect_allowed_in_mufrad`
- `test_case_effect_forbidden_in_mufrad`
- `test_morph_features_allowed_as_candidates`
- `test_syntax_role_forbidden_in_mufrad`
- `test_operator_contract_rejects_raw_token`
- `test_operator_contract_accepts_mufrad_proof`
- `test_composition_rank_cannot_exceed_mufrad_rank`
- `test_composition_inherits_mufrad_residuals`
- `test_unresolved_mufrad_competitor_blocks_certificate`
- `test_no_semantic_leak_in_mufrad_proof`
- `test_composition_readiness_levels`
- `test_weakest_link_rank`

## Allowed Scientific Claim

After this phase, the allowed claim is:

> `dal_core` now produces a governed composition-ready MufradProof for supported vocalized word forms, preserving morph/surface candidates, rank, residuals, trace, and competitors.

**Forbidden claim**:

> ~~`dal_core` now performs full syntax composition.~~

**Forbidden claim**:

> ~~`dal_core` now understands meaning or murad.~~

---

**Version**: 1.0.0
**Date**: 2026-05-19
**Status**: Implemented and Tested
