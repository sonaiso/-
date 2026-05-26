# Algebraic Decision Core Architecture

**النواة الجبرية للقرار - Governance Layer Above All Execution Layers**

## Overview

AlgebraicDecisionCore is a **governance layer** that sits above all execution layers (U₀-Uₙ) in the Arabic linguistic pipeline. It does NOT replace these layers - it audits and controls every transition to ensure:

1. Identity preservation
2. Domain boundary enforcement
3. Gate passage validation
4. Evidence sufficiency
5. Rank progression consistency
6. Residual tracking
7. Trace preservation
8. Forbidden leap prevention

## Architecture

```
AlgebraicDecisionCore (Governance Layer)
    ├── IdentityRegistry (25+ identity types)
    ├── DomainRegistry (19+ domains)
    ├── TransitionRegistry (to be implemented)
    ├── GateRegistry (to be implemented)
    ├── EvidenceRegistry (to be implemented)
    ├── RankPolicy (extends existing Rank)
    ├── ResidualGeometry (extends existing ResidualSet)
    ├── CPBIdentityGuardian (unified CPB across layers)
    └── AppendixSystem (extensibility - to be implemented)

        ↓ (governs all transitions)

Execution Layers (Operational)
    U₀ Unicode → U₁ Grapheme → U₂p Phonetic → U₂s Syllable
    → U₃ Boundary → U₄ TrueLafẓ → U₅ FunctionalRole
    → U₆ MabniClosedClass → U₇(A/B/C) SurfaceProtection
    → U₈ RootStem → U₉ Weight → U₁₀+ (Design layers)
```

## Central Law (القانون المركزي)

```
كل انتقال قرار.         Every transition is a decision.
كل قرار له هوية.         Every decision has an identity.
كل هوية لها مجال.        Every identity has a domain.
كل مجال له دالة.         Every domain has a function.
كل دالة لها بوابة.       Every function has a gate.
كل بوابة لها دليل.       Every gate has evidence.
كل دليل له رتبة.         Every evidence has rank.
كل رتبة لها بقايا.       Every rank has residuals.
والـ CPB يحرس ذلك كله.    And CPB guards all of this.
```

## Core Components

### 1. IdentityRegistry

Tracks ALL identity types in the Arabic linguistic pipeline.

**Purpose**: Ensure no layer skips identity verification.

**Identity Types** (25+):
- Surface: `RAW_SURFACE_IDENTITY`, `ORTHOGRAPHIC_IDENTITY`
- Phonetic: `PHONETIC_IDENTITY`, `SYLLABIC_IDENTITY`
- Boundary: `BOUNDARY_IDENTITY`
- Lafz: `LAFZ_IDENTITY`
- Protection: `MARKER_IDENTITY`, `PROTECTED_SURFACE_IDENTITY`, `PROTECTED_CORE_IDENTITY`
- Root Licensing: `LICENSED_ROOT_INPUT_IDENTITY`
- Morphological: `ROOT_MATERIAL_IDENTITY`, `STEM_IDENTITY` (candidates, NOT certificates)
- Weight: `WEIGHT_IDENTITY`, `FORM_IDENTITY`
- Derivational: `SOURCE_IDENTITY`, `ATTRIBUTE_IDENTITY`
- Closed Class: `CLOSED_CLASS_IDENTITY`
- Syntactic: `FUNCTIONAL_RELATION_IDENTITY`, `AMIL_IDENTITY`, `MAAMUL_IDENTITY`
- Agreement: `AGREEMENT_IDENTITY`, `REFERENCE_IDENTITY`
- Semantic: `SEMANTIC_IDENTITY`, `IFADAH_IDENTITY`
- Judgment: `HUKM_IDENTITY`

**Constitutional Laws**:
```python
# No root before license
ROOT_MATERIAL_IDENTITY requires LICENSED_ROOT_INPUT_IDENTITY

# No weight before root
WEIGHT_IDENTITY requires ROOT_MATERIAL_IDENTITY

# No function before form
FUNCTIONAL_RELATION_IDENTITY requires FORM_IDENTITY

# No semantics before syntax
SEMANTIC_IDENTITY requires FUNCTIONAL_RELATION_IDENTITY

# No judgment before semantics
HUKM_IDENTITY requires SEMANTIC_IDENTITY
```

