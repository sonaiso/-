# CognitiveCarrierGeometry Kernel

**Layer 0.5 - The Cognitive Processing Substrate**

## Purpose

CognitiveCarrierGeometry establishes the **admissibility substrate** required before any cognitive processing can occur. This is NOT a cognitive processing implementation - it is the **declaration of capacity** to perform cognitive operations.

## Core Principle

```
No cognitive processing without an admissible CognitiveCarrier.
```

`FirstPriorUnit` cannot be:
- Processed
- Compared
- Remembered
- Interpreted
- Bound

...unless there exists a `CognitiveCarrier` with declared minimal capacities.

## What This Kernel IS

✅ **Substrate Declaration**: Declares what capacities a carrier possesses
✅ **Capacity Types**: 8 capacity types (sensory, attention, memory, comparison, binding, interpretation, feedback, output)
✅ **Embodiment State**: Physical/biological/artificial/hybrid embodiment
✅ **Residual Tracking**: Missing/degraded capacities become residuals
✅ **Constitutional Laws**: Enforces 16 critical prohibition laws

## What This Kernel IS NOT

❌ **NOT Attention Implementation**: Does not select traces for processing
❌ **NOT Memory Implementation**: Does not store or recall traces
❌ **NOT Comparison Implementation**: Does not compare traces
❌ **NOT Binding Implementation**: Does not create bindings
❌ **NOT CPB**: Does not implement neutral binding element
❌ **NOT Learning**: Does not extract binding conditions
❌ **NOT Meaning Generation**: Does not create semantic content
❌ **NOT Judgment**: Does not issue epistemic judgments
❌ **NOT Certification**: Does not certify claims

## Critical Laws

### Prohibition Laws

1. **Carrier does NOT create meaning**
2. **Carrier does NOT issue judgment**
3. **Carrier does NOT certify claims**
4. **Carrier does NOT raise epistemic rank**

### Capacity Laws

5. **Capacity is declaration, NOT proof** - Having capacity ≠ correctness of outputs
6. **Attention capacity does NOT raise rank** - Affects processing priority only
7. **Memory recall ≠ original trace** - Recall creates new trace about original
8. **Primitive binding does NOT raise rank** - Produces CANDIDATE relations only
9. **Interpretation does NOT create meaning** - Operates on existing traces

### Structural Laws

10. **Missing capacity becomes residual** - Absent/degraded capacity must be tracked
11. **Embodiment state required** - Carrier must have embodied substrate
12. **All capacities must be declared** - Attention, memory, comparison, binding required

## Architecture Position

```
Layer -2: RealityGeometry
    ↓ (produces RealityEffects)
Layer -1: SensoryTransfer
    ↓ (produces SensoryTraces)
Layer 0: ProtoPrior/FirstPriorUnit
    ↓ (requires processing substrate)
Layer 0.5: CognitiveCarrier ⬅️ THIS KERNEL
    ↓ (provides substrate for...)
Future Layers:
    AttentionGeometry (PR-A2)
    MemoryGeometry (PR-A3)
    ComparisonGeometry (PR-A4)
    IdentityDifferenceGeometry (PR-A5)
    PrimitiveBinding (PR-A6)
    Learning (PR-A7)
    CPB = μΦ (PR-A8)
```

## Usage Example

```python
from gfa.cognitive_carrier import (
    CognitiveCarrier,
    EmbodiedState,
    EmbodimentType,
    AttentionCapacity,
    MemoryCapacity,
    ComparisonCapacity,
    BindingCapacity,
    CapacityLevel,
)

# Create embodied state
embodied_state = EmbodiedState(
    embodiment_type=EmbodimentType.BIOLOGICAL,
    functional_status="functional",
    known_limitations=frozenset({"finite_memory", "finite_attention"}),
)

# Declare carrier with capacities
carrier = CognitiveCarrier(
    carrier_id="human_carrier_001",
    embodied_state=embodied_state,
    attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
    memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
    comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
    binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
    # ... other capacities ...
)

# Verify carrier validity
assert carrier.is_valid
assert carrier.can_process_traces

# Verify prohibitions
assert not carrier.creates_meaning()
assert not carrier.issues_judgment()
assert not carrier.certifies_claims()
assert not carrier.raises_rank()
```

## Key Distinctions

### Capacity vs Implementation

- **This kernel**: Declares capacity exists (`attention_capacity`)
- **Future kernels**: Implement what capacity does (`AttentionGeometry` selects traces)

### Declaration vs Proof

- **Having capacity**: Carrier can attempt operations
- **Proof of correctness**: Requires evidence, testing, validation in later layers

### Substrate vs Processing

- **Substrate** (this kernel): "I have the machinery to process"
- **Processing** (future kernels): "I am processing this trace"

## Next Steps

After this kernel is hardened:

1. **PR-A2**: `AttentionGeometry` - Trace selection (not certification)
2. **PR-A3**: `MemoryGeometry` - Storage/recall (recall ≠ original)
3. **PR-A4**: `ComparisonGeometry` - Foundation for binding
4. **PR-A5**: `IdentityDifferenceGeometry` - Origin of classification
5. **PR-A6**: `PrimitiveBinding` - Weak experimental binding
6. **PR-A7**: `BindingConditionLearning` - Extract correct binding conditions
7. **PR-A8**: `CPB = μΦ` - Neutral binding as learned fixed point

## Testing

All 20 tests passing (100% success rate):
- Mandatory field enforcement
- Embodiment requirements
- Capacity declarations
- Prohibition laws
- Missing capacity handling
- Serialization preservation

## References

- **Commit**: 6084312
- **Tests**: `tests/test_gfa_cognitive_carrier_kernel.py`
- **Validator**: `carrier_validator.py` (16 constitutional laws)
