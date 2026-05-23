# General Cognitive Algebra Using Arabic as Revealing Model

[![Tests](https://img.shields.io/badge/tests-497%2B_passing-success)]() [![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()

**Package**: `bayan-fvafk` v0.1.0 | **Architecture**: General Cognitive Algebra (5/13 layers implemented)

---

## Mission

This project implements **General Cognitive Algebra**: a typed, governed framework for studying how reality traces become knowledge through licensed binding operations. Arabic serves as the first **revealing model** because its linguistic precision exposes the boundaries between signifier (دال), signified (مدلول), semantic relations (دلالة), and judgment (حكم).

**What this project is**:
- A research implementation of General Cognitive Algebra foundations (Reality → Sensory → Processor → Prior → Attention → Memory)
- A pre-semantic Arabic algebra (Dal → Binding → Wadh → Mutabaqah) with governed transitions
- A constitutional framework enforcing: **لا مخرج عارٍ** (no bare output)
- A testbed proving that `Result = value + rank + evidence + residuals + failures + trace`

**What this project is NOT**:
- ❌ A complete General Cognitive Algebra (only 5/13 layers implemented)
- ❌ A full human-mind simulation
- ❌ A semantic understanding system (Ifādah/Murad/Hukm layers are planned, not implemented)
- ❌ A production Arabic NLP tool (it is a research algebra)

---

## Core Constitution

> **لا مخرج عارٍ.**
> Every `Result = value + rank + evidence + residuals + failures + trace`.

No operation may emit a bare value. Every output must declare:
- **Rank** of its claim (UNRESOLVED < CANDIDATE < LICENSED < CERTIFIED)
- **Evidence** that supports it
- **Residuals** that block certification
- **Failures** that contradict it
- **Trace** that makes it replay-able

### Constitutional Laws

1. **No bare output**: All results carry full provenance
2. **No leap**: No layer may claim outputs of a later layer
3. **Rank discipline**: CERTIFIED forbidden while residuals remain
4. **Evidence requirement**: LICENSED/CERTIFIED require evidence
5. **Failure forces refutation**: Fatal failures force REFUTED rank
6. **Trace preservation**: All operations are replay-able

---

## Current Implementation vs Target Architecture

### ✅ Implemented (Foundation Layers)

**General Cognitive Algebra (5/13 layers)**:
```
Reality (-2) ✅ → SensoryTransfer (-1) ✅ → CognitiveCarrier (0.5) ✅
→ PriorInformation (0) ✅ → Attention (1) ✅ → Memory (2) ✅
```

**Arabic Algebra (Foundation)**:
```
Pure Dāl Geometry (partial) ✅
→ Dāl/Madlūl Binding ✅
→ Wadh Geometry ✅
→ Mutabaqah Gate ✅
→ Semantic Boundary Guards ✅
```

**DAL_CORE (Pre-Semantic)**:
```
D0: Graphophonemic ✅ → D1: Syllabic ✅ → D2: PreMorph ✅
→ D3: Origin ✅ → D4: Template ✅ → D7: MufradProof ✅
→ OperatorTrigger ✅ → NahwOperatorRegistry ✅
```

**Governance**:
```
Result Contract ✅ | CPB Bridge Enforcement ✅ | Rank Policy ✅
NoLeap Tests ✅ | Residual Preservation ✅
```

### ⏳ Planned (Not Yet Implemented)

**Cognitive Layers**:
- Comparison (Layer 3)
- Tasawwur (conceptualization)
- Nisbah (relational binding)
- Ifādah (semantic completion)
- Hukm (judgment)
- Action/Effect
- Audit Trace

**Arabic Completion**:
- Ifādah closure
- Hukm boundary implementation
- Murad (speaker intent) inference
- Full semantic composition

**DAL_CORE Completion**:
- RelationCandidate
- CaseEffectCandidate
- MurakkabProof

**Governance Hardening**:
- LayerSpec formal contract (PR-F3)
- Residual taxonomy (linguistic vs implementation) (PR-F1)
- Rank ceiling enforcement (PR-F2)
- Golden Dataset (100 examples)

See [`docs/CLAIM_BOUNDARY_AUDIT.md`](docs/CLAIM_BOUNDARY_AUDIT.md) for complete status.

---

## How Arabic Functions as Revealing Model

Arabic exposes cognitive algebra boundaries through its precision:

1. **دال (Dāl)**: Signifier form alone ≠ meaning
2. **مدلول (Madlūl)**: Signified candidates ≠ speaker intent
3. **وضع (Wadh)**: Conventional linking ≠ semantic understanding
4. **دلالة (Dalālah)**: Semantic relation ≠ pragmatic inference
5. **المطابقة (Mutabaqah)**: Direct correspondence ≠ full meaning
6. **إفادة (Ifādah)**: Semantic completion ≠ judgment
7. **حكم (Hukm)**: Judgment requires evidence beyond form

By enforcing these boundaries computationally, we reveal what **cannot** be inferred from form alone—exposing the general cognitive requirements for any knowledge system.

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/sonaiso/Eqratech_Hussein_Hiyassat_Project.git
cd Eqratech_Hussein_Hiyassat_Project

# Install dependencies
pip install -r requirements.txt

# Install as editable package
pip install -e .
```

### Run Tests

```bash
# Full test suite (497+ tests)
PYTHONPATH=src pytest -q

# Algebra governance tests
PYTHONPATH=src pytest tests/fvafk/algebra/ -v

# GFA foundation tests
PYTHONPATH=src pytest tests/gfa/ -v

# DAL_CORE tests
PYTHONPATH=src pytest tests/dal_core/ -v
```

### CLI Usage

```bash
# Basic analysis
PYTHONPATH=src python -m fvafk.cli "كَتَبَ" --morphology --json

# Algebra decision tree (demonstrates Result contract)
python -c "
from fvafk.algebra import ArabicAlgebraDecisionTree
result = ArabicAlgebraDecisionTree().analyze('كاتب')
print(f'Rank: {result.rank}')
print(f'Residuals: {result.residuals}')
print(f'Certificate allowed: {result.certificate_allowed}')
"
```

---

## Project Structure

```
├── src/
│   ├── fvafk/                  # Arabic Algebra + FVAFK Pipeline
│   │   ├── algebra/            # Correspondence-Preserving Algebra
│   │   │   ├── core.py         # Result contract, Rank, Evidence, Residual
│   │   │   ├── cpb.py          # Bridge enforcement
│   │   │   ├── morphology/     # Governed morphology operations
│   │   │   ├── syntax/         # Governed syntax operations
│   │   │   ├── semantics/      # Semantic boundary guards
│   │   │   └── lafzi_madlul/   # Lafẓī Madlūl Fractal Algebra
│   │   ├── c1/                 # Encoding layer
│   │   ├── c2a/                # Phonology gates
│   │   ├── c2b/                # Morphology (roots, patterns)
│   │   └── syntax/             # Syntax layer
│   │
│   ├── gfa/                    # General Foundational Algebra
│   │   ├── reality/            # RealityGeometry (Layer -2)
│   │   ├── sensory_transfer/   # SensoryTransfer (Layer -1)
│   │   ├── proto_prior/        # FirstPriorUnit (Layer 0)
│   │   ├── cognitive_carrier/  # CognitiveCarrier (Layer 0.5)
│   │   ├── attention/          # AttentionGeometry (Layer 1)
│   │   ├── foundations/memory/ # MemoryGeometry (Layer 2)
│   │   └── methods/            # Rational methods, Wadh, Binding
│   │
│   └── dal_core/               # Pre-Semantic Dal Algebra (D0-D7)
│       ├── carriers.py         # Typed carriers
│       ├── atoms.py            # Atomic analysis
│       ├── syllable_candidate.py  # Syllabic layer
│       ├── mufrad_proof.py     # Single signifier closure
│       ├── operator_trigger.py # Operator triggering
│       └── nahw_operator_registry.py  # Nahw operators
│
├── tests/                      # Test suite (497+ tests passing)
├── docs/                       # Architecture documentation
│   ├── CLAIM_BOUNDARY_AUDIT.md    # Implementation status audit
│   ├── PROJECT_DEFINITION.md      # Core definitions
│   ├── NEXT_PHASE_PLAN.md         # Foundation hardening plan
│   ├── ARABIC_ALGEBRA_ARCHITECTURE.md
│   ├── ARABIC_ALGEBRA_ROADMAP.md
│   └── PROJECT_ALGEBRA_ARCHITECTURE_MAP.md
└── pyproject.toml              # Package metadata
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [CLAIM_BOUNDARY_AUDIT.md](docs/CLAIM_BOUNDARY_AUDIT.md) | **START HERE**: Implementation status audit |
| [PROJECT_DEFINITION.md](docs/PROJECT_DEFINITION.md) | Core laws and boundaries |
| [NEXT_PHASE_PLAN.md](docs/NEXT_PHASE_PLAN.md) | Foundation hardening (PR-F1/F2/F3) |
| [TERMINOLOGY.md](docs/TERMINOLOGY.md) | Precise definitions |
| [ARABIC_ALGEBRA_ARCHITECTURE.md](docs/ARABIC_ALGEBRA_ARCHITECTURE.md) | Constitution and CPB contract |
| [ARABIC_ALGEBRA_ROADMAP.md](docs/ARABIC_ALGEBRA_ROADMAP.md) | Phase plan (0-5.5 implemented) |
| [PROJECT_ALGEBRA_ARCHITECTURE_MAP.md](docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md) | 11-layer architecture (A0-A10) |

---

## Current Limitations

### What We Cannot Do Yet

1. **Semantic Completion**: Ifādah layer not implemented
2. **Speaker Intent**: Murad layer not implemented
3. **Judgment**: Hukm layer not implemented
4. **Full Composition**: MurakkabProof not implemented
5. **Golden Validation**: No golden dataset yet

### Known Governance Gaps (To Be Fixed)

1. **Residual Taxonomy**: No separation of linguistic residuals from implementation failures (PR-F1)
2. **Rank Ceiling**: No automatic enforcement of rank ceilings in binding operations (PR-F2)
3. **LayerSpec**: No formal typed layer specification contract (PR-F3)
4. **Wadh Guard**: WadhGate does not verify Dal rank strength yet
5. **Golden Dataset**: No canonical test suite (PR-G1)

See [`docs/GAP_HALLUCINATION_AUDIT.md`](docs/GAP_HALLUCINATION_AUDIT.md) for complete gap analysis.

---

## Next Phase Priorities

**Foundation Hardening (Before New Features)**:

1. **PR-F1**: Residual Taxonomy Formalization
   - Separate `LinguisticResidual` from `ImplementationFailure`
   - Implementation exceptions must not appear as successful residuals

2. **PR-F2**: Rank Policy Hardening
   - Enforce rank ceilings
   - Prevent CANDIDATE → CERTIFIED promotion without evidence
   - Define required evidence kinds per layer

3. **PR-F3**: LayerSpec Contract
   - Explicit typed layer specification
   - Each layer declares input_type, output_type, forbidden_outputs, required_evidence

After foundation hardening:
- PR-C1: PriorInformationSystem formal contract
- PR-C2: General governed_binding function
- PR-C3-C6: Tasawwur/Nisbah/Ifadah/Hukm layers
- PR-G1: Golden Dataset (100 examples)

See [`docs/NEXT_PHASE_PLAN.md`](docs/NEXT_PHASE_PLAN.md) for detailed specifications.

---

## Testing Commands

```bash
# All tests
pytest

# Algebra tests only
pytest tests/fvafk/algebra/ -v

# GFA foundation tests
pytest tests/gfa/ -v

# Semantic boundary guards
pytest tests/fvafk/algebra/test_semantic_boundary_hardening.py -v

# Result invariants
pytest tests/fvafk/algebra/test_result_invariants.py -v

# CPB enforcement
pytest tests/fvafk/algebra/test_bridge_matrix.py -v
```

---

## Forbidden Claims

This repository must NOT claim:

- ❌ Complete General Cognitive Algebra (only 5/13 layers)
- ❌ Full human-mind simulation
- ❌ Qur'anic cognitive algebra implementation
- ❌ Semantic understanding completion
- ❌ Hukm production capability
- ❌ CERTIFIED rank without full evidence and zero residuals
- ❌ "Arabic proves the mind" (Arabic is revealing model, not proof)

---

## Allowed Claims

This repository MAY claim:

- ✅ General Cognitive Algebra foundation (5/13 layers implemented)
- ✅ Governed Arabic algebra (Dal → Binding → Wadh → Mutabaqah)
- ✅ Constitutional enforcement (no bare output, CPB bridges, rank discipline)
- ✅ Pre-semantic Dal algebra (D0-D7 with MufradProof)
- ✅ Semantic boundary guards (preventing premature HUKM)
- ✅ Arabic as first revealing model for General Cognitive Algebra
- ✅ Research implementation proving governed binding is computationally viable

---

## License

MIT

---

## Status Summary

**Constitutional Foundation**: ✅ **Solid and enforced**
**Arabic Algebra Foundation**: ✅ **Strong** (Dal → Wadh → Mutabaqah)
**General Cognitive Algebra**: ⏳ **5/13 layers** (foundation only)
**Governance**: ⚠️ **Needs hardening** (PR-F1/F2/F3)
**Semantic Completion**: ⏳ **Planned** (Ifādah/Murad/Hukm)
**Overall Completion**: **38%** (5 of 13 cognitive layers implemented)

**Next Milestone**: Foundation Hardening (PR-F1/F2/F3) before new layer implementation

---

For questions or contributions, see [CONTRIBUTING.md](CONTRIBUTING.md) (if exists) or open an issue.
