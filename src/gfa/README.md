# General Foundational Algebra (GFA)

## Overview

General Foundational Algebra (GFA) is the implementation of the foundational components required for General Algebra, starting from the minimal sufficient unit (FirstPriorUnit) that serves as the foundation for all knowledge systems.

## Core Principle

**CPB is not an axiom. CPB is a learned theorem: CPB = μΦ**

The system transforms:
```
ExistentialTrace
→ PrimitiveBinding (may fail)
→ Repetition / Contrast
→ Classification
→ PriorGeometry
→ Learning (Φ function)
→ BindingConditions
→ CPB (as stable result: μΦ)
→ LayerAlgebraGenerator
```

## Architecture

### Current Implementation: ProtoPrior Kernel ✅

**Package**: `src/gfa/proto_prior/`

Implements **FirstPriorUnit** - the minimal sufficient unit for First Prior Geometry.

**FirstPriorUnit is NOT**:
- A rule
- A concept/meaning
- A word
- A law
- A judgment

**FirstPriorUnit IS**:
- A distinguished existential trace
- Anchored in time, place, and reference (MANDATORY)
- Bounded and retainable
- Comparable and primitively bindable
- Sufficient for entering PriorGeometry
- Insufficient for producing rules/meanings/judgments

**14 Mandatory Fields**:
1. `entity_or_effect` - What exists
2. `existence_type` - Mode of existence (physical, conceptual, linguistic, etc.)
3. `domain` - Realm/field
4. `distinction` - How distinguished from background
5. `boundary` - Extent/limits
6. `time_anchor` - Temporal anchoring
7. `place_anchor` - Spatial/domain anchoring
8. `reference_anchor` - What/who it refers to
9. `channel` - Access pathway
10. `retention_state` - Retention capability
11. `comparability_state` - Comparison capability
12. `primitive_bindability` - Binding capability
13. `residuals` - Unresolved aspects
14. `rank` - Epistemic status

Plus auto-generated: `trace_id` (unique UUID)

### Layer 1: AttentionGeometry ✅

**Package**: `src/gfa/attention/`

**Core Principle**: Attention selects traces for processing; attention does NOT certify, does NOT raise rank.

**Key Components**:
- `AttentionEvent` - Single attention operation over traces
- `AttentionGate` - Selection filter applying criteria
- `AttentionPolicy` - Strategy for selecting traces
- `AttendedTrace` - Result of attention selection
- `AttentionResidual` - Classification of ignored traces

**Critical Laws**:
- No attention without CognitiveCarrier
- Attention requires attention_capacity
- Attention selects, but does NOT certify
- Attention changes processing priority, NOT epistemic rank
- Attention preserves original trace_id
- Ignored trace becomes residual (NOT deleted)
- Attention does NOT store memory
- Attention does NOT compare traces
- Attention does NOT bind traces
- Attention does NOT learn patterns
- Attention does NOT create CPB

### Future Components (Not Yet Implemented)

- `memory/` - Memory storage and retrieval (NOT attention)
- `comparison/` - Trace comparison and contrast
- `identity_difference/` - Identity and difference operations
- `binding_core/` - Core binding mechanisms
- `primitive_binding/` - Experimental binding that may fail
- `prior_geometry/` - Stabilized trace memory (not rule database)
- `learning/` - Binding condition extraction (Φ function)
- `cpb/` - Stable binding policy extraction (μΦ solver)
- `algebra/` - Layer algebra generation from specifications

## Usage

```python
from gfa.proto_prior import (
    FirstPriorUnit,
    ExistenceType,
    Domain,
    Channel,
    TimeAnchor,
    PlaceAnchor,
    ReferenceAnchor,
    Distinction,
    Boundary,
    RetentionState,
    ComparabilityState,
    PrimitiveBindability,
    Rank,
)
from gfa.proto_prior.retention import RetentionLevel
from gfa.proto_prior.comparability import ComparabilityType
from gfa.proto_prior.primitive_bindability import BindabilityLevel
from datetime import datetime

# Example: Physical observation
unit = FirstPriorUnit(
    entity_or_effect="ball falling",
    existence_type=ExistenceType.PHYSICAL,
    domain=Domain(name="3D space"),
    distinction=Distinction(
        distinguishing_features={"red color", "spherical shape", "motion"}
    ),
    boundary=Boundary(spatial_boundary="0.1m radius sphere"),
    time_anchor=TimeAnchor(timestamp=datetime.now()),
    place_anchor=PlaceAnchor(locality_label="lab_room_A"),
    reference_anchor=ReferenceAnchor(entity_id="ball_001"),
    channel=Channel(name="visual_observation"),
    retention_state=RetentionState(retention_level=RetentionLevel.STABLE),
    comparability_state=ComparabilityState(
        supported_comparisons={ComparabilityType.METRIC}
    ),
    primitive_bindability=PrimitiveBindability(
        bindability_level=BindabilityLevel.GENERAL
    ),
    rank=Rank.OBSERVED
)

# Verify constitutional laws
assert unit.can_produce_rule() is False  # ✓
assert unit.can_produce_meaning() is False  # ✓
assert unit.can_issue_judgment() is False  # ✓
assert unit.can_certify() is False  # ✓

# Example: Attention over traces
from gfa.attention import (
    AttentionEvent,
    AttentionType,
    AttentionGate,
    AttendedTrace,
    AttentionPriority,
)
from uuid import uuid4

carrier_id = uuid4()
trace_ids = {uuid4(), uuid4(), uuid4()}

# Select subset of traces for processing
attention_event = AttentionEvent(
    carrier_id=carrier_id,
    attention_type=AttentionType.SELECTIVE,
    input_trace_ids=trace_ids,
    selected_trace_ids={list(trace_ids)[0], list(trace_ids)[1]},
    ignored_trace_ids={list(trace_ids)[2]},
    attention_capacity_used=0.4,
)

# Verify attention laws
assert not attention_event.can_certify()  # ✓
assert not attention_event.can_raise_rank()  # ✓
assert not attention_event.can_create_memory()  # ✓
assert not attention_event.can_compare_traces()  # ✓
assert not attention_event.can_bind()  # ✓
assert not attention_event.can_learn()  # ✓
```

