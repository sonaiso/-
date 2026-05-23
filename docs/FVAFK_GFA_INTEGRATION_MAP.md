# FVAFK-GFA Integration Roadmap

**Purpose**: Map existing GFA/dal_core components to FVAFK pipeline gaps

**Date**: 2026-05-23

**Status**: Week 1 - Gap Analysis Phase

---

## Executive Summary

**Strategic Decision**: Instead of building FVAFK Phases 4-6 from scratch, integrate existing 158 Python files (113 GFA + 45 dal_core) that implement mature governance, wadh, mutabaqah, and syntax theory.

**Key Insight**: The project has **already built** the foundational components. They just need to be bridged to FVAFK pipeline.

---

## Current State Audit

### ✅ What Exists (Mature, Tested, Ready)

#### 1. **GFA Governance Chain** (113 files, ~10% runtime)
**Location**: `src/gfa/`

**Components**:
- **Memory Geometry** (PR-G1): 30/30 tests ✅
  - `memory_trace.py`, `memory_storage.py`, `memory_gate.py`
  - `recall_process.py`, `memory_residual.py`
  - **Law**: Memory stores trace not content; recall ≠ original

- **Wadh Geometry + Gate** (PR-L5A/L5B): 37/37 tests ✅
  - `wadh_source.py`, `wadh_transmission_mode.py`, `wadh_scope.py`
  - `wadh_evidence.py`, `wadh_claim.py`, `mawdu_lah_structure.py`
  - `wadh_gate.py`, `wadh_gate_result.py`
  - **Law**: Reason alone cannot license Arabic Wadh (requires transmission)

- **Mutabaqah Gate** (PR-L6A): 29/29 tests ✅
  - `mutabaqah_gate.py`, `mutabaqah_candidate.py`, `mutabaqah_result.py`
  - **Law**: المطابقة = whole of placed-for only

- **Neutral Binding** (PR-N1): 19/19 tests ✅
  - `neutral_binding.py`
  - **Law**: Does NOT raise rank, does NOT certify

- **Cognitive Carrier** (Layer 0.5): 20/20 tests ✅
  - `cognitive_carrier.py`, `carrier_capacity.py`, `embodied_state.py`
  - **Law**: Carrier does NOT create meaning

**Total**: 135/135 tests passing ✅

#### 2. **dal_core (Dal Algebra)** (45 files)
**Location**: `src/dal_core/`

**Components**:
- **Domain Architecture** (D0-D7):
  - D0: Carrier
  - D1: Syllable Candidate
  - D2: Morpheme Candidate
  - D3: Mufrad (DMufrad, DLugha, DType)
  - D4: Murakkab (SentenceFrameCandidate)
  - D5: CaseSignMatrix
  - D6: OperatorTriggerPotential
  - D7: OperatorCandidate

