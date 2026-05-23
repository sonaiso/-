# PR-L3 Phase 2: DalCandidateBuilder Implementation Guide
# دليل تنفيذ المرحلة الثانية: بناء الدال

**Target**: Week of 2026-05-30
**Priority**: Critical - Unblocks complete PR-L3

---

## Objective | الهدف

Implement `DalCandidateBuilder` to automatically construct fully-licensed `DalCandidate` from raw Arabic text via C1→C2a→C2b pipeline.

---

## Architecture | المعمارية

```
Raw Signal (نص عربي)
    ↓
DalCandidateBuilder.build()
    │
    ├─→ Phase 1: C1 Encoding
    │   └─→ extract_phonic_carriers()
    │       └─→ PhonicCarrier[]
    │
    ├─→ Phase 2: C2a Phonology
    │   ├─→ apply_haraka_operations()
    │   │   └─→ HarakaOperation[] (10 gates)
    │   └─→ license_syllables()
    │       └─→ SyllableLicense[] (CV/CVC/CVV)
    │
    ├─→ Phase 3: C2b Morphology
    │   ├─→ detect_word_boundaries()
    │   │   └─→ WordBoundaryInfo
    │   ├─→ separate_clitics()
    │   │   └─→ CliticAnalysis
    │   ├─→ generate_formula_candidates()
    │   │   └─→ FormulaCandidate[]
    │   ├─→ classify_path_type()
    │   │   └─→ PathType
    │   ├─→ determine_pattern_status()
    │   │   └─→ PatternStatus
    │   └─→ resolve_terminal_state()
    │       └─→ TerminalState
    │
    ├─→ Phase 4: C2b Syntax Readiness
    │   ├─→ assess_syntactic_readiness()
    │   │   └─→ SyntacticReadiness
    │   ├─→ analyze_sentence_shape()
    │   │   └─→ SentenceShape?
    │   └─→ project_role_candidates()
    │       └─→ RoleProjection[]
    │
    └─→ Phase 5: Governance
        ├─→ compute_rank_from_evidence()
        ├─→ collect_residuals()
        └─→ generate_trace()
            ↓
        DalCandidate (13 fields)
```

---

## Integration Points | نقاط التكامل

### C1 Encoding

**Existing**: `src/fvafk/c1/`

```python
# Expected interface
from fvafk.c1 import FormEncoder

def extract_phonic_carriers(raw_signal: str) -> Tuple[PhonicCarrier, ...]:
    """Extract phonic carriers from raw text."""
    encoder = FormEncoder()
    encoded = encoder.encode(raw_signal)

    carriers = []
    for i, char in enumerate(encoded.graphemes):
        carrier = PhonicCarrier(
            form=char,
            phoneme=encoded.phonemes[i] if encoded.phonemes else None,
            position=i,
            features=frozenset(encoded.features[i])
        )
        carriers.append(carrier)

    return tuple(carriers)
```

### C2a Phonology Gates

**Existing**: `src/fvafk/c2a/gates/`

```python
# Expected gates
from fvafk.c2a.gates import (
    GateSukun,
    GateShadda,
    GateTanwin,
    GateHamza,
    GateWaqf,
    GateIdgham,
    GateMadd,
    # ... others
)

def apply_haraka_operations(
    carriers: Tuple[PhonicCarrier, ...]
) -> Tuple[HarakaOperation, ...]:
    """Apply all C2a phonology gates."""
    operations = []

    # Apply each gate in sequence
    gates = [
        GateSukun(),
        GateShadda(),
        GateTanwin(),
        # ... 7 more gates
    ]

    for gate in gates:
        result = gate.apply(carriers)
        if result.status == GateStatus.REPAIR:
            op = HarakaOperation(
                operation_type=gate.operation_type,
                position=result.position,
                input_form=result.input_form,
                output_form=result.output_form,
                gate_name=gate.__class__.__name__
            )
            operations.append(op)

    return tuple(operations)
```

### C2b Morphology

**Existing**: `src/fvafk/c2b/`

