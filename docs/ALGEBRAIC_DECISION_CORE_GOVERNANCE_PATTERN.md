# AlgebraicDecisionCore Governance Pattern

## Constitutional Principle

**Layer does not own Governor. Governor owns Transition Permission.**

الطبقة لا تملك الحاكم. الحاكم يملك ترخيص الانتقال.

## The Problem

**WRONG PATTERN** (Constitutional Violation):
```python
# ❌ U₉ creates and owns AlgebraicDecisionCore
class U9_WeightLayer:
    def process(self, u8_input):
        # WRONG: Layer instantiates governor
        core = AlgebraicDecisionCore()
        audit = core.decide_transition(...)

        if audit.is_approved():
            return self.execute(u8_input)
```

**Why this is wrong:**
- Makes the guard inside the guarded (الحارس داخل المحروس)
- Layer approves itself
- Breaks constitutional separation of powers
- Same architectural violation as "weight absorbing meaning" or "U₈ absorbing agreement edge"

## The Solution

**CORRECT PATTERN** (Constitutional):
```python
# ✓ Pipeline/Orchestrator owns AlgebraicDecisionCore
class ArabicPipeline:
    def __init__(self):
        # Pipeline owns the governor
        self.governor = AlgebraicDecisionCore()
        self.existing_identities = set()

    def execute_u8_to_u9_transition(self, u8_output):
        # 1. Ask governor for approval
        audit = self.governor.decide_transition(
            transition_id="U8_to_U9_weight",
            from_layer=ExecutionLayer.U8_ROOT_STEM,
            to_layer=ExecutionLayer.U9_WEIGHT,
            input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
            output_identity=IdentityType.WEIGHT_IDENTITY,
            existing_identities=frozenset(self.existing_identities),
            domain=DomainType.WEIGHT_DOMAIN,
            attempted_determination="weight_pattern",
            gate_name="WeightTransitionGate",
            gate_passed=self._check_weight_gate(u8_output),
            evidence=("root_candidate_evidence",),
            required_evidence=frozenset({"root_candidate_evidence"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.CANDIDATE,
            residual_set=u8_output.residuals,
            trace=u8_output.trace
        )

        # 2. Check approval
        if not audit.is_approved():
            return self._handle_rejection(audit)

        # 3. Create approved context
        context = create_approved_context(
            audit,
            frozenset(self.existing_identities)
        )

        # 4. Pass context to U₉
        u9_output = transition_to_weight(u8_output, context)

        # 5. Update identity registry
        self.existing_identities.add(IdentityType.WEIGHT_IDENTITY)

        return u9_output

    def _handle_rejection(self, audit):
        """Handle transition rejection."""
        print(f"Transition blocked: {audit.cpb_status}")
        for violation in audit.violations:
            print(f"  - {violation}")
        return None
```

## U₉ Layer Implementation

```python
# u9_arabic_weight.py

from dal_core.approved_transition_context import ApprovedTransitionContext

def transition_to_weight(
    u8_root_stem: RootStemCandidateUnit,
    approved_context: ApprovedTransitionContext
) -> WeightCandidateUnit:
    """
    Transition U₈ → U₉ under AlgebraicDecisionCore governance.

    Constitutional Requirements:
        - MUST receive ApprovedTransitionContext
        - MUST verify context is approved
        - MUST NOT instantiate AlgebraicDecisionCore internally

    Args:
        u8_root_stem: Root/stem candidate from U₈
        approved_context: Approved transition context from governor

    Returns:
        WeightCandidateUnit with preserved trace and residuals

    Raises:
        ValueError: If approved_context is not truly approved
        TypeError: If approved_context is missing
    """
    # Constitutional verification
    if approved_context is None:
        raise TypeError(
            "Constitutional violation: U₉ requires ApprovedTransitionContext. "
            "Pipeline/Orchestrator must obtain approval from AlgebraicDecisionCore."
        )

    if not approved_context.is_approved():
        raise ValueError(
            f"Constitutional violation: Context not approved. "
            f"CPB Status: {approved_context.audit.cpb_status}"
        )

    # Verify transition is U₈ → U₉
    if approved_context.to_layer != ExecutionLayer.U9_WEIGHT:
        raise ValueError(
            f"Context is for {approved_context.to_layer}, not U₉"
        )

    # Verify domain is WEIGHT_DOMAIN
    if approved_context.domain != DomainType.WEIGHT_DOMAIN:
        raise ValueError(
            f"Context domain is {approved_context.domain}, not WEIGHT_DOMAIN"
        )

    # Now execute weight analysis
    # (with full constitutional protection)

    weight_candidate = WeightCandidateUnit(
        unit_id=str(uuid4()),
        surface=u8_root_stem.surface,
        weight_type=determine_weight_type(u8_root_stem),
        weight_pattern=extract_weight_pattern(u8_root_stem),
        faa_ayn_lam_mapping=map_faa_ayn_lam(u8_root_stem),

        # Preserve constitutional requirements
        trace=approved_context.trace + (u8_root_stem.unit_id,),
        residuals=approved_context.get_residuals(),
        rank=approved_context.get_rank(),
        evidence=approved_context.get_evidence(),

        # Domain boundary respect
        meaning=None,  # ✗ Forbidden in WEIGHT_DOMAIN
        syntactic_role=None,  # ✗ Forbidden
        i3rab=None,  # ✗ Forbidden
        hukm=None,  # ✗ Forbidden

        # Metadata
        decision_id=approved_context.get_decision_id(),
        transition_id=approved_context.get_transition_id()
    )

    return weight_candidate
```