**Usage**:
```python
from dal_core.identity_registry import IdentityRegistry, IdentityType

registry = IdentityRegistry()

# Check if transition is valid
can_transition, reason = registry.can_transition(
    from_identity=IdentityType.PROTECTED_CORE_IDENTITY,
    to_identity=IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
    existing_identities=frozenset({
        IdentityType.RAW_SURFACE_IDENTITY,
        IdentityType.PROTECTED_CORE_IDENTITY
    })
)

if can_transition:
    # Proceed with transition
    pass
else:
    # Handle violation
    print(f"Transition blocked: {reason}")
```

### 2. DomainRegistry

Defines and enforces domain boundaries for all operations.

**Purpose**: Ensure every judgment occurs within its proper domain.

**Domain Types** (19+):
- Surface: `SCRIPT_DOMAIN`, `SOUND_DOMAIN`
- Phonological: `SYLLABLE_DOMAIN`, `BOUNDARY_DOMAIN`
- Lexical: `LAFZ_DOMAIN`
- Protection: `MARKER_PROTECTION_DOMAIN`, `CLAUSE_AGREEMENT_DOMAIN`
- Morphological: `ROOT_STEM_DOMAIN`, `WEIGHT_DOMAIN`
- Derivational: `SOURCE_FORM_DOMAIN`, `ATTRIBUTE_FORM_DOMAIN`, `FUNCTIONAL_FORM_DOMAIN`
- Syntactic: `AMIL_RELATION_DOMAIN`, `I3RAB_SURFACE_DOMAIN`, `SYNTAX_DOMAIN`
- Semantic: `SEMANTICS_DOMAIN`, `PRAGMATICS_DOMAIN`
- Meta: `EVIDENCE_DOMAIN`, `JUDGMENT_DOMAIN`

**Critical Distinction - The فاعل Problem**:
```
صيغة فاعل (WEIGHT_DOMAIN)
    ≠ الفاعل النحوي (SYNTAX_DOMAIN)
    ≠ معنى الفاعلية (SEMANTICS_DOMAIN)

"فاعل" as morphological pattern (weight domain)
    ≠ "فاعل" as syntactic agent (syntax domain)
    ≠ "فاعل" as semantic performer (semantics domain)
```

**Prohibitions**:
- `WEIGHT_DOMAIN` prohibits: `syntactic_role`, `meaning`, `i3rab`
- `SYNTAX_DOMAIN` prohibits: `meaning`, `semantic_interpretation`
- `ROOT_STEM_DOMAIN` prohibits: `root_certification` (only candidates in U₈)

**Usage**:
```python
from dal_core.domain_registry import DomainRegistry, DomainType

registry = DomainRegistry()

# Check if determination is allowed in domain
can_determine, reason = registry.can_determine_in_domain(
    domain_type=DomainType.WEIGHT_DOMAIN,
    competency="weight_pattern"  # Allowed
)

# This would fail:
can_determine, reason = registry.can_determine_in_domain(
    domain_type=DomainType.WEIGHT_DOMAIN,
    competency="meaning"  # Forbidden!
)
```

### 3. CPBIdentityGuardian

Unified CPB (Completeness Predicate and Proof Builder) across all layers.

**Purpose**: Coordinate all individual layer CPBs (CPB₀, CPB₁, ..., CPB₈, CPB₉) under single governance.

**Verification Dimensions**:
1. **Identity**: Input → Output identity valid?
2. **Domain**: Operation within domain competency?
3. **Gate**: Required gate passed?
4. **Evidence**: Sufficient evidence provided?
5. **Rank**: Rank progression valid?
6. **Residuals**: Blocking residuals present?
7. **Trace**: Execution trace preserved?
8. **Forbidden Leap**: Layer skipping prevented?

**CPB Status Values**:
- `APPROVED`: All checks passed
- `IDENTITY_VIOLATION`: Identity not preserved
- `DOMAIN_VIOLATION`: Operation outside domain
- `GATE_VIOLATION`: Required gate not passed
- `EVIDENCE_INSUFFICIENT`: Evidence missing
- `RANK_VIOLATION`: Invalid rank progression
- `RESIDUAL_BLOCKING`: Blocking residuals present
- `TRACE_LOSS`: Trace not preserved
- `FORBIDDEN_LEAP`: Layer jump detected

