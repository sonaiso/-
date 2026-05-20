# Project Algebra Architecture Map

**PR #22**: Complete architectural map from General Algebra to domain-specific specializations
**Created**: 2026-05-20
**Status**: Documentation only (no implementation)

---

## Purpose

This document maps the **complete project algebra architecture**, showing how Dal Algebra fits as one pre-semantic specialization within a larger framework that extends from form analysis through semantic interpretation to inference.

**Critical Principle**: This is an architecture map, not an implementation claim. Most layers are future work.

---

## The Complete Algebra Hierarchy (A0–A10)

### A0: General Algebra (Future Framework)

**Purpose**: Abstract framework for typed, ordered, compositional analysis with partial transitions

**Core Concepts**:
- Typed elements
- Ordered compositions
- Partial transitions (not total pipelines)
- Candidate sets (competing alternatives)
- Rank (preference ordering)
- Residuals (unresolved questions)
- Trace (reverse recoverability)
- Evidence (claim-scoped observations)
- Counter-evidence (blocking observations)
- Promotion (layer transitions)
- Blocking (constraints)
- Composition (combining units)
- Failure (explicit non-coverage)

**Status**: 🔮 **Future work** - architectural concept only

**Note**: This is NOT a claim of mathematical formalization. General Algebra represents the shared patterns we observe across domain-specific algebras, documented here to prevent duplication and ensure consistency.

---

### A1: Carrier / Ordered Form Algebra

**Purpose**: Foundational algebra of carriers, marks, atoms, and ordered sequences

**Domain**: Pre-analysis representation

**Implemented in**: `dal_core.carriers`, `dal_core.atoms`

**Core Operations**:
- Encoding text to carriers
- Attaching marks (diacritics, hamza, shadda)
- Converting to atomic units
- Preserving order and boundaries

**Governance**: PR #21 (Ordered Dal Form Governance)

**Status**: ✅ **Implemented**

**Key Law**: Dal = ordered bounded sequence, not bag of features

---

### A2: Dal Algebra (Pre-Semantic Signifier Analysis)

**Purpose**: General algebra specialized to Arabic signifier form analysis

**Domain**: Signifier (الدال) only - NO signified (المدلول)

**Position**: Specialization of General Algebra (A0) for form-only analysis

**Scope**:
- Ordered form sequences
- Internal composition
- Surface marks
- Morphological candidates
- Functional candidates
- Operator triggers
- Operator candidates
- Form-based ranking
- Form-based residuals

**Does NOT Include**:
- ❌ Meaning (المعنى)
- ❌ Signified (المدلول)
- ❌ Murad (المراد / intended meaning)
- ❌ Semantic roles
- ❌ Real-world reference
- ❌ Haqiqa/Majaz interpretation
- ❌ Usage context (حقيقة/مجاز/عرف/شرع)
- ❌ Legal/logical judgment

**Status**: 🚧 **Partially implemented** (see A3, A4 below)

**Key Boundary**: Dal Algebra ends where meaning begins

---

### A3: Dal-Mufrad Algebra (Individual Signifier Closure)

**Purpose**: Close individual signifier as ordered, bounded, internally composed form candidate

**Domain**: Single word form analysis

**Implemented Chain**:
```
Carrier (A1)
→ Atom
→ Syllable
→ Pre-morph segmentation
→ Origin (root vs frozen)
→ Template (pattern)
→ Identity axes (lexical lookup)
→ Surface effects
→ Form-feature candidates
→ MufradProof (closure)
```

**Current Implementation**:
- `dal_core.pipeline.analyze_dal_mufrad()`
- `dal_core.mufrad_proof.MufradProof`
- Contracts 1-3 (Carrier, Atom, Unit)

**Outputs**:
- `MufradProof` with:
  - Root candidates (if applicable)
  - Wazn candidates (if applicable)
  - Stem proof
  - Clitic proof
  - Segmentation proof
  - Surface effects
  - Rank
  - Residuals
  - Trace