```python
# Expected analyzers
from fvafk.c2b import (
    WordBoundaryDetector,
    CliticAnalyzer,
    PatternMatcher,
    PathClassifier,
)

def detect_word_boundaries(
    syllables: Tuple[SyllableLicense, ...]
) -> WordBoundaryInfo:
    """Detect word boundaries."""
    detector = WordBoundaryDetector()
    result = detector.detect(syllables)

    return WordBoundaryInfo(
        start_position=result.start,
        end_position=result.end,
        boundary_markers=frozenset(result.markers),
        confidence=result.confidence
    )

def separate_clitics(
    boundaries: WordBoundaryInfo
) -> CliticAnalysis:
    """Separate clitics from stem."""
    analyzer = CliticAnalyzer()
    result = analyzer.analyze(boundaries)

    return CliticAnalysis(
        stem=result.stem,
        prefixes=tuple(result.prefixes),
        suffixes=tuple(result.suffixes),
        has_clitics=len(result.prefixes) + len(result.suffixes) > 0
    )
```

---

## Implementation Steps | خطوات التنفيذ

### Step 1: Create Builder Skeleton

**File**: `src/gfa/methods/lafzi_dal/dal_candidate_builder.py`

```python
"""
DalCandidateBuilder - بناء الدال المرخّص

Constructs fully-licensed DalCandidate from raw Arabic text.
"""

from typing import Tuple, FrozenSet
from .dal_candidate import DalCandidate
from .dal_structures import *


class DalCandidateBuilder:
    """
    بناء الدال - DalCandidate Builder

    Orchestrates C1→C2a→C2b pipeline to construct
    complete DalCandidate from raw signal.
    """

    def __init__(self):
        """Initialize builder with pipeline components."""
        # C1
        self.form_encoder = None  # To be wired

        # C2a
        self.phonology_gates = []  # To be wired
        self.syllabifier = None  # To be wired

        # C2b
        self.boundary_detector = None  # To be wired
        self.clitic_analyzer = None  # To be wired
        self.pattern_matcher = None  # To be wired
        self.path_classifier = None  # To be wired

    def build(self, raw_signal: str) -> DalCandidate:
        """
        Build complete DalCandidate from raw Arabic text.

        Args:
            raw_signal: Raw Arabic text (e.g., "كَتَبَ")

        Returns:
            DalCandidate with all 13 mandatory fields

        Raises:
            ValueError: If any pipeline stage fails critically
        """
        # Phase 1: C1 Encoding
        phonic_carriers = self._extract_phonic_carriers(raw_signal)

        # Phase 2: C2a Phonology
        haraka_ops = self._apply_haraka_operations(phonic_carriers)
        syllables = self._license_syllables(phonic_carriers, haraka_ops)

        # Phase 3: C2b Morphology
        boundaries = self._detect_word_boundaries(syllables)
        clitics = self._separate_clitics(boundaries)
        formulas = self._generate_formula_candidates(clitics)
        path = self._classify_path_type(formulas)
        pattern = self._determine_pattern_status(formulas)
        terminal = self._resolve_terminal_state(formulas)

        # Phase 4: C2b Syntax
        readiness = self._assess_syntactic_readiness(terminal)
        shape = self._analyze_sentence_shape(readiness)
        roles = self._project_role_candidates(shape)

        # Phase 5: Governance
        trace_id = self._generate_trace_id()
        residuals = self._collect_residuals()

        # Construct DalCandidate
        return DalCandidate(
            phonic_carriers=phonic_carriers,
            haraka_operations=haraka_ops,
            syllable_licenses=syllables,
            word_boundaries=boundaries,
            clitics=clitics,
            formula_candidates=formulas,
            path_type=path,
            pattern_status=pattern,
            terminal_state=terminal,
            syntactic_readiness=readiness,
            sentence_shape=shape,
            role_projection_candidates=roles,
            trace_id=trace_id,
            residuals=residuals,
            source_layer="PURE_DAL"
        )

    # === Phase 1: C1 Encoding ===

    def _extract_phonic_carriers(
        self, raw_signal: str
    ) -> Tuple[PhonicCarrier, ...]:
        """Extract phonic carriers from raw text."""
        raise NotImplementedError("Wire to C1")

    # === Phase 2: C2a Phonology ===

    def _apply_haraka_operations(
        self, carriers: Tuple[PhonicCarrier, ...]
    ) -> Tuple[HarakaOperation, ...]:
        """Apply C2a phonology gates."""
        raise NotImplementedError("Wire to C2a gates")

    def _license_syllables(
        self,
        carriers: Tuple[PhonicCarrier, ...],
        operations: Tuple[HarakaOperation, ...]
    ) -> Tuple[SyllableLicense, ...]:
        """License syllable structures."""
        raise NotImplementedError("Wire to C2a syllabifier")

    # === Phase 3: C2b Morphology ===

    def _detect_word_boundaries(
        self, syllables: Tuple[SyllableLicense, ...]
    ) -> WordBoundaryInfo:
        """Detect word boundaries."""
        raise NotImplementedError("Wire to C2b boundary detector")

    # ... (similar for other C2b methods)

    # === Phase 5: Governance ===

    def _generate_trace_id(self) -> str:
        """Generate unique trace ID."""
        import uuid
        return f"dal_{uuid.uuid4().hex[:8]}"

    def _collect_residuals(self) -> FrozenSet[str]:
        """Collect residuals from all stages."""
        # To be implemented: aggregate from all pipeline stages
        return frozenset()
```