### 4. AlgebraicDecisionCore

Main governance system that orchestrates all components.

**Decision Contract**:
```python
@dataclass(frozen=True)
class DecisionAudit:
    decision_id: str                    # Unique decision ID
    transition_id: str                  # Transition type
    from_layer: ExecutionLayer          # Source layer
    to_layer: ExecutionLayer            # Target layer
    input_identity: IdentityType        # Identity before
    output_identity: IdentityType       # Identity after
    domain: DomainType                  # Operating domain
    function: str                       # Function performed
    gate: str                           # Gate passed
    evidence: Tuple[str, ...]           # Evidence provided
    rank: Rank                          # Output rank
    residuals: Tuple[Residual, ...]     # Residuals
    trace: Tuple[str, ...]              # Execution trace
    cpb_status: CPBStatus               # CPB validation status
    allowed: bool                       # Decision result
    violations: Tuple[str, ...]         # Violations (if any)
```

## Usage Examples

### Basic Usage

```python
from dal_core.algebraic_decision_core import AlgebraicDecisionCore
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation import Rank, create_residual_set

# Initialize core
core = AlgebraicDecisionCore()

# Make a decision about U₇-C → U₈ transition
audit = core.decide_transition(
    transition_id="U7C_to_U8",
    from_layer=ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
    to_layer=ExecutionLayer.U8_ROOT_STEM,
    input_identity=IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
    output_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
    existing_identities=frozenset({
        IdentityType.RAW_SURFACE_IDENTITY,
        IdentityType.ORTHOGRAPHIC_IDENTITY,
        IdentityType.PHONETIC_IDENTITY,
        IdentityType.SYLLABIC_IDENTITY,
        IdentityType.BOUNDARY_IDENTITY,
        IdentityType.LAFZ_IDENTITY,
        IdentityType.PROTECTED_SURFACE_IDENTITY,
        IdentityType.PROTECTED_CORE_IDENTITY,
        IdentityType.LICENSED_ROOT_INPUT_IDENTITY
    }),
    domain=DomainType.ROOT_STEM_DOMAIN,
    attempted_determination="root_candidate_extraction",
    gate_name="RootInputGate",
    gate_passed=True,
    evidence=("license_permission", "marker_protection", "agreement_verified"),
    required_evidence=frozenset({"license_permission"}),
    input_rank=Rank.CANDIDATE,
    output_rank=Rank.CANDIDATE,  # Root in U₈ is candidate, NOT certificate
    residual_set=create_residual_set(frozenset()),
    trace=("U0", "U1", "U2p", "U2s", "U3", "U4", "U5", "U6", "U7A", "U7B", "U7C")
)

# Check decision
if audit.is_approved():
    print("✓ Transition approved")
    # Proceed with U₈ root candidate extraction
else:
    print("✗ Transition blocked")
    for violation in audit.violations:
        print(f"  - {violation}")
```

### Detecting Forbidden Leaps

```python
# Attempt forbidden leap: U₂s → U₈ (skips U₃, U₄, U₅, U₆, U₇)
audit = core.decide_transition(
    transition_id="FORBIDDEN_U2S_to_U8",
    from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
    to_layer=ExecutionLayer.U8_ROOT_STEM,
    input_identity=IdentityType.SYLLABIC_IDENTITY,
    output_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
    existing_identities=frozenset({IdentityType.SYLLABIC_IDENTITY}),
    domain=DomainType.ROOT_STEM_DOMAIN,
    attempted_determination="root_candidate_extraction",
    gate_name="RootGate",
    gate_passed=True,
    evidence=("syllable_analysis",),
    required_evidence=frozenset({"syllable_analysis"}),
    input_rank=Rank.CANDIDATE,
    output_rank=Rank.CANDIDATE,
    residual_set=create_residual_set(frozenset()),
    trace=("U0", "U1", "U2p", "U2s")
)

# Result: BLOCKED
assert audit.cpb_status == CPBStatus.FORBIDDEN_LEAP
assert not audit.is_approved()
```

