# Architectural Correction Summary: AlgebraicDecisionCore Governance

## التصحيح المعماري الجوهري

**التصحيح الجوهري:** نقل العبارة من:

```
U₉ calls/creates AlgebraicDecisionCore
```

إلى:

```
U₈→U₉ transition is governed by AlgebraicDecisionCore
```

**المعنى:** موضوع الحوكمة هو **الانتقال** لا الطبقة.

---

## القاعدة المعمارية النهائية

### English

```
Layer does not own Governor.
Governor owns Transition Permission.
```

### العربية

```
الطبقة لا تملك الحاكم.
الحاكم يملك ترخيص الانتقال.
```

---

## النموذج الصناعي الصحيح

### ✓ CORRECT Pattern

```python
Pipeline / Orchestrator
  → asks AlgebraicDecisionCore to approve U₈→U₉
  → receives DecisionAudit
  → if approved: creates ApprovedTransitionContext
  → calls U₉ with ApprovedTransitionContext
  → if rejected: blocks transition and preserves violations/residuals
```

### ✗ WRONG Pattern (Constitutional Violation)

```python
U₉
  → creates AlgebraicDecisionCore()
  → approves itself
  → executes
```

**لماذا هذا خطأ؟**

لأن هذا يجعل **الحارس داخل المحروس**، وهذا يكسر المعنى الدستوري للحاكم.

---

## الصياغة القانونية المختصرة

### English

```
No U₉ execution without ApprovedTransitionContext.
No ApprovedTransitionContext without AlgebraicDecisionCore approval.
No AlgebraicDecisionCore approval without identity, domain, gate,
    evidence, rank, residuals, trace, and no-leap validation.
```

### العربية

```
لا تشغيل لـ U₉ بلا سياق انتقال مُجاز.
ولا سياق انتقال مُجاز بلا موافقة النواة الجبرية للقرار.
ولا موافقة بلا فحص الهوية والمجال والبوابة والدليل والرتبة والبقايا والأثر ومنع القفز.
```

---

## أثر هذا التصحيح

بهذا لا نسمح لـ U₉ أن تبتلع الحاكم، كما لا نسمح:

- للوزن أن يبتلع الجذر
- للوزن أن يبتلع المعنى
- للوزن أن يبتلع الوظيفة
- لـ U₈ أن يبتلع حافة الاتفاق

القانون يصبح متسقًا:

```
U₈ لا يبتلع حافة الاتفاق.
U₉ لا يبتلع المعنى أو الوظيفة.
U₉ لا يبتلع الحاكم.
الحاكم لا ينفذ الوزن، بل يرخّص الانتقال إليه.
```

---

## Implementation Summary

### Files Created

1. **`src/dal_core/approved_transition_context.py`**
   - `ApprovedTransitionContext` dataclass
   - `create_approved_context()` factory
   - Post-init validation (ensures true approval)
   - Complete constitutional documentation

2. **`docs/ALGEBRAIC_DECISION_CORE_GOVERNANCE_PATTERN.md`**
   - Wrong vs. Correct pattern comparison
   - Complete pipeline/orchestrator example
   - U₉ layer implementation with verification
   - Constitutional laws summary
   - Migration guide

### Files Modified

1. **`src/dal_core/u9_arabic_weight.py`**
   - Added "Constitutional Governance" section in header
   - Added "Architectural Law" statement
   - Added "Execution Pattern" documentation
   - Added "Constitutional Requirements" with 8-dimensional validation
   - Added "Domain Boundaries" (forbidden/permitted)
   - Added Critical Law #8: NO internal AlgebraicDecisionCore instantiation

2. **`src/dal_core/__init__.py`**
   - Export `ApprovedTransitionContext`
   - Export `create_approved_context`

---

## Constitutional Architecture

### Three-Level Governance