- **Transition Contracts** (PR #22):
  - `DalTransitionContract`, `DalCandidateProtocol`
  - `DalEvidence`, `DalTrace`, `DalClaimScope`
  - **Law**: No direct cross-layer promotion

- **Morphology Contracts**:
  - `MufradProof`, `RootCandidate`, `WaznCandidate`
  - `BinaaJudgment`, `IshtiqaqJudgment`
  - `MabniRegistry` (frozen words)

- **Syntax Foundations**:
  - `PreSyntaxMufradVector`
  - `SentenceFrameCandidate` (Nominal/Verbal/Particle-Led/Fragment)
  - `FrameBuilder`, `CaseSignMatrix`
  - `OperatorTriggerPotential`, `NahwOperatorRegistry`
  - `OperatorCandidate`

**Total**: Contracts 1-9 complete (Phases 0/1) ✅

#### 3. **syntax_theory** (Graph-based syntax)
**Location**: `src/syntax_theory/`

**Components**:
- **Structures**:
  - `SyntacticInput`, `SyntacticGraph`
  - `Node`, `Edge`, `EdgeType`
  - `CaseMarking`, `MoodMarking`

- **Relations**:
  - ISN (إسناد), TADMN (تضمين), TAQYID (تقييد)
  - `RelationBuilder`, `RelationConstraints`

- **Generators**:
  - `CanonicalConstructor` (y₀ builder)
  - `CandidateGenerator` (G(x) generator)

- **Minimizers**:
  - Energy function E(x,y)
  - Multi-component minimization

**Status**: Definitions complete, needs integration ✅

#### 4. **maqam_theory** (Style gates)
**Location**: `src/maqam_theory/`

**Components**:
- **12 Gates** (verified):
  - Interrogative (Polar/Wh/Alternative)
  - Vocative, Imperative, Prohibitive
  - Exclamative, Declarative, Optative, Wish
  - Conditional, Oath

- **Gate Contract**:
  - `BaseGate`, `can_activate`, `compute_satisfaction`, `compute_cost`
  - Hard gates (∞) vs Soft gates (finite penalty)

**Status**: Gate pattern proven ✅

### 🔴 What's Missing (FVAFK Gaps)

#### 1. **FVAFK Phase 3 (C2b Morphology)** - Partial
**Location**: `src/fvafk/c2b/`

**Exists**:
- ✅ `root_resolver/` (root extraction)
- ✅ `word_classifier.py` (noun/verb/particle detection)
- ✅ `syllabifier.py`
- ✅ `mabni_rules.py`

**Missing**:
- ❌ Word boundary detection (tokenization)
- ❌ Affix identification (prefixes/suffixes)
- ❌ Complete morphological feature extraction
- ❌ **Bridge to dal_core D3 (DMufrad)**

#### 2. **FVAFK Phase 4 (Syntax)** - Completely Missing
**Location**: `src/fvafk/syntax/` (exists but incomplete)

**Partial exists**:
- ⚠️ `src/fvafk/c2b/syntax/` (i3rab parser, partial)

**Missing**:
- ❌ Full syntactic parser (VSO, ISNADI, TADMINI, TAQYIDI)
- ❌ **Bridge to syntax_theory relations (ISN/TADMN/TAQYID)**
- ❌ **Bridge to dal_core D4 (SentenceFrameCandidate)**
- ❌ Graph construction from FVAFK tokens

#### 3. **FVAFK Phase 5 (Constraints)** - Completely Missing
**Location**: None (needs creation)

**Missing**:
- ❌ 6 grammar constraints
- ❌ **Bridge to maqam_theory gates**
- ❌ Energy minimization integration
- ❌ Constraint violation detection

#### 4. **FVAFK Phase 6 (Integration)** - Incomplete
**Location**: `src/fvafk/cli/`

**Exists**:
- ✅ CLI skeleton (`main.py`)
- ✅ C1 → C2a pipeline

**Missing**:
- ❌ C2b → Syntax → Constraints chain
- ❌ End-to-end tests with metrics
- ❌ Golden dataset validation (PR #29)

---

## Integration Strategy

### Principle: **Adapter Pattern with Governance Preservation**

**Core Idea**: Create thin adapters that translate FVAFK outputs to dal_core/GFA inputs, preserving governance laws.

### Phase 1: Bridge Interfaces (Week 2)

#### Adapter 1: **FVAFK C2b → dal_core D3 (Mufrad)**

**Input**: FVAFK `WordForm` from C2b
**Output**: dal_core `DMufrad` + `MufradProof`

**Adapter Design**:
```python
# src/fvafk/adapters/c2b_to_d3_adapter.py

from dataclasses import dataclass
from typing import Optional
from fvafk.c2b.word_form import WordForm
from dal_core import DMufrad, MufradProof, DalEvidence, DalTrace

@dataclass(frozen=True)
class C2bToD3Adapter:
    """
    Bridge FVAFK C2b morphology to dal_core D3 Mufrad.
    
    Preserves:
    - Trace reversibility (DalTrace)
    - Evidence requirement (DalEvidence)
    - No meaning field (Theorem 5)
    - No direct promotion (layer contracts)
    """
    
    def adapt_word_form(self, word_form: WordForm) -> tuple[Optional[DMufrad], DalEvidence, DalTrace]:
        """
        Convert FVAFK WordForm to dal_core DMufrad.
        
        Returns:
            (mufrad, evidence, trace) or (None, ...) if inadmissible
        """
        # Step 1: Extract evidence from FVAFK
        evidence = self._extract_evidence(word_form)
        
        # Step 2: Build trace
        trace = self._build_trace(word_form)
        
        # Step 3: Construct DMufrad (respecting contracts)
        mufrad = self._construct_dmufrad(word_form, evidence, trace)
        
        return (mufrad, evidence, trace)
    
    def _extract_evidence(self, wf: WordForm) -> DalEvidence:
        """Extract claim-scoped evidence (span required)"""
        # Map FVAFK root/wazn to DalEvidence
        ...
    
    def _build_trace(self, wf: WordForm) -> DalTrace:
        """Build reversible trace (is_reversible() = True)"""
        # Ensure trace can reverse back to FVAFK atoms
        ...
    
    def _construct_dmufrad(self, wf, evidence, trace) -> Optional[DMufrad]:
        """Construct DMufrad respecting Theorem 5 (no meaning field)"""
        # Use dal_core.build_d_form, prove_lugha, infer_type, close_mufrad
        ...
```

**Tests Required** (8 tests):
1. ✅ Valid word → DMufrad with trace
2. ✅ Evidence contains span
3. ✅ Trace is reversible
4. ✅ No meaning field in DMufrad
5. ✅ Invalid word → None (governed failure)
6. ✅ Mabni word → MabniRegistry lookup
7. ✅ Mushtaq word → IshtiqaqJudgment
8. ✅ Round-trip: DMufrad → trace → FVAFK atoms

#### Adapter 2: **FVAFK Tokens → syntax_theory SyntacticInput**

**Input**: List of FVAFK `WordForm` + sentence text
**Output**: syntax_theory `SyntacticInput`

**Adapter Design**:
```python
# src/fvafk/adapters/fvafk_to_syntax_input_adapter.py

from dataclasses import dataclass
from typing import List
from fvafk.c2b.word_form import WordForm
from syntax_theory.structures import SyntacticInput, LexicalAtom

@dataclass(frozen=True)
class FvafkToSyntaxInputAdapter:
    """
    Convert FVAFK token stream to syntax_theory SyntacticInput.
    
    Preserves:
    - Lexical type classification
    - Verb valency extraction
    - Intent constraints (interrogative/imperative/...)
    """
    
    def adapt_tokens(self, tokens: List[WordForm], intent: str) -> SyntacticInput:
        """Build SyntacticInput for syntax_theory graph construction"""
        atoms = [self._to_lexical_atom(t) for t in tokens]
        constraints = self._extract_intent_constraints(intent)
        return SyntacticInput(atoms=atoms, constraints=constraints)
    
    def _to_lexical_atom(self, token: WordForm) -> LexicalAtom:
        """Map FVAFK token to syntax_theory LexicalAtom"""
        ...
    
    def _extract_intent_constraints(self, intent: str) -> List:
        """Map intent to IntentConstraint (interrogative/imperative/...)"""
        ...
```

**Tests Required** (6 tests):
1. ✅ Nominal sentence → SyntacticInput
2. ✅ Verbal sentence → SyntacticInput with verb valency
3. ✅ Interrogative intent → IntentConstraint
4. ✅ Imperative intent → IntentConstraint
5. ✅ Mixed sentence → correct atom classification
6. ✅ Empty sentence → governed failure

#### Adapter 3: **SyntacticGraph → FVAFK Syntax Output**

**Input**: syntax_theory `SyntacticGraph` (y⋆ from argmin)
**Output**: FVAFK syntax dict (ISN/TADMN/TAQYID relations)

**Adapter Design**:
```python
# src/fvafk/adapters/syntax_graph_to_fvafk_adapter.py

from dataclasses import dataclass
from typing import Dict, List
from syntax_theory.structures import SyntacticGraph, EdgeType

@dataclass(frozen=True)
class SyntaxGraphToFvafkAdapter:
    """
    Convert syntax_theory graph back to FVAFK output format.
    
    Extracts:
    - ISN relations (إسناد)
    - TADMN relations (تضمين)
    - TAQYID relations (تقييد)
    - Case markings (nominative/accusative/genitive)
    - Mood markings (indicative/subjunctive/jussive)
    """
    
    def extract_relations(self, graph: SyntacticGraph) -> Dict[str, List]:
        """Extract all relations from graph"""
        return {
            "isn": self._extract_isn(graph),
            "tadmn": self._extract_tadmn(graph),
            "taqyid": self._extract_taqyid(graph),
            "case_markings": self._extract_case(graph),
            "mood_markings": self._extract_mood(graph),
        }
    
    def _extract_isn(self, graph) -> List[Dict]:
        """Extract ISN (predication) relations"""
        ...
    
    def _extract_tadmn(self, graph) -> List[Dict]:
        """Extract TADMN (transitive/embedding) relations"""
        ...
    
    def _extract_taqyid(self, graph) -> List[Dict]:
        """Extract TAQYID (modification) relations"""
        ...
```

**Tests Required** (6 tests):
1. ✅ ISN relation extraction
2. ✅ TADMN relation extraction
3. ✅ TAQYID relation extraction
4. ✅ Case marking extraction
5. ✅ Mood marking extraction
6. ✅ Round-trip: FVAFK → graph → FVAFK (idempotent)

### Phase 2: Syntax Integration (Weeks 3-4)

#### Component 1: **FVAFK Syntax Parser (using syntax_theory)**

**Location**: `src/fvafk/syntax/parser.py`

**Design**:
```python
# src/fvafk/syntax/parser.py

from dataclasses import dataclass
from typing import List, Dict, Optional
from fvafk.c2b.word_form import WordForm
from fvafk.adapters import (
    C2bToD3Adapter,
    FvafkToSyntaxInputAdapter,
    SyntaxGraphToFvafkAdapter,
)
from syntax_theory.structures import SyntacticInput, SyntacticGraph
from syntax_theory.generators import CanonicalConstructor, CandidateGenerator
from syntax_theory.minimizers import EnergyMinimizer

@dataclass
class FvafkSyntaxParser:
    """
    FVAFK syntax parser using syntax_theory backend.
    
    Pipeline:
        FVAFK tokens → SyntacticInput → G(x) → argmin E → SyntacticGraph → FVAFK output
    """
    
    c2b_adapter: C2bToD3Adapter
    syntax_input_adapter: FvafkToSyntaxInputAdapter
    syntax_output_adapter: SyntaxGraphToFvafkAdapter
    canonical_constructor: CanonicalConstructor
    candidate_generator: CandidateGenerator
    energy_minimizer: EnergyMinimizer
    
    def parse(self, tokens: List[WordForm], intent: str = "declarative") -> Dict:
        """
        Parse FVAFK tokens to syntax relations.
        
        Args:
            tokens: FVAFK WordForm list from C2b
            intent: Sentence intent (declarative/interrogative/imperative/...)
        
        Returns:
            Dict with keys: isn, tadmn, taqyid, case_markings, mood_markings
        """
        # Step 1: Convert to SyntacticInput
        x = self.syntax_input_adapter.adapt_tokens(tokens, intent)
        
        # Step 2: Build canonical structure y₀
        y0 = self.canonical_constructor.construct(x)
        
        # Step 3: Generate candidates G(x)
        candidates = self.candidate_generator.generate(x, y0)
        
        # Step 4: Minimize energy E(x,y)
        y_star = self.energy_minimizer.minimize(x, candidates)
        
        # Step 5: Convert back to FVAFK format
        result = self.syntax_output_adapter.extract_relations(y_star)
        
        return result
```

**Tests Required** (12 tests):
1-3. ✅ Nominal sentences (ISN dominant)
4-6. ✅ Verbal sentences (TADMN/TAQYID)
7-9. ✅ Complex sentences (mixed relations)
10-12. ✅ Edge cases (fragments, unresolved)

#### Component 2: **CLI Integration**

**Location**: `src/fvafk/cli/main.py`

**Updated Pipeline**:
```python
# src/fvafk/cli/main.py (updated)

def analyze_text(text: str, include_syntax: bool = True) -> Dict:
    """
    Full FVAFK pipeline: C1 → C2a → C2b → [Syntax] → [Constraints]
    """
    # Phase 1: Encoding (C1)
    c1_result = encode_text(text)
    
    # Phase 2: Phonology (C2a)
    c2a_result = apply_phonology_gates(c1_result)
    
    # Phase 3: Morphology (C2b)
    tokens = tokenize_and_analyze_morphology(c2a_result)
    
    # Phase 4: Syntax (NEW)
    syntax_result = None
    if include_syntax:
        parser = FvafkSyntaxParser(...)
        syntax_result = parser.parse(tokens, intent="declarative")
    
    return {
        "encoding": c1_result,
        "phonology": c2a_result,
        "morphology": tokens,
        "syntax": syntax_result,
    }
```

**Tests Required** (6 tests):
1. ✅ End-to-end with syntax
2. ✅ End-to-end without syntax
3. ✅ Syntax errors handled gracefully
4. ✅ Metrics extraction (UAS/LAS)
5. ✅ Performance (< 100ms per sentence)
6. ✅ Memory (< 50MB per 1000 sentences)

### Phase 3: Constraints + Golden Dataset (Weeks 5-6)

#### Component 1: **Maqam Gate Integration**

**Location**: `src/fvafk/constraints/maqam_constraints.py`

**Design**:
```python
# src/fvafk/constraints/maqam_constraints.py

from maqam_theory.gates import (
    InterrogativePolarGate,
    InterrogativeWhGate,
    VocativeGate,
    ImperativeGate,
    ProhibitiveGate,
    DeclarativeGate,
)

class MaqamConstraintValidator:
    """
    Validate FVAFK syntax output using maqam_theory gates.
    
    Enforces:
    - Interrogative structure correctness
    - Vocative placement rules
    - Imperative/prohibitive constraints
    - Declarative default structure
    """
    
    def validate(self, syntax_graph, intent):
        """
        Apply maqam gates based on intent.
        
        Returns:
            (is_valid, violations, energy_cost)
        """
        gate = self._select_gate(intent)
        
        if not gate.can_activate(syntax_graph):
            return (False, ["Gate cannot activate"], float('inf'))
        
        satisfaction = gate.compute_satisfaction(syntax_graph, None)
        cost = gate.compute_cost(syntax_graph, None, activated=True)
        
        violations = [] if satisfaction > 0.8 else ["Low satisfaction"]
        
        return (satisfaction > 0.8, violations, cost)
```

**Tests Required** (12 tests):
1-2. ✅ Interrogative polar gate
3-4. ✅ Interrogative wh gate
5-6. ✅ Vocative gate
7-8. ✅ Imperative gate
9-10. ✅ Prohibitive gate
11-12. ✅ Declarative gate

#### Component 2: **Golden Dataset Validation**

**Location**: `tests/fvafk/test_golden_dataset.py`

**Dataset**: 100 annotated sentences

**Metrics**:
- **F1 morphology**: Root detection accuracy
- **UAS**: Unlabeled attachment score (syntax)
- **LAS**: Labeled attachment score (syntax + relations)
- **Constraint violations**: 0 for valid sentences

**Tests Required** (8 tests):
1. ✅ Load golden dataset (100 sentences)
2. ✅ Morphology F1 ≥ 0.80
3. ✅ UAS ≥ 0.75
4. ✅ LAS ≥ 0.70
5. ✅ 0 constraint violations on valid sentences
6. ✅ Detect violations on invalid sentences
7. ✅ Performance benchmark
8. ✅ Memory benchmark

---

## Deliverables

### Week 1-2: Bridge Interfaces
- ✅ FVAFK_GFA_INTEGRATION_MAP.md (this document)
- ✅ 3 adapter files (20+ tests total)
- ✅ Integration tests passing

### Week 3-4: Syntax Integration
- ✅ FvafkSyntaxParser (12+ tests)
- ✅ CLI integration (6+ tests)
- ✅ End-to-end pipeline working

### Week 5-6: Constraints + Validation
- ✅ MaqamConstraintValidator (12+ tests)
- ✅ Golden dataset (100 sentences)
- ✅ Metrics: F1 ≥ 0.80, UAS ≥ 0.75, LAS ≥ 0.70
- ✅ PR #29 (Golden Dataset Phase 2) complete

---

## Success Criteria

### Technical
1. ✅ All adapters preserve governance laws (no rank inflation, trace preserved, evidence required)
2. ✅ 50+ integration tests passing
3. ✅ No code duplication between FVAFK and GFA/dal_core
4. ✅ Syntax parser uses syntax_theory backend
5. ✅ Maqam gates validate syntax structures

### Performance
1. ✅ < 100ms per sentence (end-to-end)
2. ✅ < 50MB memory per 1000 sentences
3. ✅ F1 morphology ≥ 0.80
4. ✅ UAS ≥ 0.75, LAS ≥ 0.70

### Documentation
1. ✅ Integration map (this document)
2. ✅ Adapter API documentation
3. ✅ Golden dataset description
4. ✅ PR #29 summary

---

## Risk Mitigation

### Risk 1: Adapter complexity explodes
**Mitigation**: Keep adapters thin (< 200 lines each). Pure translation, no logic.

### Risk 2: Performance degradation
**Mitigation**: Profile early. Adapter overhead target < 10ms.

### Risk 3: Governance violations in adapters
**Mitigation**: 
- Test: `test_adapter_preserves_trace`
- Test: `test_adapter_requires_evidence`
- Test: `test_adapter_no_meaning_field`

### Risk 4: Golden dataset too ambitious
**Mitigation**: Start with 20 sentences, expand to 100 incrementally.

---

## Next Steps

### Immediate (Week 1, Day 1-2)
1. ✅ Complete this gap analysis
2. → Create `src/fvafk/adapters/` directory
3. → Implement `C2bToD3Adapter` (first 8 tests)
4. → Validate adapter preserves governance laws

### Week 1, Day 3-5
1. → Implement `FvafkToSyntaxInputAdapter` (6 tests)
2. → Implement `SyntaxGraphToFvafkAdapter` (6 tests)
3. → Integration smoke test: FVAFK token → SyntacticGraph → FVAFK output

### Week 2
1. → Refine adapters based on test failures
2. → Performance profiling
3. → Documentation

---

## Appendix: File Counts (Evidence)

```bash
# GFA
find src/gfa -name "*.py" | wc -l
# 113 files

# dal_core
find src/dal_core -name "*.py" | wc -l
# 45 files

# FVAFK
find src/fvafk -name "*.py" | wc -l
# 149 files

# Total existing foundation
113 + 45 = 158 files (mature, tested)

# FVAFK gaps (rough estimate)
# Phase 4 (Syntax): ~8 files needed
# Phase 5 (Constraints): ~5 files needed
# Adapters: ~3 files needed
# Total new code: ~16 files (10% of existing foundation)
```

**Conclusion**: 90% of the work is done. We just need 10% adapters + integration.

---

**Document Version**: 1.0  
**Author**: Integration Planning Agent  
**Review Status**: Pending user approval