## Pipeline/Orchestrator Complete Example

```python
"""
Complete example of constitutional governance in Arabic NLP pipeline.
"""

from dal_core.algebraic_decision_core import AlgebraicDecisionCore
from dal_core.approved_transition_context import create_approved_context
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation import Rank


class ConstitutionalArabicPipeline:
    """
    Arabic NLP Pipeline with Constitutional Governance.

    The pipeline owns AlgebraicDecisionCore and governs all transitions.
    Individual layers NEVER instantiate the governor.
    """

    def __init__(self):
        """Initialize pipeline with governor."""
        # Central governor (owned by pipeline, not layers)
        self.governor = AlgebraicDecisionCore()

        # Identity tracking across pipeline
        self.existing_identities = set([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ORTHOGRAPHIC_IDENTITY
        ])

        # Layer outputs (preserved for trace)
        self.layer_outputs = {}

    def execute_full_pipeline(self, text: str):
        """
        Execute full pipeline with governance at every transition.

        Args:
            text: Input Arabic text

        Returns:
            Final output with complete audit trail
        """
        # U₀ → U₁ → ... → U₇ → U₈
        # (each transition governed by AlgebraicDecisionCore)

        u0_output = self.execute_u0(text)
        u1_output = self.execute_u0_to_u1(u0_output)
        # ... (continue through layers)
        u8_output = self.execute_u7c_to_u8(u7c_output)

        # U₈ → U₉ (governed transition)
        u9_output = self.execute_u8_to_u9(u8_output)

        return u9_output

    def execute_u8_to_u9(self, u8_output):
        """
        Execute U₈ → U₉ transition with full governance.

        This is the CORRECT pattern for all layer transitions.
        """
        # 1. Prepare transition request
        transition_request = {
            "transition_id": "U8_to_U9_weight",
            "from_layer": ExecutionLayer.U8_ROOT_STEM,
            "to_layer": ExecutionLayer.U9_WEIGHT,
            "input_identity": IdentityType.ROOT_MATERIAL_IDENTITY,
            "output_identity": IdentityType.WEIGHT_IDENTITY,
            "existing_identities": frozenset(self.existing_identities),
            "domain": DomainType.WEIGHT_DOMAIN,
            "attempted_determination": "weight_pattern",
            "gate_name": "WeightTransitionGate",
            "gate_passed": self._verify_weight_gate(u8_output),
            "evidence": tuple(u8_output.evidence),
            "required_evidence": frozenset({"root_candidate_evidence"}),
            "input_rank": u8_output.rank,
            "output_rank": Rank.CANDIDATE,  # Maintain candidate status
            "residual_set": u8_output.residuals,
            "trace": u8_output.trace
        }

        # 2. Ask governor for decision
        audit = self.governor.decide_transition(**transition_request)

        # 3. Check decision
        if not audit.is_approved():
            print(f"❌ U₈→U₉ transition BLOCKED")
            print(f"   CPB Status: {audit.cpb_status}")
            for violation in audit.violations:
                print(f"   - {violation}")
            return None

        print(f"✓ U₈→U₉ transition APPROVED")
        print(f"  Decision ID: {audit.decision_id}")

        # 4. Create approved context
        approved_context = create_approved_context(
            audit,
            frozenset(self.existing_identities)
        )

        # 5. Execute U₉ with approved context
        u9_output = transition_to_weight(u8_output, approved_context)

        # 6. Update identity registry
        self.existing_identities.add(IdentityType.WEIGHT_IDENTITY)
        self.layer_outputs[ExecutionLayer.U9_WEIGHT] = u9_output

        return u9_output

    def _verify_weight_gate(self, u8_output) -> bool:
        """
        Verify that weight transition gate requirements are met.

        Gate Requirements:
            1. Root material identity established
            2. No blocking residuals
            3. Trace complete from U₀
            4. Evidence of root candidacy
        """
        # Check root material identity
        if not hasattr(u8_output, 'root_material'):
            return False

        # Check no blocking residuals
        if u8_output.residuals.has_blocking():
            return False

        # Check trace completeness
        if not u8_output.trace or len(u8_output.trace) < 8:
            return False

        # Check evidence
        if not u8_output.evidence:
            return False

        return True


# Usage Example
if __name__ == "__main__":
    pipeline = ConstitutionalArabicPipeline()

    # Process Arabic text with full governance
    text = "كَاتِبٌ"
    result = pipeline.execute_full_pipeline(text)

    if result:
        print(f"\n✓ Pipeline executed successfully")
        print(f"  Final identity: {result.identity}")
        print(f"  Weight type: {result.weight_type}")
        print(f"  Weight pattern: {result.weight_pattern}")
        print(f"  Decision trail: {len(result.trace)} decisions")
```

