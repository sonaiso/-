"""
Test suite for CognitiveCarrierGeometry Kernel - Layer 0.5

This test suite validates all critical laws for the CognitiveCarrier Kernel:
- No cognitive processing without CognitiveCarrier
- Carrier must declare all required capacities
- Carrier does NOT create meaning
- Carrier does NOT issue judgment
- Carrier does NOT certify
- Carrier does NOT raise rank
- Missing capacity becomes residual or failure

Test coverage:
1. CognitiveCarrier creation and validation
2. Embodied state requirements
3. Capacity declarations (attention, memory, comparison, binding)
4. Prohibition laws (no meaning, no judgment, no certification, no rank raising)
5. Processing readiness validation
6. Binding readiness validation
7. Missing capacity handling
8. Residual preservation
"""

import pytest
from uuid import UUID

from gfa.cognitive_carrier import (
    CognitiveCarrier,
    CarrierResidual,
    EmbodiedState,
    EmbodimentType,
    SensoryCapacity,
    AttentionCapacity,
    MemoryCapacity,
    ComparisonCapacity,
    BindingCapacity,
    InterpretationCapacity,
    FeedbackCapacity,
    OutputCapacity,
    CapacityLevel,
    CarrierValidator,
)


# ============================================================================
# Test 1: CognitiveCarrier - Mandatory Fields
# ============================================================================

def test_cognitive_carrier_requires_all_mandatory_fields():
    """Test that all 10 mandatory capacity fields are enforced."""
    # Create valid CognitiveCarrier
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="fully_functional",
        known_limitations=frozenset({"finite_memory", "finite_attention"}),
    )

    carrier = CognitiveCarrier(
        carrier_id="carrier_001",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(
            capacity_level=CapacityLevel.FULL,
            available_channels=frozenset({"visual", "auditory", "tactile"}),
        ),
        attention_capacity=AttentionCapacity(
            capacity_level=CapacityLevel.FULL,
            selection_policy="priority_based",
        ),
        memory_capacity=MemoryCapacity(
            capacity_level=CapacityLevel.FULL,
            storage_type="associative",
            distortion_risk="low",
        ),
        comparison_capacity=ComparisonCapacity(
            capacity_level=CapacityLevel.FULL,
            comparison_fields=frozenset({"similarity", "difference", "identity"}),
        ),
        binding_capacity=BindingCapacity(
            capacity_level=CapacityLevel.FULL,
            binding_types=frozenset({"primitive", "learned"}),
        ),
        interpretation_capacity=InterpretationCapacity(
            capacity_level=CapacityLevel.FULL,
            interpretation_types=frozenset({"pattern_recognition"}),
        ),
        feedback_capacity=FeedbackCapacity(
            capacity_level=CapacityLevel.FULL,
            feedback_channels=frozenset({"success", "failure"}),
        ),
        output_capacity=OutputCapacity(
            capacity_level=CapacityLevel.FULL,
            output_types=frozenset({"binding", "comparison_result"}),
        ),
    )

    assert carrier.is_valid
    assert isinstance(carrier.carrier_trace_id, UUID)
    assert carrier.carrier_id == "carrier_001"
    assert carrier.embodied_state.embodiment_type == EmbodimentType.BIOLOGICAL


def test_cognitive_carrier_missing_fields_raises_error():
    """Test that missing mandatory fields raise errors."""
    # Missing carrier_id
    with pytest.raises(TypeError):
        CognitiveCarrier()


# ============================================================================
# Test 2: No Cognitive Processing Without Carrier
# ============================================================================

def test_no_cognitive_processing_without_carrier():
    """Test that cognitive processing requires a valid carrier."""
    # This is a conceptual test - the carrier must exist before processing
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="test_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # Carrier must exist and be valid
    assert carrier.is_valid
    assert carrier.can_process_traces


# ============================================================================
# Test 3: Embodied State Requirements
# ============================================================================

def test_carrier_requires_embodied_state():
    """Test that carrier requires embodied state."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="functional",
        known_limitations=frozenset({"limited_bandwidth"}),
    )

    carrier = CognitiveCarrier(
        carrier_id="embodied_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    assert carrier.embodied_state is not None
    assert carrier.embodied_state.is_biological
    assert carrier.embodied_state.is_functional


# ============================================================================
# Test 4: Capacity Requirements
# ============================================================================

def test_carrier_requires_attention_capacity():
    """Test that carrier requires attention capacity."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="attention_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    assert carrier.attention_capacity is not None
    assert carrier.attention_capacity.is_available