### Step 2: Wire C1 Integration

**Update**: `_extract_phonic_carriers()` method

```python
def _extract_phonic_carriers(
    self, raw_signal: str
) -> Tuple[PhonicCarrier, ...]:
    """Extract phonic carriers from C1 encoding."""
    # Import C1 components
    from fvafk.c1.form_encoder import FormEncoder

    encoder = FormEncoder()
    result = encoder.encode(raw_signal)

    carriers = []
    for i, grapheme in enumerate(result.graphemes):
        carrier = PhonicCarrier(
            form=grapheme,
            phoneme=result.phonemes[i] if result.phonemes else None,
            position=i,
            features=frozenset(result.features.get(i, []))
        )
        carriers.append(carrier)

    return tuple(carriers)
```

### Step 3: Wire C2a Integration

**Update**: `_apply_haraka_operations()` and `_license_syllables()`

(See Integration Points section above)

### Step 4: Wire C2b Integration

**Update**: All C2b methods

(See Integration Points section above)

### Step 5: Add Builder Tests

**File**: `tests/gfa/methods/test_dal_candidate_builder.py`

```python
"""Tests for DalCandidateBuilder."""

import pytest
from gfa.methods.lafzi_dal import DalCandidateBuilder


class TestDalCandidateBuilder:
    """Test DalCandidateBuilder integration."""

    def test_build_simple_verb(self):
        """Test building DalCandidate from simple verb."""
        builder = DalCandidateBuilder()
        candidate = builder.build("كَتَبَ")

        assert candidate.is_valid
        assert candidate.path_type == PathType.VERB
        assert len(candidate.phonic_carriers) == 3
        assert candidate.get_stem() == "كتب"

    def test_build_with_clitics(self):
        """Test building with clitics."""
        builder = DalCandidateBuilder()
        candidate = builder.build("وَالْكِتَابُ")

        assert candidate.is_valid
        assert candidate.clitics.has_clitics
        assert len(candidate.clitics.prefixes) > 0

    # ... more tests
```

---

## Success Criteria | معايير النجاح

### Phase 2 Complete When:

1. ✅ DalCandidateBuilder skeleton created
2. ✅ C1 integration working (phonic_carriers)
3. ✅ C2a integration working (haraka_operations, syllable_licenses)
4. ✅ C2b integration working (all 9 remaining fields)
5. ✅ 10+ builder tests passing
6. ✅ End-to-end test: "كَتَبَ" → valid DalCandidate

### Performance Target:

- ⏱️ < 10ms per word (measured with pytest-benchmark)

---

## Dependencies | الاعتماديات

**Required Existing Components**:

- `src/fvafk/c1/` (encoding)
- `src/fvafk/c2a/gates/` (phonology)
- `src/fvafk/c2b/` (morphology)

**If Missing**: Create minimal stubs for testing

---

## Timeline | الجدول الزمني

**Week of 2026-05-30**:

- Day 1-2: Builder skeleton + C1 wire
- Day 3-4: C2a wire (gates + syllabifier)
- Day 5-6: C2b wire (boundaries, clitics, patterns)
- Day 7: Testing + benchmarks

**Deliverable**: Functional DalCandidateBuilder with 10+ tests

---

## Next After Phase 2

**Phase 3**: Performance + Coverage
- Benchmark < 10ms
- Coverage ≥90%
- 40+ total tests

**Phase 4**: Documentation + Review
- Usage examples
- Architecture review
- PR merge

---

**Status**: Ready to Start | جاهز للبدء
**Owner**: Implementation Agent | الوكيل المنفذ
**Priority**: Critical | حرج

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