```
┌─────────────────────────────────────────────────┐
│  AlgebraicDecisionCore (Constitutional Level)   │
│  - Owns transition permissions                  │
│  - Enforces 8-dimensional validation            │
│  - Owned by Pipeline/Orchestrator               │
└──────────────┬──────────────────────────────────┘
               │ governs
               ↓
┌──────────────────────────────────────────────────┐
│  ApprovedTransitionContext (Evidence Level)      │
│  - Proof of AlgebraicDecisionCore approval       │
│  - Passed to layers as evidence                  │
│  - Cannot be created without approval            │
└──────────────┬───────────────────────────────────┘
               │ passed to
               ↓
┌──────────────────────────────────────────────────┐
│  U₉ (Execution Level)                            │
│  - Receives ApprovedTransitionContext            │
│  - Verifies context before execution             │
│  - MUST NOT create AlgebraicDecisionCore         │
└──────────────────────────────────────────────────┘
```

### The 8-Dimensional Validation

Every transition MUST pass all 8 checks:

1. **Identity** (الهوية): `ROOT_MATERIAL_IDENTITY → WEIGHT_IDENTITY`
2. **Domain** (المجال): `WEIGHT_DOMAIN` only (no meaning, syntax, hukm)
3. **Gate** (البوابة): `WeightTransitionGate` passed
4. **Evidence** (الدليل): Root/stem candidacy evidence present
5. **Rank** (الرتبة): `CANDIDATE → CANDIDATE` (no elevation without evidence)
6. **Residuals** (البقايا): No blocking residuals
7. **Trace** (الأثر): Complete `U₀→U₁→...→U₈` trace preserved
8. **No Leap** (منع القفز): Sequential progression verified

---

## Domain Boundaries for U₉ (WEIGHT_DOMAIN)

### ✗ Forbidden in WEIGHT_DOMAIN

```python
# These determinations violate domain boundaries:
- Meaning determination (معنى)
    # صيغة فاعل ≠ معنى الفاعلية
- Syntactic role (فاعل نحوي)
    # صيغة فاعل ≠ الفاعل النحوي
- I'rab judgment (إعراب)
- Hukm (حكم)
- Semantic derivation (اشتقاق معنوي)
- Functional assignment (وظيفة)
```

### ✓ Permitted in WEIGHT_DOMAIN

```python
# These determinations are within domain competency:
- Weight pattern (وزن)
- Morphological template (قالب صرفي)
- F-'-L mapping (فاء-عين-لام)
```

---

## Code Pattern Examples

### Pipeline/Orchestrator (Correct)

```python
class ArabicPipeline:
    def __init__(self):
        # ✓ Pipeline owns the governor
        self.governor = AlgebraicDecisionCore()
        self.existing_identities = set()

    def execute_u8_to_u9(self, u8_output):
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
            gate_passed=True,
            evidence=("root_candidate",),
            required_evidence=frozenset({"root_candidate"}),
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

        # 4. Execute U₉ with approved context
        u9_output = transition_to_weight(u8_output, context)

        # 5. Update identities
        self.existing_identities.add(IdentityType.WEIGHT_IDENTITY)

        return u9_output
```

### U₉ Layer (Correct)

```python
def transition_to_weight(
    u8_root_stem: RootStemCandidateUnit,
    approved_context: ApprovedTransitionContext  # ✓ Required parameter
) -> WeightCandidateUnit:
    """
    Transition U₈ → U₉ under constitutional governance.

    Constitutional Requirements:
        - MUST receive ApprovedTransitionContext
        - MUST verify context is approved
        - MUST NOT instantiate AlgebraicDecisionCore
    """
    # ✓ Verify constitutional requirements
    if approved_context is None:
        raise TypeError(
            "Constitutional violation: U₉ requires ApprovedTransitionContext"
        )

    if not approved_context.is_approved():
        raise ValueError(
            f"Context not approved: {approved_context.audit.cpb_status}"
        )

    # ✓ Verify correct layer transition
    if approved_context.to_layer != ExecutionLayer.U9_WEIGHT:
        raise ValueError(f"Context is for {approved_context.to_layer}, not U₉")

    # ✓ Verify correct domain
    if approved_context.domain != DomainType.WEIGHT_DOMAIN:
        raise ValueError(
            f"Context domain is {approved_context.domain}, not WEIGHT_DOMAIN"
        )

    # ✓ Now execute with constitutional protection
    weight_candidate = WeightCandidateUnit(
        # ... weight analysis ...
        trace=approved_context.trace + (u8_root_stem.unit_id,),
        residuals=approved_context.get_residuals(),
        rank=approved_context.get_rank(),
        decision_id=approved_context.get_decision_id()
    )

    return weight_candidate
```