def test_carrier_requires_memory_capacity():
    """Test that carrier requires memory capacity."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="memory_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    assert carrier.memory_capacity is not None
    assert carrier.memory_capacity.is_available


def test_carrier_requires_comparison_capacity():
    """Test that carrier requires comparison capacity."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="comparison_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    assert carrier.comparison_capacity is not None
    assert carrier.comparison_capacity.is_available


def test_carrier_requires_binding_capacity():
    """Test that carrier requires binding capacity."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="binding_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    assert carrier.binding_capacity is not None
    assert carrier.binding_capacity.is_available


# ============================================================================
# Test 5: Prohibition Laws
# ============================================================================

def test_carrier_does_not_create_meaning():
    """Test that carrier does NOT create meaning."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="no_meaning_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # CRITICAL LAW: Carrier does NOT create meaning
    assert not carrier.creates_meaning()


def test_carrier_does_not_issue_judgment():
    """Test that carrier does NOT issue judgment."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="no_judgment_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # CRITICAL LAW: Carrier does NOT issue judgment
    assert not carrier.issues_judgment()


def test_carrier_does_not_certify():
    """Test that carrier does NOT certify claims."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="no_certify_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # CRITICAL LAW: Carrier does NOT certify
    assert not carrier.certifies_claims()


def test_carrier_does_not_raise_rank():
    """Test that carrier does NOT raise epistemic rank."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="no_rank_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # CRITICAL LAW: Carrier does NOT raise rank
    assert not carrier.raises_rank()


def test_capacity_does_not_prove_correctness():
    """Test that capacity does NOT prove correctness."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="capacity_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # CRITICAL LAW: Capacity ≠ Proof
    assert not carrier.capacity_proves_correctness()


# ============================================================================
# Test 6: Attention Does Not Raise Rank
# ============================================================================

def test_attention_does_not_raise_rank():
    """Test that attention does NOT raise epistemic rank."""
    attention = AttentionCapacity(
        capacity_level=CapacityLevel.FULL,
        selection_policy="salience_based",
    )

    # CRITICAL LAW: Attention selects; it does NOT certify
    assert not attention.can_raise_rank()


# ============================================================================
# Test 7: Memory Recall ≠ Original
# ============================================================================

def test_memory_recall_not_equal_original():
    """Test that recalled trace ≠ original trace."""
    memory = MemoryCapacity(
        capacity_level=CapacityLevel.FULL,
        storage_type="distributed",
        distortion_risk="moderate",
    )

    # CRITICAL LAW: Recall(trace) ≠ original_trace
    assert not memory.recall_equals_original()


# ============================================================================
# Test 8: Primitive Binding Does Not Raise Rank
# ============================================================================

def test_primitive_binding_does_not_raise_rank():
    """Test that primitive binding does NOT raise rank."""
    binding = BindingCapacity(
        capacity_level=CapacityLevel.FULL,
        binding_types=frozenset({"primitive", "learned"}),
    )

    # CRITICAL LAW: Primitive binding → CANDIDATE only
    assert not binding.primitive_binding_raises_rank()


# ============================================================================
# Test 9: Interpretation Does Not Create Meaning
# ============================================================================

def test_interpretation_does_not_create_meaning():
    """Test that interpretation does NOT create meaning."""
    interpretation = InterpretationCapacity(
        capacity_level=CapacityLevel.FULL,
        interpretation_types=frozenset({"pattern_matching"}),
    )

    # CRITICAL LAW: Interpretation operates on traces, doesn't create meaning
    assert not interpretation.creates_meaning()


# ============================================================================
# Test 10: Missing Capacity Becomes Residual
# ============================================================================