## Constitutional Laws Summary

### Three-Level Governance

1. **Layer CPB (Local)**: Each layer has internal CPB (CPB₀, CPB₁, ..., CPB₉)
   - Validates layer-specific constraints
   - Example: CPB₈ ensures root starts from licensed input

2. **AlgebraicDecisionCore (Cross-layer)**: Governor above all layers
   - Validates transitions between layers
   - Enforces 8-dimensional audit
   - Owned by Pipeline/Orchestrator, NOT by layers

3. **ApprovedTransitionContext (Evidence)**: Proof of approval
   - Created only after AlgebraicDecisionCore approval
   - Passed to target layer as evidence
   - Layer MUST verify context before execution

### Constitutional Requirements

```
No U₉ execution without ApprovedTransitionContext.
No ApprovedTransitionContext without AlgebraicDecisionCore approval.
No AlgebraicDecisionCore approval without 8-dimensional validation.
```

وبالعربية:

```
لا تشغيل لـ U₉ بلا سياق انتقال مُجاز.
ولا سياق انتقال مُجاز بلا موافقة النواة الجبرية للقرار.
ولا موافقة بلا فحص الهوية والمجال والبوابة والدليل والرتبة والبقايا والأثر ومنع القفز.
```

### The 8-Dimensional Audit

Every transition MUST pass:

1. **Identity** (الهوية): Valid identity progression
2. **Domain** (المجال): Operation within competency
3. **Gate** (البوابة): Required gates passed
4. **Evidence** (الدليل): Sufficient evidence provided
5. **Rank** (الرتبة): Valid rank progression
6. **Residuals** (البقايا): No blocking residuals
7. **Trace** (الأثر): Complete execution trace
8. **No Leap** (منع القفز): Sequential progression

## Migration Guide

If you have code that violates the constitutional pattern:

### Before (Violation):
```python
def my_u9_function(u8_input):
    core = AlgebraicDecisionCore()  # ❌ WRONG
    audit = core.decide_transition(...)
    # ...
```

### After (Constitutional):
```python
# In pipeline:
audit = self.governor.decide_transition(...)
if audit.is_approved():
    context = create_approved_context(audit, existing_identities)
    output = my_u9_function(u8_input, context)

# In U₉ layer:
def my_u9_function(u8_input, approved_context):
    # ✓ Verify context
    if not approved_context.is_approved():
        raise ValueError("Context not approved")
    # ... execute with constitutional protection
```

## See Also

- `src/dal_core/algebraic_decision_core.py` - Governor implementation
- `src/dal_core/approved_transition_context.py` - Approved context contract
- `src/dal_core/identity_registry.py` - Identity type system
- `src/dal_core/domain_registry.py` - Domain boundary system
- `docs/ALGEBRAIC_DECISION_CORE.md` - Complete governance documentation

## PR Reference

- PR #112: AlgebraicDecisionCore governance
- Created: 2026-05-26
- Constitutional principle established