### Detecting Domain Violations

```python
# Attempt to determine meaning in weight domain (forbidden)
audit = core.decide_transition(
    transition_id="U8_to_U9",
    from_layer=ExecutionLayer.U8_ROOT_STEM,
    to_layer=ExecutionLayer.U9_WEIGHT,
    input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
    output_identity=IdentityType.WEIGHT_IDENTITY,
    existing_identities=frozenset({...}),
    domain=DomainType.WEIGHT_DOMAIN,
    attempted_determination="meaning",  # FORBIDDEN in weight domain
    gate_name="WeightGate",
    gate_passed=True,
    evidence=("weight_pattern",),
    required_evidence=frozenset({"weight_pattern"}),
    input_rank=Rank.CANDIDATE,
    output_rank=Rank.HYPOTHESIS,
    residual_set=create_residual_set(frozenset()),
    trace=("...", "U8")
)

# Result: BLOCKED
assert audit.cpb_status == CPBStatus.DOMAIN_VIOLATION
assert "meaning" in str(audit.violations)
```

## Integration with Existing Layers

The AlgebraicDecisionCore does NOT replace existing layer CPB implementations (CPB₁, CPB₂s, CPB₆, CPB₈, etc.). Instead:

1. **Layer CPBs** remain responsible for layer-specific validation
2. **AlgebraicDecisionCore** provides ADDITIONAL governance coordination
3. Layers can consult the core for transition approval
4. Core tracks cross-layer identity and domain consistency

## Future Extensions

### TransitionRegistry (Planned)
Track all valid transitions with metadata:
- `U0_to_U1`, `U1_to_U2p`, ..., `U7C_to_U8`, `U8_to_U9`
- Required gates per transition
- Required evidence per transition
- Forbidden outputs per transition

### GateRegistry (Planned)
Catalog of all gates across layers:
- `UnicodeGate`, `GraphemeGate`, `PhoneticGate`, `SyllableGate`
- `BoundaryGate`, `TrueLafzGate`, `ClosedClassGate`
- `PreWeightContractGate`, `SurfaceGuardGate`, `ClauseAgreementGate`
- `RootInputGate`, `RootCandidateGate`, `WeightCandidateGate`

### EvidenceRegistry (Planned)
Classification of evidence types:
- `SurfaceEvidence`, `OrthographicEvidence`, `PhoneticEvidence`
- `LexiconEvidence`, `PatternEvidence`, `AgreementEvidence`
- `MarkerEvidence`, `ContextEvidence`, `RelationEvidence`

### AppendixSystem (Planned)
Extensible system for comprehensive Arabic coverage:
- `BrokenPluralAppendix` - جمع التكسير coverage
- `SourceFormAppendix` - مصدر coverage
- `AttributeFormAppendix` - صفة coverage
- `InflectionalMarkerAppendix` - علامات الإعراب coverage
- `ClauseAgreementAppendix` - اتفاق coverage
- `ClosedClassAppendix` - حروف وأدوات coverage
- `AmilRelationsAppendix` - عوامل coverage
- `WeakRootAppendix` - معتل coverage
- `ForeignProperJamidAppendix` - دخيل وعلم وجامد coverage

## Testing

Comprehensive test suite at `tests/dal_core/test_algebraic_decision_core.py`:

```bash
PYTHONPATH=src python -m pytest tests/dal_core/test_algebraic_decision_core.py -v
```

Tests cover:
- Identity registry and transitions
- Domain boundary enforcement
- CPB guardian verification
- Complete decision auditing
- Forbidden leap detection
- Domain violation detection
- Integration scenarios

## Key Principles

1. **No output without Decision** - Every transition must be audited
2. **No Decision without CPB approval** - Guardian must validate
3. **Identity preservation** - Input → Output identity tracked
4. **Domain boundaries** - No cross-domain violations
5. **Rank progression** - Only evidence-based elevation
6. **Residual tracking** - All residuals preserved
7. **Trace preservation** - Full execution trace maintained
8. **No forbidden leaps** - Layer progression enforced

## License

Part of the Arabic Linguistic Analysis Framework.

PR: ALGEBRAIC-DECISION-CORE
Created: 2026-05-26