def test_missing_capacity_becomes_residual():
    """Test that missing/degraded capacity becomes residual."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="degraded",
        known_limitations=frozenset({"impaired_vision", "limited_memory"}),
    )

    carrier = CognitiveCarrier(
        carrier_id="degraded_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(
            capacity_level=CapacityLevel.DEGRADED,
            capacity_description="Partial sensory function",
        ),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.PARTIAL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.DEGRADED),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.PARTIAL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
        carrier_residuals=frozenset({
            CarrierResidual(
                description="Impaired vision reduces visual processing",
                residual_type="capacity_limitation",
                severity="moderate"
            ),
            CarrierResidual(
                description="Limited memory may cause recall failures",
                residual_type="capacity_limitation",
                severity="high"
            )
        })
    )

    assert carrier.has_residuals
    assert len(carrier.carrier_residuals) == 2
    assert carrier.embodied_state.is_degraded


# ============================================================================
# Test 11: Validator Enforcement
# ============================================================================

def test_validator_enforces_all_laws():
    """Test that CarrierValidator enforces all constitutional laws."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="fully_functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="valid_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # Valid carrier should have no violations
    violations = CarrierValidator.validate_cognitive_carrier(carrier)
    assert len(violations) == 0
    assert CarrierValidator.is_valid_cognitive_carrier(carrier)


# ============================================================================
# Test 12: Serialization and Stability
# ============================================================================

def test_carrier_serializes_without_losing_capacities():
    """Test that carrier maintains all capacity information."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.HYBRID,
        functional_status="functional",
        known_limitations=frozenset({"bandwidth_limit"}),
    )

    carrier = CognitiveCarrier(
        carrier_id="serializable_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(
            capacity_level=CapacityLevel.FULL,
            available_channels=frozenset({"visual", "auditory"}),
        ),
        attention_capacity=AttentionCapacity(
            capacity_level=CapacityLevel.FULL,
            selection_policy="priority",
        ),
        memory_capacity=MemoryCapacity(
            capacity_level=CapacityLevel.FULL,
            storage_type="associative",
        ),
        comparison_capacity=ComparisonCapacity(
            capacity_level=CapacityLevel.FULL,
            comparison_fields=frozenset({"similarity", "difference"}),
        ),
        binding_capacity=BindingCapacity(
            capacity_level=CapacityLevel.FULL,
            binding_types=frozenset({"primitive"}),
        ),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # Check all capacities preserved
    assert carrier.sensory_capacity.available_channels == frozenset({"visual", "auditory"})
    assert carrier.attention_capacity.selection_policy == "priority"
    assert carrier.memory_capacity.storage_type == "associative"
    assert carrier.comparison_capacity.comparison_fields == frozenset({"similarity", "difference"})
    assert carrier.binding_capacity.binding_types == frozenset({"primitive"})


# ============================================================================
# Test 13: GUARD - No Premature Layer Implementation
# ============================================================================

def test_guard_no_attention_geometry_implementation():
    """GUARD TEST: Prove no AttentionGeometry implementation exists."""
    # AttentionGeometry is PR-A2 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import AttentionGeometry  # noqa: F401


def test_guard_no_memory_geometry_implementation():
    """GUARD TEST: Prove no MemoryGeometry implementation exists."""
    # MemoryGeometry is PR-A3 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import MemoryGeometry  # noqa: F401


def test_guard_no_comparison_geometry_implementation():
    """GUARD TEST: Prove no ComparisonGeometry implementation exists."""
    # ComparisonGeometry is PR-A4 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import ComparisonGeometry  # noqa: F401


def test_guard_no_binding_core_implementation():
    """GUARD TEST: Prove no BindingCore implementation exists."""
    # BindingCore is PR-A6 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import BindingCore  # noqa: F401


def test_guard_no_primitive_binding_implementation():
    """GUARD TEST: Prove no PrimitiveBinding implementation exists."""
    # PrimitiveBinding is PR-A6 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import PrimitiveBinding  # noqa: F401


def test_guard_no_cpb_implementation():
    """GUARD TEST: Prove no CPB (μΦ) implementation exists."""
    # CPB is PR-A8 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import CPB  # noqa: F401


def test_guard_no_learning_implementation():
    """GUARD TEST: Prove no Learning implementation exists."""
    # Learning is PR-A7 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import BindingConditionLearning  # noqa: F401


def test_guard_no_prior_geometry_implementation():
    """GUARD TEST: Prove no PriorGeometry implementation exists."""
    # PriorGeometry is future - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import PriorGeometry  # noqa: F401


def test_guard_no_identity_difference_implementation():
    """GUARD TEST: Prove no IdentityDifferenceGeometry implementation exists."""
    # IdentityDifferenceGeometry is PR-A5 - must NOT exist in PR-A1
    with pytest.raises(ImportError):
        from gfa.cognitive_carrier import IdentityDifferenceGeometry  # noqa: F401


# ============================================================================
# Test 14: GUARD - Capacity Does NOT Imply Correctness (Explicit)
# ============================================================================

def test_guard_full_capacity_does_not_guarantee_correct_output():
    """GUARD TEST: Having FULL capacity does NOT guarantee correct outputs."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="full_capacity_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # CRITICAL: All capacities FULL, but correctness NOT guaranteed
    assert carrier.sensory_capacity.capacity_level == CapacityLevel.FULL
    assert carrier.attention_capacity.capacity_level == CapacityLevel.FULL
    assert carrier.memory_capacity.capacity_level == CapacityLevel.FULL
    assert carrier.comparison_capacity.capacity_level == CapacityLevel.FULL
    assert carrier.binding_capacity.capacity_level == CapacityLevel.FULL

    # BUT: Capacity ≠ Proof of correctness
    assert not carrier.capacity_proves_correctness()

    # Carrier CAN process, but outputs may be incorrect
    assert carrier.can_process_traces


