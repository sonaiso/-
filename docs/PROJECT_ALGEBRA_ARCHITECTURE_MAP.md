# Project Algebra Architecture Map

**PR #22**: Complete algebraic hierarchy from reality to judgment
**Status**: Governance documentation (no implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document presents the **complete algebraic architecture** of the project, showing how Dal Algebra fits within a broader General Algebra framework.

**Core correction**:
> **Dal Algebra is not the first algebra.**
> **Wadhʿ is not the first contract.**
> **Madlul is not a given primitive.**

The architecture spans **13 algebraic layers** (A0-A13), from Source-of-Effect through Hukm/Inference.

---

## The Complete Hierarchy

```text
A0: General Algebra
    ├─ A1: Source-of-Effect Algebra
    ├─ A2: Effect Reception Algebra
    ├─ A3: Prior-Information Algebra
    ├─ A4: Effect-Prior Binding Algebra
    ├─ A5: Tasawwur / Candidate-Madlul Algebra
    ├─ A6: Ordered Dal Form Algebra
    ├─ A7: Dal-Mufrad Algebra
    ├─ A8: Dal-Murakkab Algebra
    ├─ A9: Wadhʿ Contract Algebra
    ├─ A10: Dalalah Algebra
    ├─ A11: Istiʿmal Algebra
    ├─ A12: Murad Understanding Algebra
    └─ A13: Hukm / Inference / Tanzil Algebra
```

---

## Layer Definitions

### A0: General Algebra

**Definition**: The abstract algebraic framework providing foundational structures for all specialized algebras.

**Scope**:
- Abstract types and contracts
- Candidate generation patterns
- Evidence structures
- Rank/Residual patterns
- Trace preservation principles
- Bounded/unbounded domain theory

**Key principle**:
> General Algebra does NOT start with Dal, Madlul, or Wadhʿ.
> It starts with Source → Effect → Prior → Binding.

**Status**: Architectural abstraction (not implemented as runtime algebra)

**Related**: This layer provides the meta-framework for all other algebras

---

### A1: Source-of-Effect Algebra

**Definition**: Algebra governing the identification and classification of reality sources producing effects.

**Domain**: 10 source types
1. Sensory Reality (physical signals)
2. Mental Reality (cognitive states)
3. Linguistic Reality (language as system)
4. Social Reality (institutions, conventions)
5. Technical Reality (domain systems)
6. Legal Reality / Shar'i Reality (legal/religious systems)
7. Mathematical Reality (formal structures)
8. Programmatic Reality (computational execution)
9. Textual Source (pre-existing texts)
10. Reported Source (transmitted information)

**Key principle**:
> Reality is not limited to sensory reality.

**Operations**:
- Source identification
- Source classification
- Multi-source composition
- Source uncertainty modeling

**Contracts**:
```text
IdentifySource: RawInput → SourceCandidate
ClassifySource: SourceCandidate → SourceType
ComposeSource: [Source] → CompositeSource
```

**Status**: Documented (A1 runtime implementation is out of scope for PR #22)

**Related**: See `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §1

---

### A2: Effect Reception Algebra

**Definition**: Algebra governing what reaches the system boundary.

**Domain**: 10 effect types
1. Sound (acoustic signals)
2. Script (visual written patterns)
3. Image (visual representations)
4. Gesture (embodied communication)
5. Report (transmitted accounts)
6. Context (situational information)
7. Text (structured linguistic input)
8. Definition (explicit specifications)
9. Event (observed occurrences)
10. Signal (abstract information carriers)

**Key principle**:
> Effect is not Madlul.
> Effect is the raw signal before interpretation.

**Operations**:
- Effect capture
- Effect normalization
- Multi-modal effect composition
- Effect-source linking

**Contracts**:
```text
CaptureEffect: Source → EffectCandidate
NormalizeEffect: RawEffect → NormalizedEffect
LinkEffectToSource: Effect → (Effect, Source)
```

**Status**: Documented (A2 runtime implementation is out of scope for PR #22)

**Related**: See `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §2

---

### A3: Prior-Information Algebra

**Definition**: Algebra governing the "non-absolute zero" knowledge layer.

**Domain**: 10 prior information components
1. Lexicon (stored word forms)
2. Attestation (recorded usage)
3. Classification (category systems)
4. Examples (paradigmatic instances)
5. Rules (explicit constraints)
6. Domain Constraints (field-specific knowledge)
7. Previous Experience (accumulated exposure)
8. Axioms (foundational principles)
9. Initial Facts (starting assumptions)
10. Usage Conventions (pragmatic norms)

**Key principle**:
> No Tasawwur (conceptualization) without Prior Information.

**Operations**:
- Prior retrieval
- Prior update
- Prior composition
- Prior consistency checking

**Contracts**:
```text
RetrievePrior: Query → PriorCandidateSet
UpdatePrior: NewEvidence × Prior → UpdatedPrior
CheckConsistency: [Prior] → ConsistencyReport
```

**Status**: Documented (A3 runtime implementation is out of scope for PR #22)

**Related**: See `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §3

---

### A4: Effect-Prior Binding Algebra

**Definition**: The **first cognitive contract** algebra, binding effects to prior information.

**Formula**:
```text
Effect × PriorInformation → BindingCandidate
```

**Key principle**:
> This is the first contract.
> Wadhʿ comes later (A9).

**Operations**:
- Pattern matching (Effect ↔ Prior exemplars)
- Rule application (Effect validates against Prior rules)
- Frequency weighting (Effect likelihood from Prior experience)
- Context integration (Effect interpretation via Prior context)

**Contracts**:
```text
BindEffectToPrior: (Effect, Prior) → BindingCandidateSet
RankBindings: BindingCandidateSet → RankedBindings
DetectConflicts: BindingCandidateSet → ConflictReport
```

**Output**: `BindingCandidate` carrying:
- `effect_source`: which effect pattern
- `prior_source`: which prior information
- `binding_strength`: confidence/rank
- `residuals`: unexplained aspects
- `counter_evidence`: competing interpretations

**Status**: Documented (A4 runtime implementation is out of scope for PR #22)

**Related**: See `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §4

---

### A5: Tasawwur / Candidate-Madlul Algebra

**Definition**: Algebra governing the formation of meaning candidates from effect-prior bindings.

**Formula**:
```text
CandidateMadlul = Bound(Effect, PriorInformation)
```

**Key principle**:
> Madlul is not a primitive.
> It is a licensed candidate requiring evidence.

**Operations**:
- Candidate generation from bindings
- Candidate ranking
- Counter-evidence detection
- Residual analysis
- Trace preservation

**Contracts**:
```text
GenerateMadlulCandidates: BindingCandidateSet → MadlulCandidateSet
RankMadlul: MadlulCandidateSet → RankedMadlul
ValidateEvidence: MadlulCandidate → EvidenceReport
```

**Required fields** in `CandidateMadlul`:
- `evidence`: effect pattern + prior match + binding operation
- `counter_evidence`: competing candidates + conflicts
- `rank`: confidence + ranking basis
- `residuals`: unexplained aspects + gaps
- `trace`: derivation path + source effect + source prior
- `missing_required_inputs`: required context/qarina/licensing

**Status**: Documented (A5 runtime implementation is out of scope for PR #22)

**Related**: See `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §5

---

### A6: Ordered Dal Form Algebra

**Definition**: Algebra governing the construction of ordered, bounded, internally composed signifier forms.

**Formula**:
```text
RawDalEffect → OrderedBoundedDalCandidate
```

**Key principle**:
> Dal is not raw sound or raw letters.
> Dal is an ordered, bounded, structured form.

**Operations**:
- Ordering (sequence construction)
- Boundary placement
- Unit composition (fold/split)
- Direction analysis (forward/backward scan)
- Trace preservation

**Contracts**:
```text
OrderDal: RawDalEffect → OrderedDal
SetBoundaries: OrderedDal → BoundedDal
FoldUnits: [Unit] → ComposedUnit (with reverse trace)
ScanDirection: OrderedDal → DirectionalEvidence
```

**Required properties** in `OrderedDal`:
- `order`: sequence + indices + direction
- `boundaries`: left_boundary + right_boundary + internal_boundaries
- `units`: atomic_units + composed_units + unit_relations
- `direction`: scan_direction + prev/next links
- `fold_trace`: source_atoms + operations + reverse_trace
- `residuals`: ambiguous_boundaries + competing_orders
- `rank`: order_confidence + boundary_confidence

**Status**: Governed by `docs/ORDERED_DAL_FORM_GOVERNANCE.md` (PR #21)

**Related**:
- Full specification: `docs/ORDERED_DAL_FORM_GOVERNANCE.md`
- Boundary details: `docs/INTERNAL_COMPOSITION_BOUNDARIES.md`
- Direction details: `docs/BIDIRECTIONAL_ANALYSIS_CHARTER.md`
- Reality-Effect-Prior link: `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §6

---

### A7: Dal-Mufrad Algebra (Individual Signifier Algebra)

**Definition**: Algebra governing individual closed signifier units (words).

**Scope**: Single lexical items with internal morphological structure

**Domain layers** (from `dal_core`):
- D0: Graphophonemic (letters + diacritics)
- D1: Syllabic (CV patterns)
- D2: Pre-Morph (syllable aggregates)
- D3: Origin (root/particle/frozen classification)
- D4: Template (morphological patterns)
- D5: Identity Axis (lexical identity)
- D6: Directional Analysis (forward/backward evidence)
- D7: Judgment (ranked candidates)

**Key principle**:
> Dal-Mufrad closes the individual signifier.
> It does NOT create CandidateMadlul.
> It does NOT create Wadhʿ.
> It does NOT create Dalalah.

**Operations**:
- Phonological analysis (C1 → C2a)
- Morphological analysis (C2b)
- Root extraction
- Pattern matching
- Morphological segmentation
- Lexical sign closure

**Contracts**: (from `dal_core`)
- `Contract 1`: Carrier (Unicode/UTF-8 representation)
- `Contract 2`: Atom (letters + diacritics)
- `Contract 3`: Unit (syllables)
- `Contract 4`: MorphProof (morphological evidence)
- `Contract 5`: MufradProof (lexical closure)
- `Contract 6`: PreSyntaxVector (syntax-ready interface)
- `Contract 7`: OperatorTrigger (operator candidacy)
- `Contract 8`: OperatorRegistry (operator inventory)
- `Contract 9`: SentenceFrame (composition container)

**Status**: ✅ **Implemented** in `src/dal_core/` (Contracts 1-9)

**Forbidden**:
- ❌ Meaning fields in MufradProof
- ❌ Direct semantic interpretation
- ❌ Wadhʿ claims
- ❌ Pragmatic murad inference

**Related**:
- Implementation: `src/dal_core/d_mufrad.py`
- Governance: `docs/SPEC_DAL_CORE.md`
- Compliance: `docs/DAL_CORE_COMPLIANCE.md`

---

### A8: Dal-Murakkab Algebra (Composed Signifier Algebra)

**Definition**: Algebra governing composition of already-closed individual signifiers.

**Scope**: Phrases, clauses, sentences built from individual Dal-Mufrad units

**Key principle**:
> Dal-Murakkab composes already-closed signifiers.
> It does NOT create CandidateMadlul.
> It does NOT create Wadhʿ.
> It does NOT create Dalalah.
> It does NOT infer Murad.

**Operations**:
- Composition (fold multiple mufrad units)
- Boundary preservation (track mufrad boundaries in murakkab)
- Order preservation (maintain sequence)
- Trace preservation (reverse to mufrad components)
- Syntactic candidacy (not syntax application)

**Contracts**:
```text
ComposeMufrad: [MufradProof] → MurakkabCandidate
PreserveBoundaries: MurakkabCandidate → BoundaryTrace
GenerateSyntaxCandidates: MurakkabCandidate → SyntaxCandidateSet
```

**Status**: ✅ **Partially implemented** in `dal_core` (SentenceFrame as container)

**Forbidden**:
- ❌ Meaning composition (semantics)
- ❌ Pragmatic inference
- ❌ Context-based disambiguation
- ❌ Operator application (that's syntax, not dal)

**Note**: Syntactic **candidates** (OperatorTrigger) are allowed; syntactic **application** (CaseEffect) is forbidden.

**Related**:
- Container: `src/dal_core/sentence_frame.py`
- Trigger: `src/dal_core/operator_trigger.py`
- Governance: `docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md` (this PR)

---

### A9: Wadhʿ Contract Algebra

**Definition**: Algebra governing the linking of OrderedDal to CandidateMadlul with evidence.

**Formula**:
```text
WadhʿContractCandidate = OrderedDal × CandidateMadlul × WadhʿEvidence
```

**Key principle**:
> Wadhʿ is not merely Dal ↔ Madlul.
> Wadhʿ is a three-way contract: Dal × Madlul × Evidence.
> Wadhʿ is NOT the first contract (A4 Effect-Prior Binding comes first).

**Wadhʿ types**:
1. **Lexical Wadhʿ** (وضع لغوي): Conventional linguistic assignment
2. **Technical Wadhʿ** (وضع اصطلاحي): Domain-specific assignment
3. **Shar'i Wadhʿ** (وضع شرعي): Religious-legal assignment
4. **Stipulative Wadhʿ** (وضع تعييني): Explicit definitional assignment

**Evidence types**:
- Lexicon attestation
- Corpus frequency
- Morphological derivation
- Contextual clue
- Explicit definition
- Transmitted authority

**Contracts**:
```text
EstablishWadh: (OrderedDal, CandidateMadlul, Evidence) → WadhʿCandidate
RankWadh: WadhʿCandidateSet → RankedWadh
ValidateWadhEvidence: WadhʿCandidate → EvidenceReport
```

**Status**: Documented (A9 runtime implementation is out of scope for PR #22)

**Forbidden**:
- ❌ Wadhʿ without OrderedDal (no raw strings)
- ❌ Wadhʿ without CandidateMadlul (no raw meanings)
- ❌ Wadhʿ without Evidence (no unjustified linking)

**Related**: See `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` §7

---

### A10: Dalalah Algebra

**Definition**: Algebra governing the **direction of signification** from Dal to Madlul.

**Three dalalah types** (classical ُأصول الفقه):

#### 10.1 المطابقة (Conformity)
```text
Dal signifies the ENTIRE Madlul
Example: لفظ "إنسان" على الحيوان الناطق
("human" signifies the entire concept of rational animal)
```

#### 10.2 التضمن (Inclusion)
```text
Dal signifies PART of the Madlul
Example: لفظ "بيت" على الجدار
("house" signifies wall as part of house concept)
```

#### 10.3 الالتزام (Entailment)
```text
Dal signifies what is ENTAILED by the Madlul
Example: لفظ "سقف" على الجدار
("ceiling" signifies wall because ceiling entails walls)
```

**Key principle**:
> Dalalah requires established Wadhʿ.
> No Dalalah without Wadhʿ contract.

**Contracts**:
```text
DetermineDalalahDirection: WadhʿContract → DalalahType
ValidateDalalah: (Dal, Madlul, DalalahType) → DalalahJudgment
```

**Status**: Documented (A10 runtime implementation is out of scope for PR #22)

**Forbidden**:
- ❌ Dalalah without prior Wadhʿ
- ❌ Direction-free signification
- ❌ Assuming مطابقة without evidence

---

### A11: Istiʿmal Algebra (Usage Algebra)

**Definition**: Algebra governing **actual usage** contexts and deviations from base Wadhʿ.

**Five usage types**:

#### 11.1 حقيقة (Literal Usage)
```text
Usage according to original Wadhʿ
Example: أسد for actual lion
```

#### 11.2 مجاز (Figurative Usage)
```text
Usage departing from original Wadhʿ with قرينة (indicator)
Example: أسد for brave man (with bravery قرينة)
```

#### 11.3 نقل (Transferred Usage)
```text
Complete transfer to new Wadhʿ
Example: دابة transferred from "walking creature" to "specific animals"
```

#### 11.4 عرف (Conventional Usage)
```text
Usage established by social convention
Example: walad (originally "offspring") → "son" in عرف
```

#### 11.5 شرع (Religious-Legal Usage)
```text
Usage established by religious law
Example: صلاة in شرع = ritual prayer (not generic supplication)
```

**Key principle**:
> No Istiʿmal without قرينة (contextual indicator).
> قرينة distinguishes حقيقة from مجاز.

**Contracts**:
```text
DetectQarina: Context → QarinaSet
ClassifyUsage: (WadhContract, Qarina) → UsageType
ValidateMajaz: MajazCandidate → MajazJudgment
```

**Status**: Documented (A11 runtime implementation is out of scope for PR #22)

**Forbidden**:
- ❌ Istiʿmal without Qarina
- ❌ Majaz without قرينة مانعة من إرادة المعنى الحقيقي
- ❌ Context-free usage classification

---

### A12: Murad Understanding Algebra

**Definition**: Algebra governing **intended meaning** inference from usage + context + licensing.

**Key principle**:
> Murad is not given.
> Murad is inferred from: Istiʿmal + Context + Licensing conditions.

**Inputs**:
- Istiʿmal classification (حقيقة/مجاز/نقل/عرف/شرع)
- Qarina set (contextual indicators)
- Speaker intent signals
- Hearer assumptions
- Discourse context
- Licensing conditions

**Contracts**:
```text
InferMurad: (Istiʿmal, Context, License) → MuradCandidate
RankMurad: MuradCandidateSet → RankedMurad
ValidateLicense: MuradCandidate → LicenseReport
```

**Status**: Documented (A12 runtime implementation is out of scope for PR #22)

**Forbidden**:
- ❌ Murad without context
- ❌ Murad without licensing
- ❌ Assuming unique intended meaning
- ❌ Direct Dal → Murad jump (skipping Wadhʿ, Dalalah, Istiʿmal)

---

### A13: Hukm / Inference / Tanzil Algebra

**Definition**: Algebra governing **judgment, inference, and application** to specific cases.

**Scope**:
- Logical inference (استنباط)
- Legal ruling (حكم شرعي)
- Application to reality (تنزيل على الواقع)
- Case classification (تكييف)

**Key principle**:
> No Hukm without:
> 1. Inference license (استدلال)
> 2. Tanzil conditions (تنزيل على الواقع)
> 3. Prior layer completion (Murad understood)

**Contracts**:
```text
InferHukm: (Murad, InferenceLicense, TanzilConditions) → HukmCandidate
ValidateInference: HukmCandidate → InferenceReport
ApplyToCase: (Hukm, Case) → TanzilJudgment
```

**Status**: Documented (A13 runtime implementation is out of scope for PR #22)

**Forbidden**:
- ❌ Hukm without inference license
- ❌ Tanzil without reality mapping
- ❌ Judgment without prior Murad understanding
- ❌ Direct Dal → Hukm jump (skipping all intermediate layers)

---

## Architectural Laws

### Law 1: Layer Dependency
```text
No algebra may claim outputs of a later algebra.

A6 (Ordered Dal) cannot claim A9 (Wadhʿ) outputs
A7 (Dal-Mufrad) cannot claim A10 (Dalalah) outputs
A8 (Dal-Murakkab) cannot claim A12 (Murad) outputs
```

### Law 2: No Layer Skipping
```text
Each layer depends on previous layers completing.

Cannot go: Effect (A2) → Madlul (A5) without Binding (A4)
Cannot go: Dal (A6) → Dalalah (A10) without Wadhʿ (A9)
Cannot go: Wadhʿ (A9) → Murad (A12) without Istiʿmal (A11)
```

### Law 3: Evidence Preservation
```text
Every claim must trace back to source evidence.

CandidateMadlul (A5) traces to Effect (A2) + Prior (A3)
WadhʿContract (A9) traces to OrderedDal (A6) + CandidateMadlul (A5)
Murad (A12) traces to Istiʿmal (A11) + Context
```

### Law 4: No Effect Without Source
```text
All effects must declare source or admit unknown source.

A2 (Effect) depends on A1 (Source)
```

### Law 5: No Tasawwur Without Prior
```text
All conceptualization requires prior information.

A5 (CandidateMadlul) depends on A3 (Prior) + A4 (Binding)
```

### Law 6: No Wadhʿ Without Structure
```text
Wadhʿ requires structured Dal and evidenced Madlul.

A9 (Wadhʿ) depends on A6 (OrderedDal) + A5 (CandidateMadlul)
```

### Law 7: No Istiʿmal Without Qarina
```text
Usage classification requires contextual indicators.

A11 (Istiʿmal) requires Qarina detection
```

### Law 8: No Murad Without License
```text
Intended meaning inference requires licensing conditions.

A12 (Murad) requires Context + License
```

### Law 9: No Hukm Without Inference License
```text
Judgment requires explicit inference authorization.

A13 (Hukm) requires InferenceLicense + TanzilConditions
```

---

## Forbidden Transitions

### Forbidden Transition 1: Effect → Madlul Without Prior
```text
❌ A2 → A5 directly (skips A3, A4)
✅ A2 → A3 → A4 → A5
```

### Forbidden Transition 2: RawForm → Dal Without Structure
```text
❌ Raw string → OrderedDal (skips ordering, boundaries, trace)
✅ RawForm → Ordering → Boundaries → OrderedDal (A6)
```

### Forbidden Transition 3: Dal → Madlul Without Wadhʿ
```text
❌ A6/A7/A8 → A5 directly (no Wadhʿ contract)
✅ A6 + A5 → A9 (WadhʿContract)
```

### Forbidden Transition 4: Madlul → Dalalah Without Direction
```text
❌ A5 → signification claim (no Wadhʿ, no direction)
✅ A9 (Wadhʿ) → A10 (Dalalah with direction)
```

### Forbidden Transition 5: Dalalah → Istiʿmal Without Qarina
```text
❌ A10 → usage claim (no contextual indicator)
✅ A10 + Qarina → A11 (Istiʿmal)
```

### Forbidden Transition 6: Istiʿmal → Murad Without Context
```text
❌ A11 → intent claim (no context, no license)
✅ A11 + Context + License → A12 (Murad)
```

### Forbidden Transition 7: Murad → Hukm Without Inference License
```text
❌ A12 → judgment claim (no inference authority)
✅ A12 + InferenceLicense + TanzilConditions → A13 (Hukm)
```

---

## Dal Algebra Position in General Algebra

### What is Dal Algebra?

**Dal Algebra** = A6 + A7 + A8

```text
A6: Ordered Dal Form Algebra (structure)
A7: Dal-Mufrad Algebra (individual signifier)
A8: Dal-Murakkab Algebra (composed signifier)
```

### Dal Algebra Scope

**Dal Algebra is concerned with FORM, not MEANING**:
- ✅ Ordering signifiers
- ✅ Bounding signifiers
- ✅ Composing signifiers
- ✅ Analyzing internal structure
- ✅ Morphological patterns
- ✅ Directional evidence
- ❌ Semantic interpretation
- ❌ Wadhʿ contracts
- ❌ Dalalah directions
- ❌ Pragmatic usage
- ❌ Intended meaning
- ❌ Judgment/inference

### Dal Algebra as Pre-Semantic Specialization

**Position**:
> **Dal Algebra is a pre-semantic specialization within General Algebra.**

It sits **after** effect-prior binding (A1-A5) and **before** Wadhʿ/Dalalah/Istiʿmal/Murad (A9-A13).

**Dependency chain**:
```text
Source (A1) → Effect (A2) → Prior (A3) → Binding (A4) → CandidateMadlul (A5)
                                                              ↓
                                                    OrderedDal (A6)
                                                              ↓
                                                    Dal-Mufrad (A7) ← dal_core implements this
                                                              ↓
                                                    Dal-Murakkab (A8)
                                                              ↓
                           [Both A6 and A5 required] ← Wadhʿ (A9)
                                                              ↓
                                                        Dalalah (A10)
                                                              ↓
                                                        Istiʿmal (A11)
                                                              ↓
                                                          Murad (A12)
                                                              ↓
                                                          Hukm (A13)
```

### Dal Algebra ⊂ General Algebra

**Important caveat**:
> **Dal Algebra ⊂ General Algebra is only an architectural inclusion at this stage,**
> **not yet a formally proven mathematical subalgebra.**

**What this means**:
- ✅ Dal Algebra uses General Algebra patterns (candidates, rank, residuals, trace)
- ✅ Dal Algebra respects General Algebra laws (no layer skipping, evidence preservation)
- ✅ Dal Algebra is positioned within General Algebra hierarchy
- ❌ Formal proof of subalgebra properties not yet established
- ❌ Homomorphism properties not yet proven
- ❌ Closure under operations not yet proven

**Future work**: Formal verification that Dal Algebra satisfies mathematical subalgebra axioms.

---

## Implementation Status

### Currently Implemented

**A7: Dal-Mufrad Algebra** ← ✅ **Implemented in `dal_core`**

Contracts 1-9 implemented:
1. ✅ Carrier (Unicode/UTF-8)
2. ✅ Atom (letters + diacritics)
3. ✅ Unit (syllables)
4. ✅ MorphProof (morphological evidence)
5. ✅ MufradProof (lexical closure)
6. ✅ PreSyntaxVector (syntax interface)
7. ✅ OperatorTrigger (operator candidacy)
8. ✅ OperatorRegistry (operator inventory)
9. ✅ SentenceFrame (composition container)

**A8: Dal-Murakkab Algebra** ← ✅ **Partially implemented**
- SentenceFrame provides container
- OperatorTrigger provides syntax candidacy
- Full composition algebra TBD

### Documented (Not Implemented)

- A0: General Algebra (meta-framework)
- A1: Source-of-Effect Algebra
- A2: Effect Reception Algebra
- A3: Prior-Information Algebra
- A4: Effect-Prior Binding Algebra
- A5: Tasawwur / Candidate-Madlul Algebra
- A6: Ordered Dal Form Algebra (governance in `docs/ORDERED_DAL_FORM_GOVERNANCE.md`)
- A9: Wadhʿ Contract Algebra
- A10: Dalalah Algebra
- A11: Istiʿmal Algebra
- A12: Murad Understanding Algebra
- A13: Hukm / Inference / Tanzil Algebra

---

## Allowed Claims After PR #22

### ✅ Allowed

After merging PR #22, the project can claim:

> "The project has a documented general algebra architecture map showing 13 algebraic layers from source-of-effect through hukm."

> "The project has documented that Dal Algebra (A6-A8) is a pre-semantic specialization positioned after effect-prior binding and before Wadhʿ."

> "The project has documented that Wadhʿ is not the first contract; Effect-Prior Binding (A4) is the first cognitive contract."

> "The project has documented that Madlul is not a given primitive but a constructed candidate (A5) requiring effect-prior binding."

> "The project currently implements Dal-Mufrad Algebra (A7) via dal_core Contracts 1-9."

### ❌ Forbidden

The project **cannot** claim:

> "The project has implemented General Algebra." ← Only documented

> "The project has implemented CandidateMadlul." ← Only documented

> "The project has implemented Wadhʿ." ← Only documented

> "The project understands meaning." ← Meaning understanding is A12 (Murad), not implemented

> "The project infers murad." ← A12 not implemented

> "The project produces hukm." ← A13 not implemented

> "The project does semantic linking." ← A9-A12 not implemented

---

## Out of Scope for PR #22

This PR is **documentation and governance only**.

**Explicitly forbidden** in PR #22:
- ❌ Implementing `dal_algebra.py` runtime (becomes future PR)
- ❌ Implementing RealityEffectCandidate
- ❌ Implementing SourceOfEffect classes
- ❌ Implementing PriorInformationCandidate
- ❌ Implementing EffectPriorBinding contract
- ❌ Implementing CandidateMadlulEngine
- ❌ Implementing OrderedDalEngine
- ❌ Implementing WadhContractEngine
- ❌ Implementing DalalahEngine
- ❌ Implementing IstiʿmalEngine
- ❌ Implementing MuradEngine
- ❌ Implementing HukmEngine
- ❌ Semantic interpretation
- ❌ Meaning understanding

**Only allowed** in PR #22:
- ✅ Documenting the 13-layer architecture
- ✅ Documenting laws and forbidden transitions
- ✅ Positioning Dal Algebra within General Algebra
- ✅ Clarifying Wadhʿ is not the first contract
- ✅ Governance tests verifying documentation presence

---

## Verification

To verify compliance with this architecture:

```python
# Every algebra layer must respect dependencies
def verify_layer_dependencies(operation, claimed_layer):
    """Ensure operation doesn't claim outputs from later layers."""
    required_layers = get_required_layers(claimed_layer)
    for layer in required_layers:
        assert layer_completed(layer), f"Layer {layer} required before {claimed_layer}"

    forbidden_layers = get_later_layers(claimed_layer)
    for layer in forbidden_layers:
        assert not operation.claims_output_of(layer), \
            f"Layer {claimed_layer} cannot claim output of {layer}"

# Example: Dal-Mufrad (A7) verification
def verify_dal_mufrad_boundaries():
    """Dal-Mufrad must not claim semantic outputs."""
    mufrad = create_mufrad_proof(...)

    # Allowed
    assert hasattr(mufrad, 'morphology'), "Can analyze morphology"
    assert hasattr(mufrad, 'boundaries'), "Can identify boundaries"

    # Forbidden
    assert not hasattr(mufrad, 'meaning'), "Cannot claim meaning (A5)"
    assert not hasattr(mufrad, 'wadh'), "Cannot claim wadhʿ (A9)"
    assert not hasattr(mufrad, 'murad'), "Cannot claim murad (A12)"
```

---

## Conclusion

This architecture map establishes the **complete algebraic foundation** of the project.

**Key insights**:

1. **General Algebra starts from Source-of-Effect**, not Dal or Madlul
2. **Wadhʿ is not the first contract**; Effect-Prior Binding (A4) comes first
3. **Madlul is not a primitive**; it is CandidateMadlul (A5) constructed from binding
4. **Dal is not raw form**; it is OrderedDal (A6) with structure and boundaries
5. **Dal Algebra (A6-A8) is pre-semantic**, positioned before Wadhʿ (A9)
6. **Each layer has clear dependencies**; no layer skipping allowed
7. **Currently implemented**: Only A7 (Dal-Mufrad via dal_core)
8. **Future layers** (A9-A13) are documented but not implemented

**This map prevents three major hallucinations**:
1. ❌ Assuming Madlul without effect and prior
2. ❌ Assuming Tasawwur without prior information
3. ❌ Assuming Wadhʿ without ordered dal and candidate madlul

**Dal Algebra is now correctly positioned**: A pre-semantic specialization within the General Algebra framework, not the beginning or the end of the project.

---

**Status**: ✅ Documented (no implementation)
**Related Documents**:
- `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` (A1-A6 details)
- `docs/ORDERED_DAL_FORM_GOVERNANCE.md` (A6 governance, PR #21)
- `docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md` (Dal positioning, this PR)
- `docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md` (A7-A8 scope, this PR)
- `docs/SPEC_DAL_CORE.md` (A7 implementation spec)
- `docs/DAL_CORE_COMPLIANCE.md` (A7 compliance verification)

