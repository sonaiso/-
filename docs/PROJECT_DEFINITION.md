# Project Definition

**Project Name**: General Cognitive Algebra using Arabic as Revealing Model

**Version**: Foundation Phase (5/13 layers implemented)

**Status**: Research implementation, foundation hardening required before layer expansion

---

## Short Definition

A typed, governed framework for studying how reality traces become knowledge through licensed binding operations, using Arabic linguistic precision as the first revealing model for exposing cognitive boundaries.

---

## Long Definition

This project implements **General Cognitive Algebra**: a mathematical and computational framework that models knowledge formation as governed transitions between typed domains, where every output carries full provenance (value + rank + evidence + residuals + failures + trace).

The framework consists of 13 theoretical layers from Reality (Layer -2) to Hukm/Judgment (Layer 10). Currently, **5 foundational layers are implemented**: Reality → SensoryTransfer → CognitiveCarrier → PriorInformation → Attention → Memory.

**Arabic serves as the revealing model** because its linguistic structure explicitly separates:
- **دال (Dāl)**: Signifier form (what is written/spoken)
- **مدلول (Madlūl)**: Signified meaning (lexical candidates)
- **وضع (Wadh)**: Conventional binding (social contract linking signifier to signified)
- **دلالة (Dalālah)**: Semantic relations (mutābaqah, taḍammun, iltizām)
- **إفادة (Ifādah)**: Semantic completion (complete predication)
- **حكم (Hukm)**: Judgment (application to reality)

By implementing these as **typed algebraic layers with enforced boundaries**, the project reveals what **cannot** be inferred from form alone—exposing general cognitive requirements for any knowledge system, not just language.

The project also includes **DAL_CORE**: a pre-semantic algebra for Arabic signifier analysis (D0: Graphophonemic → D7: MufradProof) that operates entirely on form without claiming meaning.

---

## Core Laws

### Constitutional Law (المبدأ الدستوري)

**لا مخرج عارٍ** (No bare output)

Every operation must return:
```
Result = value + rank + evidence + residuals + failures + trace
```

No function may emit a naked value without declaring its epistemic rank, the evidence supporting it, the residuals blocking certification, the failures contradicting it, and the trace making it replay-able.

### Layer Separation Law (قانون الفصل بين الطبقات)

**No layer may claim the outputs of a later layer**

```
Forbidden jumps:
❌ Dal (form) → Meaning (semantic)
❌ Madlūl (lexical) → Murad (speaker intent)
❌ Wadh (conventional) → Dalālah (semantic relations)
❌ Mutabaqah (correspondence) → Ifādah (completion)
❌ Ifādah (completion) → Hukm (judgment)
❌ Morphology → Semantics
❌ Syntax → Hukm
```

### Rank Discipline Law (قانون ضبط الرتبة)

**Ranks are earned, not assumed**

```
Rank hierarchy:
UNRESOLVED (0) < CANDIDATE (1) < LICENSED (2) < CERTIFIED (3)
REFUTED = fatal failure

Rules:
- LICENSED/CERTIFIED require evidence
- CERTIFIED forbidden while residuals remain
- Fatal failure forces REFUTED
- Success of later layer does NOT raise rank of earlier layer
```

### Evidence Requirement Law (قانون الدليل)

**LICENSED/CERTIFIED ranks require evidence**

```python
if rank in {Rank.LICENSED, Rank.CERTIFIED}:
    assert len(evidence) > 0, "No bare claims"
```

### Residual Preservation Law (قانون حفظ البقايا)

**Residuals must be preserved, not hidden**

```
Residual types:
- Linguistic: missing_haraka, ambiguous_formula, context_absent
- Implementation: AttributeError, gate_crash (MUST NOT appear in success)

CERTIFIED is forbidden while residuals remain.
Residuals downgrade rank or block advancement.
```

### Trace Reversibility Law (قانون عكس الأثر)

**All operations must be replay-able**

Every Result carries a Trace that records the operation name, inputs, and transformation path, enabling audit and verification.

---

## Relation Between Arabic Algebra and General Cognitive Algebra

### General Cognitive Algebra (Abstract Framework)