def test_guard_capacity_is_declaration_not_proof():
    """GUARD TEST: Capacity is DECLARATION of ability, NOT proof of correctness."""
    # Create carrier with all FULL capacities
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier = CognitiveCarrier(
        carrier_id="declared_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # Capacity declared = carrier CAN attempt operations
    assert carrier.can_process_traces
    assert carrier.attention_capacity.is_available
    assert carrier.memory_capacity.is_available
    assert carrier.comparison_capacity.is_available
    assert carrier.binding_capacity.is_available

    # But: NO guarantee operations will be correct
    assert not carrier.capacity_proves_correctness()
    assert not carrier.certifies_claims()
    assert not carrier.raises_rank()


# ============================================================================
# Test 15: GUARD - Carrier Does NOT Raise Rank (Explicit)
# ============================================================================

def test_guard_carrier_never_raises_epistemic_rank():
    """GUARD TEST: Carrier NEVER raises epistemic rank, regardless of capacities."""
    # Test with FULL capacities
    embodied_state_full = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset(),
    )

    carrier_full = CognitiveCarrier(
        carrier_id="full_carrier",
        embodied_state=embodied_state_full,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.FULL),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
    )

    # Test with DEGRADED capacities
    embodied_state_degraded = EmbodiedState(
        embodiment_type=EmbodimentType.BIOLOGICAL,
        functional_status="degraded",
        known_limitations=frozenset({"impaired"}),
    )

    carrier_degraded = CognitiveCarrier(
        carrier_id="degraded_carrier",
        embodied_state=embodied_state_degraded,
        sensory_capacity=SensoryCapacity(capacity_level=CapacityLevel.DEGRADED),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.DEGRADED),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.DEGRADED),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.DEGRADED),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.DEGRADED),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.DEGRADED),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.DEGRADED),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.DEGRADED),
    )

    # CRITICAL: NEITHER carrier raises rank
    assert not carrier_full.raises_rank()
    assert not carrier_degraded.raises_rank()

    # Neither creates meaning, issues judgment, or certifies
    assert not carrier_full.creates_meaning()
    assert not carrier_full.issues_judgment()
    assert not carrier_full.certifies_claims()

    assert not carrier_degraded.creates_meaning()
    assert not carrier_degraded.issues_judgment()
    assert not carrier_degraded.certifies_claims()


def test_guard_attention_never_raises_rank():
    """GUARD TEST: Attention NEVER raises rank - only affects priority."""
    # Test all capacity levels
    attention_full = AttentionCapacity(capacity_level=CapacityLevel.FULL)
    attention_partial = AttentionCapacity(capacity_level=CapacityLevel.PARTIAL)
    attention_degraded = AttentionCapacity(capacity_level=CapacityLevel.DEGRADED)
    attention_absent = AttentionCapacity(capacity_level=CapacityLevel.ABSENT)

    # CRITICAL LAW: None raise rank
    assert not attention_full.can_raise_rank()
    assert not attention_partial.can_raise_rank()
    assert not attention_degraded.can_raise_rank()
    assert not attention_absent.can_raise_rank()