## Constitutional Laws

### Mandatory Field Laws
1. No FirstPriorUnit without existence
2. No FirstPriorUnit without distinction
3. No FirstPriorUnit without boundary
4. No FirstPriorUnit without time anchor
5. No FirstPriorUnit without place anchor
6. No FirstPriorUnit without reference anchor
7. No FirstPriorUnit without retention
8. No FirstPriorUnit without comparability
9. No FirstPriorUnit without primitive bindability

### Prohibition Laws
1. FirstPriorUnit CANNOT produce rule
2. FirstPriorUnit CANNOT produce meaning
3. FirstPriorUnit CANNOT issue judgment
4. FirstPriorUnit CANNOT certify

### Existence Type Constraints
1. Hypothetical existence CANNOT be CERTIFIED
2. Linguistic/textual CANNOT imply physical without ExistenceBridge
3. Existence type promotion requires explicit bridge
4. Rank promotion requires evidence
5. CERTIFIED rank requires full audit

### Preservation Laws
1. Residuals must be preserved
2. Trace ID must be stable and unique

## Testing

```bash
# Run tests
python -m pytest tests/test_gfa_proto_prior_kernel.py -v

# Check coverage
python -m coverage run -m pytest tests/test_gfa_proto_prior_kernel.py
python -m coverage report --include="src/gfa/*"
```

**Current Status**: 146/146 tests passing (all GFA layers)

## What This Package Does NOT Do

Per constitutional specification:
- ❌ Does NOT implement Memory (next in PR-A3)
- ❌ Does NOT implement Comparison (future PR-A4)
- ❌ Does NOT implement IdentityDifference (future)
- ❌ Does NOT implement BindingCore (future)
- ❌ Does NOT implement PrimitiveBinding (future)
- ❌ Does NOT implement Learning (Φ function, future)
- ❌ Does NOT implement CPB (μΦ extraction, future)
- ❌ Does NOT implement PriorGeometry (future implementation)
- ❌ Does NOT claim General Algebra completion

## Architectural Position

This package establishes **Layers -2 through 1** of General Algebra:

```
Reality (Layer -2) ✅
  ↓
SensoryTransfer (Layer -1) ✅
  ↓
ProtoPrior (Layer 0) ✅
  ↓
CognitiveCarrier (Layer 0.5) ✅
  ↓
Attention (Layer 1) ✅ ← You are here
  ↓
Memory (Layer 2) - Not yet implemented
  ↓
Comparison (Layer 3) - Not yet implemented
  ↓
PrimitiveBinding (future)
  ↓
PriorGeometry (future)
  ↓
Binding Condition Learning - Φ (future)
  ↓
CPB Extraction - μΦ (future)
  ↓
Layer Algebra Generation (future)
  ↓
Physics / Mathematics / Logic / Language
```

## Related Documentation

- `docs/GENERAL_ALGEBRA_FORMAL_SPEC_V01.md` - Constitutional specification
- `docs/GFA_BASELINE_AFTER_PR53.md` - Baseline audit after PR #53
- `tests/test_gfa_proto_prior_kernel.py` - ProtoPrior test suite (44 tests)
- `tests/test_gfa_reality_kernel.py` - Reality test suite (21 tests)
- `tests/test_gfa_sensory_transfer_kernel.py` - SensoryTransfer test suite (25 tests)
- `tests/test_gfa_cognitive_carrier_kernel.py` - CognitiveCarrier test suite (37 tests)
- `tests/test_gfa_attention_kernel.py` - AttentionGeometry test suite (19 tests)

## Status

✅ **RealityGeometry**: Complete (Layer -2)
✅ **SensoryTransferGeometry**: Complete (Layer -1)
✅ **ProtoPrior Kernel**: Complete (Layer 0)
✅ **CognitiveCarrierGeometry**: Complete (Layer 0.5)
✅ **AttentionGeometry**: Complete (Layer 1) ← Latest
⏳ **MemoryGeometry**: Not started (PR-A3)
⏳ **ComparisonGeometry**: Not started (PR-A4)
⏳ **IdentityDifferenceGeometry**: Not started
⏳ **BindingCore**: Not started
⏳ **PrimitiveBinding Kernel**: Not started
⏳ **PriorGeometry Kernel**: Not started
⏳ **Learning (Φ)**: Not started
⏳ **CPB Extraction (μΦ)**: Not started
⏳ **Layer Generator**: Not started

**Current Completion**: 5 layers implemented (Layers -2 through 1). General Algebra is NOT complete.
