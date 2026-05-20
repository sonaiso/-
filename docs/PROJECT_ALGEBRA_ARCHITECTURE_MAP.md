# Project Algebra Architecture Map

**PR #22**: Full algebra architecture positioning
**Status**: Architecture map (no runtime implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document maps the **complete algebra architecture** for this project, positioning each specialized algebra within the **Typed Transition Algebra Kernel**.

The architecture consists of **11 layers** (A0-A10), from foundational kernel to inference.

**Critical Principle**:

```text
No algebra may claim the outputs of a later algebra.
```

---

## The 11-Layer Architecture

### A0: Typed Transition Algebra Kernel

**Purpose**: Foundational mathematical kernel

**Defines**:
- Carrier (successful typed objects)
- Transitions (typed candidate generators)
- CandidateSet contract
- Failure semantics
- Claim-scoped proof
- Domain-scoped equivalence
- Conditional composition
- Local neutral elements

**Status**: Defined in `TYPED_TRANSITION_ALGEBRA_KERNEL.md`

**Authority**: Governs all other algebras

---

### A1: General Algebra

**Purpose**: Abstract framework for all transition systems

**Future definition** will include:
- Abstract typed domains
- Generic transition contracts
- Universal evidence model
- Cross-domain boundaries
- Composition laws
- Rank algebra
- Residual algebra
- Trace algebra

**Status**: **Architecture placeholder** (not yet defined)

**Caution**:

```text
General Algebra is the future abstract framework.
Dal Algebra (A2-A4) is a pre-semantic specialization.

Dal Algebra ⊂ General Algebra is an architectural inclusion,
NOT a formally proven mathematical subalgebra.
```

**Authority**: Will govern all specific algebras when defined

---

### A2: Pre-Semantic Dal Algebra

**Purpose**: Signifier form analysis (no semantic interpretation)

**Scope**: Surface form to closed signifier

**Domains**:
```text
D0: Graphophonemic (رسم/صوت)
D1: Syllabic (مقطع)
D2: Pre-Morph (ما قبل الصرف)
D3: Origin (أصل)
D4: Template (وزن)
D5: Identity Axis (محور الهوية)
D6: Directional Analysis (تحليل اتجاهي)
D7: Judgment (حكم صرفي)
```

**Outputs**:
- `DalForm` (closed signifier form)
- **NOT** `Madlul` (signified)
- **NOT** `Murad` (intended meaning)

**Status**: Partially implemented in `dal_core`

**Authority**: May certify **form only**, not meaning

---

### A3: Dal-Mufrad Algebra

**Purpose**: Close individual signifier as ordered, bounded form

**Scope**: Single-word signifier closure

**Includes**:
```text
carrier
mark
atom
syllable
pre-morph
origin
template
identity axes
surface effects
form-feature candidates
rank
residuals
trace
competitors
```

**Does NOT include**:
```text
meaning
semantic interpretation
murad
syntax role
case effect
real-world reference
```

**Output**: `MufradProof` (composition-ready closed signifier)

**Status**: Implemented in `dal_core.mufrad_proof`

**Authority**: Certifies **single signifier closure**, not composition or meaning

---

### A4: Dal-Murakkab Algebra

**Purpose**: Compose closed signifiers into governed structure candidates

**Scope**: Multi-word signifier composition (pre-semantic)

**Chain**:
```text
MufradProof
→ PreSyntaxMufradVector
→ SentenceFrameCandidate
→ CaseSignMatrix
→ OperatorTriggerPotential
→ NahwOperatorRegistry
→ OperatorCandidate
→ (future) RelationCandidate
→ (future) CaseEffectCandidate
→ (future) MurakkabProof
```

**Critical Laws**:

```text
Murakkab does NOT raise Mufrad rank.
Murakkab inherits Mufrad residuals.
Murakkab preserves Mufrad competitors.
Murakkab does NOT create meaning.
Murakkab does NOT infer murad.
```

**Status**: Partially implemented (OperatorTrigger through OperatorCandidate)

**Authority**: Certifies **compositional structure candidates**, not meaning or intent

---

### A5: Wadh' Algebra (Signifier-Signified Linking)

**Purpose**: License transition from signifier to signified

**Scope**: Dal-Madlul boundary

**Critical Transition**:

```text
WadhContract: DalForm × Context → MadlulCandidate ∪ Failure
```

**Requirements**:
- Lexical attestation (سماع)
- Conventional usage (عرف)
- Shariah usage (شرع) where applicable
- Context evidence (قرينة)

**Does NOT**:
- Infer meaning from form alone
- Transfer rank from dal to madlul
- Assume compositional semantics

**Status**: **Not yet implemented** (requires lexicon with wadh' attestations)

**Authority**: Licenses **signifier-signified link**, not meaning interpretation

---

### A6: Madlul Algebra (Signified)

**Purpose**: Analyze signified candidates (meanings associated with signifiers)

**Scope**: Lexical meaning space

**Includes**:
- Lexical meaning candidates
- Polysemy (تعدد المعنى)
- Homonymy (تشارك لفظي)
- Semantic features
- Meaning relations

**Does NOT include**:
- Speaker intent
- Contextual disambiguation
- Pragmatic inference
- Figurative interpretation

**Status**: **Not yet implemented**

**Authority**: Analyzes **lexical meaning**, not usage or intent

---

### A7: Dalalah Algebra (Semantic Relations)

**Purpose**: Analyze semantic relation types

**Three core relations**:

```text
المطابقة (Mutābaqah) - Direct correspondence
التضمن (Taḍammun)    - Inclusion/containment
الالتزام (Iltizām)    - Entailment/commitment
```

**Scope**: Meaning-to-meaning relations

**Does NOT**:
- Replace usage context
- Infer speaker intent
- Resolve ambiguity

**Status**: **Not yet implemented**

**Authority**: Classifies **semantic relation types**, not contextual meaning

---

### A8: Usage Algebra (استعمال)

**Purpose**: Analyze usage types and contexts

**Usage dimensions**:

```text
حقيقة (Ḥaqīqah)     - Literal/primary usage
مجاز (Majāz)         - Figurative/metaphorical usage
نقل (Naql)           - Transferred usage
عرف (ʿUrf)           - Conventional usage
شرع (Sharʿ)          - Shariah-specific usage
```

**Requires**:
- Textual evidence
- Conventional attestation
- Community practice evidence

**Does NOT**:
- Infer intent from form
- Override lexical wadh' without evidence
- Assume speaker meaning

**Status**: **Not yet implemented**

**Authority**: Classifies **usage type**, not speaker intent

---

### A9: Murad Algebra (Intended Meaning)

**Purpose**: Infer intended meaning from speaker/writer

**Scope**: Pragmatic interpretation

**Requires**:
- Context evidence (قرينة)
- Speaker-intent markers
- Ambiguity resolution
- Discourse context

**Multi-layer resolution**:

```text
DalForm → Madlul candidates → Usage context → Dalalah relations → Murad inference
```

**Critical Distinction**:

```text
Murad ≠ Madlul
Murad = speaker-intended meaning
Madlul = lexical signified
```

**Status**: **Not yet implemented**

**Authority**: Infers **intended meaning** with context evidence, not standalone form

---

### A10: Hukm Algebra (Inference / تنزيل)

**Purpose**: Apply meanings to real-world instances (تنزيل الأحكام)

**Scope**: Practical application

**Requires**:
- Murad (intended meaning)
- Real-world context (واقع)
- Application conditions (شروط)
- Blocking factors (موانع)

**Examples**:
- Legal rulings (أحكام فقهية)
- Inference chains (استدلال)
- Practical application (تنزيل)

**Critical Caution**:

```text
Hukm requires human judgment.
Automated inference has severe limitations.
This layer is aspirational, not achievable through form analysis alone.
```

**Status**: **Not in scope** (future research)

**Authority**: **Requires external authority** (human judgment, legal experts)

---

## Layer Dependency Graph

```text
A10: Hukm
  ↑
A9: Murad
  ↑
A8: Usage ← requires wadh' + context
  ↑
A7: Dalalah ← requires madlul
  ↑
A6: Madlul ← requires wadh' link
  ↑
A5: Wadh' ← dal-madlul boundary
  ↑
A4: Dal-Murakkab ← composition
  ↑
A3: Dal-Mufrad ← individual signifier
  ↑
A2: Pre-Semantic Dal ← form analysis
  ↑
A1: General Algebra (future)
  ↑
A0: Typed Transition Kernel
```

---

## Critical Boundaries

### Pre-Semantic / Semantic Boundary

**Pre-Semantic (A2-A4)**:
- Dal form analysis
- Morphological structure
- Compositional structure
- **NO meaning inference**

**Semantic (A5+)**:
- Wadh' linking
- Madlul analysis
- Dalalah relations
- Usage contexts
- Murad inference
- Hukm application

**Boundary is A5 (Wadh')**:

```text
Before A5: Form analysis only
After A5:  Meaning analysis begins
```

---

## The Fundamental Law

### No Algebra May Claim Later Outputs

```text
No algebra may claim the outputs of a later algebra.
```

**Violations (forbidden)**:

```text
❌ Dal-Mufrad claims meaning
❌ Dal-Murakkab claims murad
❌ Wadh' claims speaker intent
❌ Dalalah claims usage context
❌ Murad claims legal ruling
```

**Allowed claims**:

```text
✅ Dal-Mufrad certifies form
✅ Dal-Murakkab certifies composition candidates
✅ Wadh' links signifier to signified
✅ Dalalah analyzes semantic relations
✅ Usage classifies usage type
✅ Murad infers intended meaning with context
```

---

## Examples Across Layers

### Example 1: "كَتَبَ"

```text
A2-A3: Dal-Mufrad
  - Form: ك-ت-ب with فَعَلَ pattern
  - Rank: TAWATUR (widely attested signifier)
  - Certificate: Form closed as MufradProof

A5: Wadh'
  - Link: كَتَبَ → "to write" (lexical attestation)
  - Context: Requires subject

A6: Madlul
  - Meaning candidates: ["write", "inscribe", "record"]
  - Polysemy: Yes (multiple related meanings)

A7: Dalalah
  - المطابقة: Direct "write" meaning
  - التضمن: Includes "use pen/tool"
  - الالتزام: Entails "produce written text"

A8: Usage
  - حقيقة: Literal writing (primary usage)
  - مجاز: Figurative "destiny writes" (metaphorical)

A9: Murad
  - Context: "كَتَبَ اللهُ لَكَ الخَيْرَ"
  - Intent: "Allah decreed good for you" (figurative usage)
```

### Example 2: "مَكْتَب"

```text
A2-A3: Dal-Mufrad
  - Form: م-ك-ت-ب with مَفْعَل pattern
  - Certificate: Form closed as MufradProof
  - Note: Does NOT infer "place" meaning from form alone

A5: Wadh'
  - Link: مَكْتَب → "office/desk" (lexical attestation required)
  - Cannot infer from pattern alone (مَفْعَل ambiguous)

A6: Madlul
  - Meaning: "place of writing" OR "time of writing" OR "written document"
  - Requires context to disambiguate

A8: Usage
  - عرف: "Office" (modern conventional usage dominant)
```

---

## Implementation Status

### ✅ Partially Implemented

- **A0**: Kernel defined (this PR)
- **A2**: Dal domains partially implemented (`dal_core`)
- **A3**: MufradProof implemented
- **A4**: OperatorTrigger through OperatorCandidate implemented

### ❌ Not Yet Implemented

- **A1**: General Algebra (future abstract framework)
- **A4**: RelationCandidate, CaseEffectCandidate, MurakkabProof
- **A5**: Wadh' Algebra (requires lexicon with attestations)
- **A6**: Madlul Algebra
- **A7**: Dalalah Algebra
- **A8**: Usage Algebra
- **A9**: Murad Algebra
- **A10**: Hukm Algebra (aspirational)

---

## Roadmap Integration

This architecture map informs the project roadmap:

```text
PR #22: Architecture Map (this PR)
PR #23-36: Dal-only completion (A2-A4)
PR #37+: Wadh' boundary (A5)
Future: Madlul/Dalalah/Usage (A6-A8)
Future: Murad inference (A9)
Research: Hukm application (A10)
```

See `PROJECT_ALGEBRA_ROADMAP.md` for detailed PR sequence.

---

## Allowed Claim After This PR

```text
The project has a documented algebra architecture map positioning Dal Algebra (A2-A4) as a pre-semantic specialization within a Typed Transition Algebra Kernel (A0), with future layers defined up to Hukm inference (A10).
```

## Forbidden Claim After This PR

```text
The project has implemented General Algebra.
The project has implemented semantic linking.
The project understands meaning.
The project produces Murad or Hukm.
The project has a complete algebra.
```

---

**Version**: 1.0.0
**Status**: Architecture map complete
**Scope**: Documentation only (no runtime implementation)