**Does NOT Output**:
- ❌ Meaning
- ❌ Murad
- ❌ Semantic interpretation
- ❌ Syntax role (that's A4's job)
- ❌ Case effect (that's A4's job)

**Status**: ✅ **Implemented** (Phase 0/1)

**Key Law**: Mufrad certifies form, not meaning

---

### A4: Dal-Murakkab Algebra (Composed Signifier Structure)

**Purpose**: Compose already-closed `MufradProof` objects into governed structure candidates

**Domain**: Multi-word form composition (still pre-semantic)

**Implemented Chain**:
```
MufradProof (A3)
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

**Current Implementation**:
- `PreSyntaxMufradVector` (PR #10)
- `SentenceFrameCandidate` (PR #12)
- `CaseSignMatrix` (PR #13)
- `OperatorTriggerPotential` (PR #14)
- `NahwOperatorRegistry` (PR #15/16)
- `OperatorCandidate` (PR #17)

**Future Components**:
- `RelationCandidate` (إسناد/تضمين/تقييد candidates)
- `CaseEffectCandidate` (رفع/نصب/جر/جزم candidates)
- `MurakkabProof` (compositional closure)

**Critical Laws**:
1. **Murakkab does not raise Mufrad rank** - composition cannot improve form quality
2. **Murakkab inherits Mufrad residuals** - unresolved questions propagate
3. **Murakkab preserves Mufrad competitors** - alternatives remain visible
4. **Murakkab does not create meaning** - still form-only
5. **Murakkab does not infer murad** - no intended meaning

**Status**: 🚧 **Partially implemented**

**Key Law**: Murakkab certifies composition candidates, not intended meaning

---

### A5: Wadh' Algebra (Signifier-Signified Linking)

**Purpose**: Licensed linking between dal (signifier) and madlul (signified)

**Domain**: Lexical semantics - mapping form to conventional meaning

**Scope**:
- Lexicon-based dal → madlul mappings
- Conventional significations (وضع)
- Polysemy tracking (multiple madlul for one dal)
- Homonymy tracking (same form, unrelated meanings)

**Does NOT Include**:
- ❌ Contextual meaning selection (that's A8/A9)
- ❌ Murad inference (that's A9)
- ❌ Usage interpretation (حقيقة/مجاز - that's A8)
- ❌ Final judgment (that's A10)

**Status**: 🔮 **Future work**

**Key Law**: Wadh' links signifier to signified, but does not infer murad

**Boundary from A4**: This is where meaning **begins**. A4 (Dal-Murakkab) must be stable before crossing this boundary.

---

### A6: Madlul Algebra (Signified Meaning Space)

**Purpose**: Algebra of signified meanings, independent of particular signifiers

**Domain**: Conceptual/semantic space

**Scope**:
- Concept definitions
- Semantic features
- Conceptual relations
- Semantic fields
- Meaning primitives

**Does NOT Include**:
- ❌ Context-dependent interpretation (that's A8/A9)
- ❌ Speaker intent (that's A9)
- ❌ Inference (that's A10)

**Status**: 🔮 **Future work**

**Key Law**: Madlul represents conventional meaning, not situated interpretation

---

### A7: Dalalah Algebra (Signification Modes)

**Purpose**: Algebra of المطابقة / التضمن / الالتزام (conformative, inclusive, implicative signification)

**Domain**: How signifiers relate to their signifieds

**Scope**:
- المطابقة (mutabaqa): Direct/conformative signification
- التضمن (tadammun): Inclusive/partitive signification
- الالتزام (iltizam): Implicative/entailed signification

**Example**:
- "بيت" (house) signifies:
  - المطابقة: The whole house
  - التضمن: Parts of house (wall, roof, etc.)
  - الالتزام: What house implies (shelter, ownership, etc.)

**Status**: 🔮 **Future work**

**Key Law**: Dalalah analyzes signification modes, but does not replace usage context

---

### A8: Usage Algebra (Contextual Application)

**Purpose**: Algebra of حقيقة / مجاز / نقل / عرف / شرع (literal, metaphorical, transferred, conventional, legal usage)

**Domain**: How meanings are applied in context

**Scope**:
- حقيقة (haqiqa): Literal/original usage
- مجاز (majaz): Metaphorical/figurative usage
- نقل (naql): Semantic transfer
- عرف (urf): Conventional usage
- شرع (shar'): Legal/religious usage

**Requires**:
- Context evidence
- Usage domain identification
- Conventionalization tracking

**Status**: 🔮 **Future work**

**Key Law**: Usage requires context; cannot be inferred from form alone

---

### A9: Murad Algebra (Intended Meaning)

**Purpose**: Algebra of speaker/author intended meaning in context

**Domain**: Pragmatic interpretation

**Scope**:
- Speaker intent inference
- Context-dependent meaning selection
- Ambiguity resolution
- Implicature
- Presupposition

**Requires**:
- Completed dal analysis (A3/A4)
- Wadh' mapping (A5)
- Available madlul options (A6)
- Signification mode analysis (A7)
- Usage context (A8)
- Speaker/context evidence

**Status**: 🔮 **Future work**

**Key Law**: Murad requires context, speaker intent evidence, and ambiguity resolution

---

### A10: Hukm Algebra (Inference / تنزيل)

**Purpose**: Algebra of legal, logical, or practical judgment based on interpreted meaning

**Domain**: Inference and application

**Scope**:
- Legal judgment (الحكم الشرعي)
- Logical inference
- Practical application (تنزيل)
- Rule application

**Requires**:
- All previous layers (A1-A9)
- Domain rules (legal, logical, etc.)
- Evidence standards
- Authority sources

**Status**: 🔮 **Future work**

**Key Law**: Hukm is the final layer; no algebra may skip to it

---

## The Central Architectural Law

### No Algebra May Claim the Outputs of a Later Algebra

This law prevents invalid cross-layer claims:

| Algebra | ✅ May Certify | ❌ May NOT Certify |
|---------|---------------|-------------------|
| A1 (Carrier) | Ordered form, marks, atoms | Syllables, roots, meaning |
| A2 (Dal) | Form candidates | Meaning, murad |
| A3 (Dal-Mufrad) | Individual form closure | Meaning, syntax role, murad |
| A4 (Dal-Murakkab) | Composition candidates | Intended meaning, final case |
| A5 (Wadh') | Dal→Madlul links | Contextual meaning, murad |
| A6 (Madlul) | Conventional meanings | Context-dependent interpretation |
| A7 (Dalalah) | Signification modes | Usage context, murad |
| A8 (Usage) | Contextual application | Speaker intent, murad |
| A9 (Murad) | Intended meaning | Legal/logical judgment |
| A10 (Hukm) | Final judgment | (Terminal layer) |

**Enforcement**: Each layer may only produce outputs within its authority. Cross-layer promotion requires explicit evidence and licensed transition.

---

## Architectural Relations

### Dal Algebra ⊂ General Algebra

**Interpretation**: Dal Algebra is a **domain specialization** of General Algebra

**Caution**: This is an **architectural inclusion**, not yet a formally proven mathematical subalgebra

**What This Means**:
- Dal Algebra uses patterns from General Algebra (candidates, rank, residuals, trace)
- General Algebra is abstracted from observed patterns across specializations
- This relationship is documented for architecture consistency, not claimed as mathematical proof

### Dal-Mufrad ⊂ Dal Algebra

Dal-Mufrad specializes Dal Algebra to **individual signifier analysis**

### Dal-Murakkab ⊂ Dal Algebra

Dal-Murakkab specializes Dal Algebra to **compositional signifier analysis**

### Dal Algebra ⊥ Semantic Algebras

Dal Algebra (A2-A4) is **orthogonal to** semantic algebras (A5-A10):
- Dal operates on form (signifier)
- Semantic operates on meaning (signified, murad, hukm)
- Crossing boundary requires licensed Wadh' linking (A5)

---

## Implementation Status Summary

| Layer | Status | Implementation |
|-------|--------|----------------|
| A0 (General) | 🔮 Future | Architecture concept |
| A1 (Carrier) | ✅ Done | `dal_core.carriers`, `dal_core.atoms` |
| A2 (Dal) | 🚧 Partial | See A3, A4 |
| A3 (Dal-Mufrad) | ✅ Phase 0/1 | `dal_core.pipeline`, `MufradProof` |
| A4 (Dal-Murakkab) | 🚧 Partial | `PreSyntaxMufradVector`, `OperatorCandidate` |
| A5 (Wadh') | 🔮 Future | Not started |
| A6 (Madlul) | 🔮 Future | Not started |
| A7 (Dalalah) | 🔮 Future | Not started |
| A8 (Usage) | 🔮 Future | Not started |
| A9 (Murad) | 🔮 Future | Not started |
| A10 (Hukm) | 🔮 Future | Not started |

---

## Prohibited Claims

After this PR, we **may NOT claim**:

- ❌ "The project has implemented General Algebra"
- ❌ "The project has implemented complete Dal Algebra"
- ❌ "The project has implemented semantic linking"
- ❌ "The project understands meaning"
- ❌ "The project produces Murad"
- ❌ "The project produces Hukm"
- ❌ "Dal Algebra is a proven mathematical subalgebra of General Algebra"

---

## Allowed Claims

After this PR, we **may claim**:

- ✅ "The project has a documented architecture map positioning Dal Algebra as a pre-semantic specialization of future General Algebra"
- ✅ "The project implements Dal-Mufrad (individual signifier closure) at Phase 0/1"
- ✅ "The project partially implements Dal-Murakkab (compositional signifier structure)"
- ✅ "The project has a roadmap for semantic linking after Dal-only analysis is stable"

---

## Architectural Decisions

### Why Separate Dal from Semantic Algebras?

**Reason**: Linguistic principle of signifier/signified distinction

- Dal (الدال): Signifier - form, structure, surface
- Madlul (المدلول): Signified - conventional meaning
- Murad (المراد): Intended meaning in context
- Hukm (الحكم): Judgment/inference

**Benefit**: Clear boundaries prevent meaning hallucination in form analysis

### Why A0 (General Algebra) is Future Work?

**Reason**: Abstraction comes from concrete implementations, not top-down design

**Approach**:
1. Build domain-specific algebras (Dal, future others)
2. Observe common patterns
3. Extract General Algebra as documented framework
4. Validate consistency

**Current Status**: A0 documented as concept to guide Dal Algebra design

### Why 10 Layers?

**Reason**: Captures traditional Arabic linguistic/legal analysis pipeline from form to judgment

**Not arbitrary**: Each layer corresponds to established Arabic linguistic categories

---

## Next Steps

See `docs/PROJECT_ALGEBRA_ROADMAP.md` for detailed sequencing

**Immediate** (after PR #22):
- PR #23: Minimal Dal Transition Signature (implement A2 contracts)
- PR #24: Rank Algebra
- PR #25: Residual Algebra

**Dal-Mufrad completion**:
- 8-layer candidate implementations (graphophonemic → judgment)

**Dal-Murakkab completion**:
- RelationCandidate
- CaseEffectCandidate
- MurakkabProof

**Only after Dal stable**:
- A5: Wadh' / Dal-Madlul linking
- A6-A10: Semantic algebras

---

**Document Version**: 1.0
**Created**: 2026-05-20
**Author**: Claude Sonnet 4.5
**PR**: #22 (Documentation only)
**Status**: Architecture map - not implementation claim