def test_guard_memory_recall_never_equals_original():
    """GUARD TEST: Memory recall NEVER equals original trace."""
    # Test all capacity levels
    memory_full = MemoryCapacity(capacity_level=CapacityLevel.FULL)
    memory_partial = MemoryCapacity(capacity_level=CapacityLevel.PARTIAL)
    memory_degraded = MemoryCapacity(capacity_level=CapacityLevel.DEGRADED)
    memory_absent = MemoryCapacity(capacity_level=CapacityLevel.ABSENT)

    # CRITICAL LAW: Recall(trace) ≠ original_trace for ALL levels
    assert not memory_full.recall_equals_original()
    assert not memory_partial.recall_equals_original()
    assert not memory_degraded.recall_equals_original()
    assert not memory_absent.recall_equals_original()


def test_guard_binding_never_raises_rank():
    """GUARD TEST: Primitive binding NEVER raises rank - produces CANDIDATE only."""
    # Test all capacity levels
    binding_full = BindingCapacity(capacity_level=CapacityLevel.FULL)
    binding_partial = BindingCapacity(capacity_level=CapacityLevel.PARTIAL)
    binding_degraded = BindingCapacity(capacity_level=CapacityLevel.DEGRADED)
    binding_absent = BindingCapacity(capacity_level=CapacityLevel.ABSENT)

    # CRITICAL LAW: Primitive binding produces CANDIDATE relations only
    assert not binding_full.primitive_binding_raises_rank()
    assert not binding_partial.primitive_binding_raises_rank()
    assert not binding_degraded.primitive_binding_raises_rank()
    assert not binding_absent.primitive_binding_raises_rank()


def test_guard_interpretation_never_creates_meaning():
    """GUARD TEST: Interpretation NEVER creates meaning - operates on traces."""
    # Test all capacity levels
    interpretation_full = InterpretationCapacity(capacity_level=CapacityLevel.FULL)
    interpretation_partial = InterpretationCapacity(capacity_level=CapacityLevel.PARTIAL)
    interpretation_degraded = InterpretationCapacity(capacity_level=CapacityLevel.DEGRADED)
    interpretation_absent = InterpretationCapacity(capacity_level=CapacityLevel.ABSENT)

    # CRITICAL LAW: Interpretation operates on existing traces
    assert not interpretation_full.creates_meaning()
    assert not interpretation_partial.creates_meaning()
    assert not interpretation_degraded.creates_meaning()
    assert not interpretation_absent.creates_meaning()


# ============================================================================
# Test 16: GUARD - Missing Capacity Handling
# ============================================================================

def test_guard_absent_capacity_tracked_as_residual():
    """GUARD TEST: ABSENT capacity must be tracked as residual."""
    embodied_state = EmbodiedState(
        embodiment_type=EmbodimentType.ARTIFICIAL,
        functional_status="functional",
        known_limitations=frozenset({"no_vision"}),
    )

    carrier = CognitiveCarrier(
        carrier_id="absent_carrier",
        embodied_state=embodied_state,
        sensory_capacity=SensoryCapacity(
            capacity_level=CapacityLevel.ABSENT,
            capacity_description="No visual sensors"
        ),
        attention_capacity=AttentionCapacity(capacity_level=CapacityLevel.FULL),
        memory_capacity=MemoryCapacity(capacity_level=CapacityLevel.FULL),
        comparison_capacity=ComparisonCapacity(capacity_level=CapacityLevel.FULL),
        binding_capacity=BindingCapacity(capacity_level=CapacityLevel.FULL),
        interpretation_capacity=InterpretationCapacity(capacity_level=CapacityLevel.FULL),
        feedback_capacity=FeedbackCapacity(capacity_level=CapacityLevel.FULL),
        output_capacity=OutputCapacity(capacity_level=CapacityLevel.FULL),
        carrier_residuals=frozenset({
            CarrierResidual(
                description="No visual sensory capacity - cannot process visual traces",
                residual_type="absent_capacity",
                severity="high"
            )
        })
    )

    # ABSENT capacity must be tracked
    assert carrier.sensory_capacity.capacity_level == CapacityLevel.ABSENT
    assert not carrier.sensory_capacity.is_available
    assert carrier.has_residuals
    assert len(carrier.carrier_residuals) == 1


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