**13 Layers**:
```
Layer -2: Reality
Layer -1: SensoryTransfer
Layer 0: PriorInformation
Layer 0.5: CognitiveCarrier
Layer 1: Attention
Layer 2: Memory
Layer 3: Comparison
Layer 4: Tasawwur (Conceptualization)
Layer 5: Nisbah (Relational Binding)
Layer 6: Ifādah (Semantic Completion)
Layer 7: Hukm (Judgment)
Layer 8: Action
Layer 9: Effect
Layer 10: Audit
```

**Status**: Layers -2 through 2 implemented (6 of 13 layers)

### Arabic Algebra (Linguistic Specialization)

**Purpose**: Use Arabic as revealing model to test General Cognitive Algebra principles

**Layers**:
```
A0: Typed Transition Kernel (mathematical foundation)
A1: General Algebra (abstract framework - planned)
A2-A4: Pre-Semantic Dal Algebra (form analysis)
  - A2: Dal domains (D0-D7)
  - A3: Dal-Mufrad (single signifier closure)
  - A4: Dal-Murakkab (compositional structure)
A5: Wadh Algebra (signifier-signified linking)
A6: Madlūl Algebra (signified analysis)
A7: Dalālah Algebra (semantic relations)
A8: Usage Algebra (literal/figurative/transferred)
A9: Murad Algebra (speaker intent)
A10: Hukm Algebra (judgment application)
```

**Status**: A0-A4 partial, A5 partial, A6-A7 partial (Mutabaqah gate only), A8-A10 planned

### Relationship

```
General Cognitive Algebra provides the abstract framework.
Arabic Algebra instantiates it for linguistic domain.
Arabic reveals boundaries that apply to all knowledge systems.

Example:
General: Reality → SensoryTrace → Binding → Tasawwur → Hukm
Arabic:  واقع → أثر حسي → ربط → تصور → حكم
Linguistic: Form → Phoneme → Dal → Madlūl → Ifādah → Hukm

Same governance:
- No bare output
- No layer leap
- Rank discipline
- Evidence requirement
- Residual preservation
```

---

## Current Scope vs Future Scope

### Current Scope (Implemented) ✅

**General Cognitive Algebra**:
- Reality/Effect geometry (Layer -2)
- Sensory transfer geometry (Layer -1)
- PriorInformation kernel (Layer 0)
- CognitiveCarrier capacity model (Layer 0.5)
- Attention selection (Layer 1)
- Memory trace preservation (Layer 2)

**Arabic Algebra**:
- Result contract enforcement
- CPB bridge validation
- Rank policy (UNRESOLVED → CERTIFIED)
- Residual preservation (partial - needs taxonomy)
- NoLeap boundary guards (17 hard gates)
- Pure Dāl geometry (partial - Phase 2 baseline)
- Dāl/Madlūl binding (neutral relation)
- Wadh geometry (conventional linking)
- Mutabaqah gate (direct correspondence only)

**DAL_CORE**:
- D0-D7 domains
- MufradProof (single signifier closure)
- OperatorTrigger
- NahwOperatorRegistry

**Tests**: 497+ passing

### Future Scope (Planned) ⏳

**Foundation Hardening** (Next 3 PRs):
- PR-F1: Residual Taxonomy (linguistic vs implementation)
- PR-F2: Rank Policy Hardening (ceiling enforcement)
- PR-F3: LayerSpec Contract (typed layer specifications)

**Cognitive Layers**:
- Layer 3: Comparison
- Layer 4: Tasawwur (conceptualization)
- Layer 5: Nisbah (relational binding)
- Layer 6: Ifādah (semantic completion)
- Layer 7: Hukm (judgment)
- Layer 8-9: Action/Effect
- Layer 10: Audit

**Arabic Completion**:
- Full Ifādah closure
- Murad inference
- Hukm boundary implementation
- Tadammun/Iltizam gates (beyond Mutabaqah)

**DAL_CORE Completion**:
- RelationCandidate
- CaseEffectCandidate
- MurakkabProof

**Validation**:
- Golden Dataset (100 examples)
- Mutation testing
- Audit trace verification

---

## Forbidden Claims

This project must NOT claim:

1. ❌ **Complete General Cognitive Algebra** - only 5/13 layers implemented
2. ❌ **Full human-mind simulation** - foundation only
3. ❌ **Qur'anic cognitive algebra completion** - research testbed, not religious implementation
4. ❌ **Semantic understanding** - Ifādah/Murad layers not implemented
5. ❌ **Hukm production** - judgment layer not implemented
6. ❌ **CERTIFIED without evidence and zero residuals** - governance enforced but needs hardening
7. ❌ **"Arabic proves the mind"** - Arabic reveals boundaries, does not prove theory
8. ❌ **Production NLP tool** - research algebra, not production system
9. ❌ **General AI** - narrow domain-specific cognitive modeling
10. ❌ **Complete semantic interpretation** - only boundary guards exist

---

## Allowed Claims

This project MAY claim:

1. ✅ **General Cognitive Algebra foundation** - 5/13 layers with strong test coverage
2. ✅ **Governed Arabic algebra** - Dal → Binding → Wadh → Mutabaqah with NoLeap enforcement
3. ✅ **Constitutional enforcement** - no bare output, CPB bridges, rank discipline
4. ✅ **Pre-semantic Dal algebra** - D0-D7 with MufradProof
5. ✅ **Semantic boundary guards** - 17 hard gates preventing premature HUKM
6. ✅ **Arabic as revealing model** - first testbed for General Cognitive Algebra
7. ✅ **Research implementation** - proving governed binding is computationally viable
8. ✅ **Claim discipline framework** - Result contract enforced at runtime
9. ✅ **Foundation for future layers** - architecture supports expansion
10. ✅ **Partial implementation with clear gaps** - transparent about limitations

---

## Architectural Principles

### 1. Governed Binding (الربط المرخّص)

**Not** free association or pattern matching.

Every binding operation must:
- Declare input types
- Declare output types
- Provide evidence
- Preserve residuals
- Respect domain boundaries
- Return full Result (not bare value)

### 2. Claim Boundary (حد الادعاء)

**Not** claim inflation or overreach.

Every layer declares:
- What it can certify
- What it cannot certify
- What evidence it requires
- What residuals block it
- What failures refute it

### 3. Rank Discipline (ضبط الرتبة)

**Not** automatic promotion.

Rank advancement requires:
- Explicit evidence
- Resolution of residuals
- Layer-specific certification
- No inherited rank from later layers

### 4. NoLeap Enforcement (منع القفز)

**Not** direct jumps between non-adjacent domains.

Layer transitions must:
- Respect CPB bridge matrix
- Declare forbidden outputs
- Test boundary violations
- Block illegal transitions

### 5. Evidence Accountability (محاسبة الدليل)

**Not** unsupported claims.

Every LICENSED/CERTIFIED claim must:
- Cite specific evidence
- Scope evidence to domain
- Distinguish evidence types
- Allow evidence audit

---

## Terminology Conventions

- Use **"Arabic as revealing model"** not "Arabic proves the mind"
- Use **"governed binding"** not "free association"
- Use **"current implementation"** vs **"target architecture"**
- Use **"claim boundary"** and **"rank discipline"**
- Use **"foundation layers"** not "complete system"
- Use **"5/13 layers"** not "General Cognitive Algebra" (without qualification)
- Use **"research implementation"** not "production tool"
- Use **"boundary guards"** not "semantic understanding"

---

## Success Criteria

This project is successful if:

1. ✅ Constitutional foundation is enforced at runtime
2. ✅ Governance prevents claim inflation
3. ✅ Tests prove boundaries are respected
4. ✅ Arabic reveals cognitive requirements
5. ✅ Architecture supports principled expansion
6. ⏳ Foundation hardening (PR-F1/F2/F3) completes
7. ⏳ Golden dataset validates governance
8. ⏳ Cognitive layers expand systematically

---

## License

MIT

---

## Version History

- **v0.1.0**: Foundation phase (5/13 layers, PR-F0 claim audit)
- **Future**: Foundation hardening (PR-F1/F2/F3)
- **Future**: Cognitive expansion (PR-C1-C6)
- **Future**: Validation (PR-G1)

---

**Last Updated**: 2026-05-23 (PR-F0)