---

## Migration Path

### If you have code that violates the constitutional pattern:

**Before (Violation):**
```python
def my_u9_function(u8_input):
    core = AlgebraicDecisionCore()  # ❌ WRONG
    audit = core.decide_transition(...)
    if audit.is_approved():
        return self.execute(u8_input)
```

**After (Constitutional):**
```python
# In Pipeline:
audit = self.governor.decide_transition(...)
if audit.is_approved():
    context = create_approved_context(audit, existing_identities)
    output = my_u9_function(u8_input, context)

# In U₉:
def my_u9_function(u8_input, approved_context):
    # ✓ Verify context
    if not approved_context.is_approved():
        raise ValueError("Context not approved")
    # ... execute with constitutional protection
```

---

## Consistency with Previous PRs

This architectural correction is consistent with:

### PR #110: U₇-C → U₈ Transition

```
U₈ لا يبتلع حافة الاتفاق داخل الجذر
U₈ does not absorb agreement edge into root
```

### PR #111: Inflexional Surface Contract

```
U₈ لا يبتلع حافة الاتفاق
حافة الاتفاق محفوظة في الأثر
Agreement edge preserved in trace, not absorbed
```

### PR #112: AlgebraicDecisionCore Governance

```
U₉ لا يبتلع الحاكم
الحاكم يملك الانتقال لا الطبقة
Layer does not own Governor
Governor owns Transition Permission
```

---

## الخلاصة النهائية

هذه الصياغة تجعل #112 أساسًا صحيحًا لـ U₉ وما بعدها.

القانون المركزي بعد #112:

```
كل انتقال قرار.
كل قرار له هوية.
كل هوية لها مجال.
كل مجال له دالة.
كل دالة لها بوابة.
كل بوابة لها دليل.
كل دليل له رتبة.
كل رتبة لها بقايا.
والـ CPB يحرس ذلك كله.

والحاكم فوق الطبقات جميعًا.
والطبقة لا تملك الحاكم.
والحاكم يملك ترخيص الانتقال.
```

The Central Law after #112:

```
Every transition is a decision.
Every decision has an identity.
Every identity has a domain.
Every domain has a function.
Every function has a gate.
Every gate has evidence.
Every evidence has rank.
Every rank has residuals.
And CPB guards all of this.

And the Governor is above all layers.
And the Layer does not own the Governor.
And the Governor owns Transition Permission.
```

---

## References

- **Implementation**: `src/dal_core/approved_transition_context.py`
- **Pattern Documentation**: `docs/ALGEBRAIC_DECISION_CORE_GOVERNANCE_PATTERN.md`
- **U₉ Constitutional Law**: `src/dal_core/u9_arabic_weight.py` (header)
- **Core Governor**: `src/dal_core/algebraic_decision_core.py`
- **Identity System**: `src/dal_core/identity_registry.py`
- **Domain System**: `src/dal_core/domain_registry.py`

---

**PR**: #112 - AlgebraicDecisionCore Governance
**Date**: 2026-05-26
**Status**: Architectural correction complete
**Next**: Write tests for ApprovedTransitionContext and governance pattern
