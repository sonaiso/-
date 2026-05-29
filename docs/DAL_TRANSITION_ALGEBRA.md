# Dal Transition Algebra (DTA)

**Complete Operational Mathematics for Arabic Morphological Analysis**

**Version**: 1.0.0
**Created**: 2026-05-29
**Status**: 📐 Formal Specification

---

## Supreme Law (القانون الأعلى)

```
لا انتقال بلا أصل
ولا أصل بلا وصف مؤثر
ولا قياس بلا علة جامعة
ولا علة مع فرق قادح
ولا قبول بلا حفظ هوية
ولا صعود بلا حد أدنى مكتمل
```

**Translation**:
- No transition without origin
- No origin without effective description
- No qiyās without shared cause
- No cause with invalidating difference
- No acceptance without identity preservation
- No ascent without minimal completeness

**Operational Consequence**:

```
Every transition f_i : S_i ⇀ S_{i+1} is a PARTIAL FUNCTION.
f_i operates ONLY when proof π_i is provided.
Without proof: f_i(x) = ⊥ (undefined/blocked)
```

---

## Table of Contents

1. [Dal Transition Algebra Definition](#dal-transition-algebra-definition)
2. [The Twelve Formal Spaces](#the-twelve-formal-spaces)
3. [Transition Functions](#transition-functions)
4. [Qiyās as Operational Function](#qiyas-as-operational-function)
5. [Node Proof Structure](#node-proof-structure)
6. [Acceptance and Rejection Predicates](#acceptance-and-rejection-predicates)
7. [Minimal Completeness Specifications](#minimal-completeness-specifications)
8. [Islamic Legal Concepts as Operators](#islamic-legal-concepts-as-operators)
9. [Path Tree and Branching](#path-tree-and-branching)
10. [Complete Worked Examples](#complete-worked-examples)
11. [Final Algebraic Formula](#final-algebraic-formula)

---

## Dal Transition Algebra Definition

### Formal System

The **Dal Transition Algebra (DTA)** is a tuple:

```
DTA = (S, F, Π, ⊢, ~, ∅_res, R)
```

Where:

- **S** = {S₀, S₁, ..., S₁₁} - Twelve formal spaces
- **F** = {f₀, f₁, ..., f₁₀} - Eleven transition functions
- **Π** = Set of all proofs (qiyās proofs, transition licenses, effective descriptions)
- **⊢** = Entailment relation (proof validates transition)
- **~** = Identity equivalence (preserves carrier identities)
- **∅_res** = Residual set (unresolved elements at each stage)
- **R** = Epistemic rank assignment (NOT assumption)

### Core Principle

```
∀i ∈ {0,1,...,10}, ∀x ∈ S_i:
    f_i(x) is defined ⟺ ∃π_i ∈ Π such that π_i ⊢ transition(x, f_i(x))
```

**Plain English**: A transition from space S_i to S_{i+1} operates if and only if there exists a proof π_i that licenses the transition.

---

## The Twelve Formal Spaces

### S₀: UnicodeRaw

**Definition**: Raw Unicode codepoint sequence

**Elements**:
```python
x ∈ S₀ ::= sequence of Unicode codepoints
```

**Example**:
```
"كاتب" = U+0643 U+0627 U+062A U+0628
```

**Properties**:
- No linguistic structure assumed
- Pure surface representation
- Source of all subsequent analysis

---

### S₁: CarrierSpace

**Definition**: Typed phonological carriers with preserved identities

**Elements**:
```python
c ∈ S₁ ::= Carrier(
    carrier_id: str,
    unicode_source: str,
    carrier_type: CarrierType,  # CONSONANT | VOWEL | SHADDA | SUKUN | etc.
    identity_id: str,  # Preserved throughout all transitions
    trace_id: str
)
```

**Transition from S₀**:
```
f₀: S₀ ⇀ S₁
f₀(x) defined ⟺ ∃ effective_description licensing each carrier extraction
```

**Example**:
```
"كاتب" → [
    Carrier(id="c1", unicode="U+0643", type=CONSONANT, identity="i1", ...),
    Carrier(id="c2", unicode="U+0627", type=LONG_VOWEL, identity="i2", ...),
    Carrier(id="c3", unicode="U+062A", type=CONSONANT, identity="i3", ...),
    Carrier(id="c4", unicode="U+0628", type=CONSONANT, identity="i4", ...)
]
```

**Identity Preservation Law**:
```
∀c ∈ S₁: identity_id(c) must be preserved in all subsequent transitions
If c.identity_id = "i1" at S₁, then all references to this carrier in S₂...S₁₁
must preserve "i1"
```

---

### S₂: EffectiveDescriptionSpace

**Definition**: Descriptions that license or block transitions (not mere labels)

**Elements**:
```python
d ∈ S₂ ::= EffectiveDescription(
    description_id: str,
    carrier_id: str,  # References carrier in S₁
    description_code: str,  # e.g., "CONSONANT_POTENTIAL_ROOT"
    licenses: tuple[str, ...],  # Transitions this description permits
    blocks: tuple[str, ...],  # Transitions this description forbids
    required_origin: Optional[str],  # For qiyās
    shared_cause: Optional[str],  # العلة الجامعة
    preserved_identity_ids: tuple[str, ...],
    trace_id: str
)
```

**Transition from S₁**:
```
f₁: S₁ ⇀ S₂
f₁(c) defined ⟺ ∃ effective_description_proof showing:
    - Description is operative (not merely descriptive)
    - Description has licensing/blocking power
    - Description preserves identity from c
```

**Example**:
```
Carrier("ك", CONSONANT) → EffectiveDescription(
    code="POTENTIAL_ROOT_CONSONANT",
    licenses=["ROOT_EXTRACTION", "SYLLABLE_ONSET"],
    blocks=["VOWEL_NUCLEUS"],
    preserved_identity_ids=("i1",)
)
```

---

### S₃: OperativeUnitSpace

**Definition**: Minimal licensed units that can participate in syllable formation

**Elements**:
```python
u ∈ S₃ ::= OperativeUnit(
    unit_id: str,
    carrier_ids: tuple[str, ...],  # References carriers in S₁
    unit_type: OperativeUnitType,  # ONSET | NUCLEUS | CODA | GEMINATE
    attachment_license: AttachmentLicense,  # Proof of licensed attachment
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],  # Unattached carriers
    trace_id: str
)
```

**Transition from S₂**:
```
f₂: S₂ ⇀ S₃
f₂(d) defined ⟺ ∃ attachment_license showing:
    - Units can legally combine
    - Combination preserves identities
    - No blocking descriptions violated
```

**Example**:
```
[EffectiveDescription("ك", CONSONANT), EffectiveDescription("َ", FATHA)]
→ OperativeUnit(
    type=CV_SYLLABLE_POTENTIAL,
    carrier_ids=("c1", "c2"),
    preserved_identity_ids=("i1", "i2"),
    attachment_license=AttachmentLicense(...)
)
```

---

### S₄: SyllableSpace

**Definition**: Licensed syllable structures (CV, CVC, CVV, etc.)

**Elements**:
```python
σ ∈ S₄ ::= Syllable(
    syllable_id: str,
    onset_unit_ids: tuple[str, ...],  # References units in S₃
    nucleus_unit_ids: tuple[str, ...],
    coda_unit_ids: tuple[str, ...],
    syllable_type: SyllableType,  # CV | CVC | CVV | CVVC | CCV | etc.
    syllable_license: SyllableLicense,  # Proof structure satisfies constraints
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_id: str
)
```

**Transition from S₃**:
```
f₃: S₃ ⇀ S₄
f₃(u) defined ⟺ ∃ syllable_license showing:
    - Structure matches Arabic syllable templates
    - No sonority violations
    - Identities preserved from operative units
```

**Example**:
```
OperativeUnit("ك", ONSET) + OperativeUnit("ا", NUCLEUS)
→ Syllable(
    type=CV,
    onset_unit_ids=("u1",),
    nucleus_unit_ids=("u2",),
    coda_unit_ids=(),
    preserved_identity_ids=("i1", "i2")
)
```

---

### S₅: SyllableCompositionSpace

**Definition**: Multi-syllable sequences with compositional licenses

**Elements**:
```python
comp ∈ S₅ ::= SyllableComposition(
    composition_id: str,
    syllable_ids: tuple[str, ...],  # References syllables in S₄
    composition_type: CompositionType,  # MONO | BI | TRI | QUAD
    composition_license: CompositionLicense,  # Proof of legal sequencing
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_id: str
)
```

**Transition from S₄**:
```
f₄: S₄ ⇀ S₅
f₄(σ) defined ⟺ ∃ composition_license showing:
    - Syllable sequence is permitted
    - No phonotactic violations
    - Identities preserved across syllable boundaries
```

**Example**:
```
[Syllable("كا", CV), Syllable("تب", CVC)]
→ SyllableComposition(
    type=BISYLLABIC,
    syllable_ids=("σ1", "σ2"),
    preserved_identity_ids=("i1", "i2", "i3", "i4")
)
```

---

### S₆: DalPathSpace

**Definition**: Branching morphological paths (12 competing classifications)

**Elements**:
```python
path ∈ S₆ ::= DalPath(
    path_id: str,
    composition_id: str,  # References composition in S₅
    path_type: DalPathType,  # One of 12 paths
    path_license: PathLicense,  # Qiyās proof for this path
    competing_paths: tuple[str, ...],  # Other viable paths
    path_rank: str,  # Epistemic rank of this path choice
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_id: str
)
```

**Twelve Path Types**:
```python
class DalPathType(Enum):
    MABNI = "mabnī"  # مبني - Built/Indeclinable
    MURAB = "muʿrab"  # معرب - Declinable
    JAMID = "jāmid"  # جامد - Stable/Non-derived
    MUSHTAQ = "mushtaq"  # مشتق - Derived
    PARTICLE = "ḥarf"  # حرف - Particle
    PRONOUN = "ḍamīr"  # ضمير - Pronoun
    VERB = "fiʿl"  # فعل - Verb
    AUGMENTED = "mazīd"  # مزيد - Augmented form
    CLITICIZED = "muttaṣil"  # متصل - Cliticized
    LOAN = "muʿarrab"  # معرّب - Loanword
    PROPER_NAME = "ʿalam"  # علم - Proper name
    DEFERRED_UNKNOWN = "mawqūf"  # موقوف - Deferred/Unknown
```

**Transition from S₅**:
```
f₅: S₅ ⇀ S₆
f₅(comp) defined ⟺ ∃ qiyās_proof showing:
    - Origin case exists
    - Branch shares effective cause with origin
    - No invalidating difference (fariq qādih)
    - Path selection preserves identities
```

**Example**:
```
SyllableComposition("كاتب", BISYLLABIC)
→ DalPath(
    type=MUSHTAQ,  # Derived (active participle pattern)
    path_license=QiyasProof(
        origin="كَتَبَ (root verb)",
        branch="كاتب (active participle)",
        shared_cause="فاعِل pattern application",
        invalidating_differences=()
    ),
    competing_paths=("JAMID", "PROPER_NAME"),
    path_rank="HYPOTHESIS"
)
```

---

### S₇: RootStemSpace

**Definition**: Identified root consonants and stem structure

**Elements**:
```python
root ∈ S₇ ::= RootStem(
    root_id: str,
    path_id: str,  # References path in S₆
    root_consonants: tuple[str, ...],  # (ك, ت, ب)
    root_type: RootType,  # TRILATERAL | QUADRILATERAL | etc.
    stem_type: StemType,  # SIMPLE | AUGMENTED | etc.
    root_license: RootLicense,  # Proof of root extraction validity
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],  # Non-root elements
    trace_id: str
)
```

**Transition from S₆**:
```
f₆: S₆ ⇀ S₇
f₆(path) defined ⟺ ∃ root_license showing:
    - Root extraction follows licensed pattern
    - Root consonants identified with preserved identities
    - Non-root elements marked as residuals
```

**Example**:
```
DalPath("كاتب", MUSHTAQ)
→ RootStem(
    root_consonants=("ك", "ت", "ب"),
    root_type=TRILATERAL,
    preserved_identity_ids=("i1", "i3", "i4"),
    residuals=("i2",)  # Long alif is pattern vowel, not root
)
```

---

### S₈: WeightSpace

**Definition**: Morphological pattern (وزن - wazn) identification

**Elements**:
```python
w ∈ S₈ ::= Weight(
    weight_id: str,
    root_id: str,  # References root in S₇
    pattern: str,  # فاعِل, مَفعول, etc.
    pattern_type: PatternType,
    weight_license: WeightLicense,  # Proof pattern applies to this root
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_id: str
)
```

**Transition from S₇**:
```
f₇: S₇ ⇀ S₈
f₇(root) defined ⟺ ∃ weight_license showing:
    - Pattern legally applies to this root type
    - Pattern-root mapping preserves identities
    - Pattern choice licensed by qiyās
```

**Example**:
```
RootStem(ك-ت-ب, TRILATERAL)
→ Weight(
    pattern="فاعِل",
    pattern_type=ACTIVE_PARTICIPLE,
    weight_license=WeightLicense(
        origin="known فاعِل instances",
        shared_cause="agent semantic role",
        ...
    )
)
```

---

### S₉: MabniMuʿrabSpace

**Definition**: Built (indeclinable) vs. Declinable distinction

**Elements**:
```python
mm ∈ S₉ ::= MabniMurab(
    id: str,
    weight_id: str,  # References weight in S₈
    category: MabniMurabCategory,  # MABNI | MURAB
    declension_license: DeclensionLicense,
    case_potential: Optional[CasePotential],  # Only for muʿrab
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_id: str
)
```

**Transition from S₈**:
```
f₈: S₈ ⇀ S₉
f₈(w) defined ⟺ ∃ declension_license showing:
    - Mabnī/muʿrab status determined by pattern + context
    - Case potential correctly assigned
```

**Example**:
```
Weight("كاتب", فاعِل)
→ MabniMurab(
    category=MURAB,  # Declinable
    case_potential=CasePotential(NOM, ACC, GEN),
    declension_license=DeclensionLicense(...)
)
```

---

### S₁₀: JamidMushtaqSpace

**Definition**: Stable (non-derived) vs. Derived distinction

**Elements**:
```python
jm ∈ S₁₀ ::= JamidMushtaq(
    id: str,
    mabni_murab_id: str,  # References S₉
    category: JamidMushtaqCategory,  # JAMID | MUSHTAQ
    derivation_license: DerivationLicense,
    source_verb: Optional[str],  # Only for mushtaq
    preserved_identity_ids: tuple[str, ...],
    residuals: tuple[str, ...],
    trace_id: str
)
```

**Transition from S₉**:
```
f₉: S₉ ⇀ S₁₀
f₉(mm) defined ⟺ ∃ derivation_license showing:
    - Jāmid/mushtaq status determined
    - If mushtaq: source verb identified
```

**Example**:
```
MabniMurab("كاتب", MURAB)
→ JamidMushtaq(
    category=MUSHTAQ,  # Derived
    source_verb="كَتَبَ",
    derivation_license=DerivationLicense(
        origin="كَتَبَ",
        derived_pattern="فاعِل",
        shared_cause="agent derivation"
    )
)
```

---

### S₁₁: LafzMufradSpace

**Definition**: Licensed single word (الكلمة المفردة)

**Elements**:
```python
lafz ∈ S₁₁ ::= LafzMufrad(
    word_id: str,
    surface: str,  # Surface form
    jamid_mushtaq_id: str,  # References S₁₀

    # Complete proof chain
    acceptance_proof: LafzMufradAcceptanceProof,

    # Preserved elements
    preserved_carrier_ids: tuple[str, ...],
    preserved_identity_ids: tuple[str, ...],

    # Component structure
    prefix_units: tuple[str, ...],
    stem_units: tuple[str, ...],
    suffix_units: tuple[str, ...],
    clitic_units: tuple[str, ...],

    # Residuals and rank
    residuals: tuple[str, ...],
    rank: str,  # Epistemic rank
    trace_id: str,

    # FORBIDDEN outputs
    produces_meaning: bool = False,
    produces_ifadah: bool = False,
    produces_hukm: bool = False
)
```

**Transition from S₁₀**:
```
f₁₀: S₁₀ ⇀ S₁₁
f₁₀(jm) defined ⟺ ∃ acceptance_proof satisfying ALL criteria:
    1. Identity preservation
    2. Minimal completeness
    3. No blocking differences
    4. Trace preservation
    5. Rank assignment (not assumption)
    6. Residual documentation
    7. No meaning/ifādah/hukm production
```

**Example**:
```
JamidMushtaq("كاتب", MUSHTAQ)
→ LafzMufrad(
    surface="كاتب",
    acceptance_proof=LafzMufradAcceptanceProof(...),
    preserved_carrier_ids=("c1", "c2", "c3", "c4"),
    preserved_identity_ids=("i1", "i2", "i3", "i4"),
    stem_units=("كاتب",),
    residuals=(),
    rank="HYPOTHESIS",
    produces_meaning=False,
    produces_ifadah=False,
    produces_hukm=False
)
```

---

## Transition Functions

### General Transition Schema

Every transition function follows this pattern:

```python
def f_i(x: S_i, proof: Proof_i) -> Optional[S_{i+1}]:
    """
    Transition from space S_i to S_{i+1}.

    Args:
        x: Element in source space S_i
        proof: Transition license/proof

    Returns:
        Element in target space S_{i+1} if proof valid
        None (⊥) if proof invalid or blocking condition met
    """
    # 1. Check proof validity
    if not validate_proof(proof):
        return None  # ⊥ - Undefined

    # 2. Check effective descriptions (licensing/blocking)
    if has_blocking_description(x, proof):
        return None  # ⊥ - Blocked

    # 3. Check identity preservation
    if not preserves_identities(x, proof):
        return None  # ⊥ - Identity loss

    # 4. Check minimal completeness
    if not meets_minimal_requirements(x, proof):
        return None  # ⊥ - Incomplete

    # 5. Construct target element
    y = construct_target(x, proof)

    # 6. Document residuals
    y.residuals = extract_residuals(x, y)

    # 7. Assign rank (not assume)
    y.rank = assign_epistemic_rank(proof)

    # 8. Preserve trace
    y.trace_id = extend_trace(x.trace_id, proof.proof_id)

    # 9. Verify no forbidden outputs
    assert y.produces_meaning == False
    assert y.produces_ifadah == False
    assert y.produces_hukm == False

    return y
```

---

### Specific Transitions

#### f₀: UnicodeRaw → CarrierSpace

```python
def f_0(raw: str, carrier_extraction_proof: CarrierExtractionProof) -> Optional[List[Carrier]]:
    """Extract carriers from Unicode with identity assignment."""
    carriers = []
    for codepoint in raw:
        # Require effective description for each carrier
        desc = carrier_extraction_proof.get_description(codepoint)
        if desc is None:
            return None  # ⊥ - No effective description

        # Create carrier with unique identity
        carrier = Carrier(
            carrier_id=generate_id(),
            unicode_source=codepoint,
            carrier_type=desc.carrier_type,
            identity_id=generate_identity_id(),  # CRITICAL: Unique identity
            trace_id=generate_trace_id()
        )
        carriers.append(carrier)

    return carriers
```

#### f₅: SyllableComposition → DalPath (Critical Branching)

```python
def f_5(comp: SyllableComposition, qiyas_proof: QiyasProof) -> Optional[DalPath]:
    """
    Branch into one of 12 morphological paths.
    REQUIRES qiyās proof.
    """
    # 1. Validate qiyās proof structure
    if not validate_qiyas_proof(qiyas_proof):
        return None

    # 2. Check for invalidating differences
    if qiyas_proof.blocking_differences:
        return None  # Fariq qādih blocks transition

    # 3. Extract competing paths
    competing_paths = extract_competing_paths(comp, qiyas_proof)

    # 4. Select path based on strongest proof
    selected_path_type = qiyas_proof.branch_path_type

    # 5. Construct path with preserved identities
    path = DalPath(
        path_id=generate_id(),
        composition_id=comp.composition_id,
        path_type=selected_path_type,
        path_license=qiyas_proof,
        competing_paths=tuple(p.path_type for p in competing_paths),
        path_rank=assign_rank_from_proof(qiyas_proof),
        preserved_identity_ids=comp.preserved_identity_ids,
        residuals=comp.residuals,
        trace_id=extend_trace(comp.trace_id, qiyas_proof.proof_id)
    )

    return path
```

#### f₁₀: JamidMushtaq → LafzMufrad (Final Acceptance)

```python
def f_10(jm: JamidMushtaq, acceptance_proof: LafzMufradAcceptanceProof) -> Optional[LafzMufrad]:
    """
    Final acceptance as single word.
    STRICTEST requirements.
    """
    # 1. Verify complete proof chain
    if not verify_complete_proof_chain(acceptance_proof):
        return None

    # 2. Verify ALL identities preserved from S₀
    if not all_identities_preserved(acceptance_proof):
        return None

    # 3. Verify minimal completeness met
    if not meets_mufrad_minimal_completeness(acceptance_proof):
        return None

    # 4. Verify no blocking differences in entire chain
    if has_any_blocking_difference(acceptance_proof):
        return None

    # 5. Construct single word
    lafz = LafzMufrad(
        word_id=generate_id(),
        surface=reconstruct_surface(jm),
        jamid_mushtaq_id=jm.id,
        acceptance_proof=acceptance_proof,
        preserved_carrier_ids=acceptance_proof.carrier_ids,
        preserved_identity_ids=acceptance_proof.identity_ids,
        prefix_units=acceptance_proof.prefix_units,
        stem_units=acceptance_proof.stem_units,
        suffix_units=acceptance_proof.suffix_units,
        clitic_units=acceptance_proof.clitic_units,
        residuals=acceptance_proof.residuals,
        rank=acceptance_proof.rank,
        trace_id=extend_trace(jm.trace_id, acceptance_proof.proof_id),
        produces_meaning=False,  # FORBIDDEN
        produces_ifadah=False,   # FORBIDDEN
        produces_hukm=False      # FORBIDDEN
    )

    return lafz
```

---

## Qiyās as Operational Function

### Mathematical Definition

Qiyās (قياس - analogical reasoning) is NOT a heuristic or pattern-matching. It is an **operational function** with formal proof requirements.

```
Qiyās: (Origin × Branch × Cause × Differences) ⇀ {Accept, Reject, Defer}
```

### Qiyās Proof Structure

```python
@dataclass(frozen=True)
class QiyasProof:
    """
    القياس - Analogical Reasoning Proof

    Components (أركان القياس):
    1. الأصل (Origin) - Known licensed case
    2. الفرع (Branch) - New case being evaluated
    3. العلة الجامعة (Shared Cause) - Common effective property
    4. الحكم (Ruling) - Transition license from origin
    """
    proof_id: str

    # Origin case (الأصل)
    origin_id: str
    origin_surface: str
    origin_hukm: str  # Transition license of origin

    # Branch case (الفرع)
    branch_id: str
    branch_surface: str
    branch_path_type: DalPathType

    # Shared cause (العلة الجامعة)
    effective_description_id: str
    shared_cause: str
    cause_applies_to_origin: bool
    cause_applies_to_branch: bool

    # Invalidating differences (الفرق القادح)
    invalidating_differences: tuple[str, ...]

    # Blocking differences (الفرق المانع)
    blocking_differences: tuple[str, ...]

    # Evidence
    evidence: tuple[str, ...]

    # Acceptance status
    accepted: bool
    rejection_reason: Optional[str]

    # Trace
    trace_id: str
```

### Qiyās Validation Function

```python
def validate_qiyas(proof: QiyasProof) -> bool:
    """
    Validate qiyās proof according to Islamic legal methodology.

    Returns True iff:
    1. Origin exists and is licensed
    2. Shared cause identified and applies to both
    3. No invalidating difference exists
    4. No blocking difference exists
    """
    # 1. Origin must exist in registry
    if not origin_exists(proof.origin_id):
        proof.rejection_reason = "NO_ORIGIN"
        return False

    # 2. Origin must have licensed transition (hukm)
    if not has_license(proof.origin_id, proof.origin_hukm):
        proof.rejection_reason = "ORIGIN_UNLICENSED"
        return False

    # 3. Shared cause must apply to BOTH origin and branch
    if not (proof.cause_applies_to_origin and proof.cause_applies_to_branch):
        proof.rejection_reason = "CAUSE_NOT_SHARED"
        return False

    # 4. Check for invalidating differences (الفرق القادح)
    if proof.invalidating_differences:
        proof.rejection_reason = f"INVALIDATING_DIFF: {proof.invalidating_differences[0]}"
        return False

    # 5. Check for blocking differences (الفرق المانع)
    if proof.blocking_differences:
        proof.rejection_reason = f"BLOCKING_DIFF: {proof.blocking_differences[0]}"
        return False

    return True
```

### Qiyās Examples

#### Example 1: كاتب (kātib - writer) as فاعِل (active participle)

```python
qiyas_katib = QiyasProof(
    proof_id="qiyas_001",

    # Origin: Known active participle ضارب (ḍārib - striker)
    origin_id="origin_darib",
    origin_surface="ضارب",
    origin_hukm="ACTIVE_PARTICIPLE_LICENSE",

    # Branch: New case كاتب
    branch_id="branch_katib",
    branch_surface="كاتب",
    branch_path_type=DalPathType.MUSHTAQ,

    # Shared cause: فاعِل pattern application
    effective_description_id="ed_fail_pattern",
    shared_cause="فاعِل pattern: C₁āC₂iC₃ with agent semantic role",
    cause_applies_to_origin=True,  # ضارب matches فاعِل
    cause_applies_to_branch=True,   # كاتب matches فاعِل

    # No invalidating differences
    invalidating_differences=(),
    blocking_differences=(),

    evidence=(
        "Root ض-ر-ب trilateral, root ك-ت-ب trilateral",
        "Pattern C₁āC₂iC₃ matches both",
        "Both derive from form I verbs",
        "Both express agent semantic role"
    ),

    accepted=True,
    rejection_reason=None,
    trace_id="trace_qiyas_001"
)
```

#### Example 2: مِنْ (min - from) as Particle

```python
qiyas_min = QiyasProof(
    proof_id="qiyas_002",

    # Origin: Known particle إلى (ilā - to)
    origin_id="origin_ila",
    origin_surface="إلى",
    origin_hukm="PARTICLE_LICENSE",

    # Branch: مِنْ
    branch_id="branch_min",
    branch_surface="مِنْ",
    branch_path_type=DalPathType.PARTICLE,

    # Shared cause: Monosyllabic particle pattern
    effective_description_id="ed_particle_mono",
    shared_cause="Monosyllabic preposition expressing spatial relation",
    cause_applies_to_origin=True,  # إلى is monosyllabic particle
    cause_applies_to_branch=True,   # مِنْ is monosyllabic particle

    # No invalidating differences
    invalidating_differences=(),
    blocking_differences=(),

    evidence=(
        "Both monosyllabic",
        "Both prepositions (حروف الجر)",
        "Both mabnī (indeclinable)",
        "Both govern genitive case"
    ),

    accepted=True,
    rejection_reason=None,
    trace_id="trace_qiyas_002"
)
```

---

## Node Proof Structure

Every node in the transition tree carries a **node proof** documenting the transition that created it.

### NodeProof Definition

```python
@dataclass(frozen=True)
class NodeProof:
    """
    Proof structure for every tree node.
    Documents the transition that produced this node.
    """
    node_id: str
    node_space: str  # S₀, S₁, ..., S₁₁

    # Transition that created this node
    source_node_id: Optional[str]  # None for S₀ (root)
    transition_function: str  # f₀, f₁, ..., f₁₀
    transition_proof_id: str

    # Preservation evidence
    preserved_identity_ids: tuple[str, ...]
    identity_preservation_evidence: tuple[str, ...]

    # Residuals at this node
    residuals: tuple[str, ...]
    residual_reasons: tuple[str, ...]

    # Rank
    rank: str  # OBSERVATION | HYPOTHESIS | CONFIRMED | etc.
    rank_justification: str

    # Trace
    trace_id: str
    trace_chain: tuple[str, ...]  # Full chain from S₀

    # Constitutional compliance
    produces_meaning: bool = False
    produces_ifadah: bool = False
    produces_hukm: bool = False
```

### Tree Structure with Proofs

```
                           S₀: UnicodeRaw
                                 |
                              [f₀, π₀]
                                 ↓
                           S₁: Carriers
                          [NodeProof₁]
                                 |
                              [f₁, π₁]
                                 ↓
                    S₂: EffectiveDescriptions
                          [NodeProof₂]
                                 |
                              [f₂, π₂]
                                 ↓
                       S₃: OperativeUnits
                          [NodeProof₃]
                                 |
                              [f₃, π₃]
                                 ↓
                          S₄: Syllables
                          [NodeProof₄]
                                 |
                              [f₄, π₄]
                                 ↓
                    S₅: SyllableComposition
                          [NodeProof₅]
                                 |
                              [f₅, π₅_qiyas]
                                 ↓
                           S₆: DalPath
                          [NodeProof₆]
                        /       |       \
                   [Mabnī]  [Muʿrab] [Mushtaq] ...
                      |        |         |
                   [f₆,π₆]  [f₆,π₆]   [f₆,π₆]
                      ↓        ↓         ↓
                   S₇: RootStem (different for each path)
                          [NodeProof₇]
                                 |
                              [f₇, π₇]
                                 ↓
                           S₈: Weight
                          [NodeProof₈]
                                 |
                              [f₈, π₈]
                                 ↓
                        S₉: MabniMurab
                          [NodeProof₉]
                                 |
                              [f₉, π₉]
                                 ↓
                       S₁₀: JamidMushtaq
                          [NodeProof₁₀]
                                 |
                              [f₁₀, π₁₀]
                                 ↓
                        S₁₁: LafzMufrad
                          [NodeProof₁₁]
                        [ACCEPTANCE PROOF]
```

---

## Acceptance and Rejection Predicates

### Acceptance Predicate (ACCEPT)

```python
def accept_as_lafz_mufrad(proof: LafzMufradAcceptanceProof) -> bool:
    """
    Accept as single word iff ALL conditions met.
    """
    return all([
        # 1. Identity preservation
        all_identities_preserved_from_s0(proof),

        # 2. Complete proof chain
        complete_proof_chain_exists(proof),

        # 3. Minimal completeness
        meets_minimal_completeness_s11(proof),

        # 4. No blocking differences
        not has_blocking_difference(proof),

        # 5. No invalidating differences
        not has_invalidating_difference(proof),

        # 6. Identity-neutral transformations
        all_transformations_identity_neutral(proof),

        # 7. Trace preserved
        trace_preserved_from_s0(proof),

        # 8. Rank assigned (not assumed)
        rank_properly_assigned(proof),

        # 9. Residuals documented
        residuals_properly_documented(proof),

        # 10. No forbidden outputs
        not proof.produces_meaning,
        not proof.produces_ifadah,
        not proof.produces_hukm
    ])
```

### Rejection Types

```python
class RejectionType(Enum):
    """Why a transition was rejected (⊥)."""

    # Proof failures
    NO_PROOF = "no_proof_provided"
    INVALID_PROOF = "proof_invalid"
    NO_ORIGIN = "qiyas_no_origin"
    UNLICENSED_ORIGIN = "qiyas_origin_not_licensed"

    # Qiyās failures
    NO_SHARED_CAUSE = "no_shared_cause"
    INVALIDATING_DIFFERENCE = "fariq_qadih"
    BLOCKING_DIFFERENCE = "fariq_mani"

    # Identity failures
    IDENTITY_LOSS = "identity_not_preserved"
    IDENTITY_VIOLATION = "identity_transformation_not_neutral"

    # Completeness failures
    INCOMPLETE_MINIMUM = "minimal_completeness_not_met"
    MISSING_REQUIRED_COMPONENT = "required_component_missing"

    # Description failures
    BLOCKING_DESCRIPTION = "effective_description_blocks"
    NO_LICENSING_DESCRIPTION = "no_licensing_description"

    # Competitive failures
    STRONGER_COMPETING_PATH = "stronger_path_exists"
    AMBIGUOUS_PATHS = "cannot_disambiguate_paths"

    # Constitutional failures
    FORBIDDEN_OUTPUT_MEANING = "produces_meaning"
    FORBIDDEN_OUTPUT_IFADAH = "produces_ifadah"
    FORBIDDEN_OUTPUT_HUKM = "produces_hukm"
```

### Deferred Status

```python
class DeferredReason(Enum):
    """Why a decision is deferred (موقوف)."""

    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    COMPETING_PROOFS = "multiple_valid_proofs"
    AWAITING_COMPOSITION = "needs_compositional_context"
    UNKNOWN_ORIGIN = "origin_not_in_registry"
    AMBIGUOUS_CAUSE = "shared_cause_ambiguous"
```

---

## Minimal Completeness Specifications

Each space S_i has **minimal completeness requirements**. Transition to S_{i+1} is BLOCKED unless these are met.

### S₁: CarrierSpace

**Minimum Requirements**:
```python
def minimal_completeness_s1(carriers: List[Carrier]) -> bool:
    """Each carrier must have identity and type."""
    return all(
        c.carrier_id and
        c.identity_id and
        c.carrier_type and
        c.unicode_source
        for c in carriers
    )
```

### S₂: EffectiveDescriptionSpace

**Minimum Requirements**:
```python
def minimal_completeness_s2(desc: EffectiveDescription) -> bool:
    """Description must license or block at least one transition."""
    return (
        desc.description_code and
        (len(desc.licenses) > 0 or len(desc.blocks) > 0) and
        desc.preserved_identity_ids
    )
```

### S₃: OperativeUnitSpace

**Minimum Requirements**:
```python
def minimal_completeness_s3(unit: OperativeUnit) -> bool:
    """Unit must have type and attachment license."""
    return (
        unit.unit_type and
        unit.attachment_license and
        len(unit.carrier_ids) > 0 and
        unit.preserved_identity_ids
    )
```

### S₄: SyllableSpace

**Minimum Requirements**:
```python
def minimal_completeness_s4(syll: Syllable) -> bool:
    """Syllable must have nucleus (at minimum)."""
    return (
        len(syll.nucleus_unit_ids) > 0 and  # CRITICAL: Nucleus required
        syll.syllable_type and
        syll.syllable_license and
        syll.preserved_identity_ids
    )
```

### S₅: SyllableCompositionSpace

**Minimum Requirements**:
```python
def minimal_completeness_s5(comp: SyllableComposition) -> bool:
    """Composition must have at least one syllable."""
    return (
        len(comp.syllable_ids) > 0 and
        comp.composition_type and
        comp.composition_license and
        comp.preserved_identity_ids
    )
```

### S₆: DalPathSpace

**Minimum Requirements**:
```python
def minimal_completeness_s6(path: DalPath) -> bool:
    """Path must have qiyās proof."""
    return (
        path.path_type and
        path.path_license and  # CRITICAL: Qiyās proof required
        isinstance(path.path_license, QiyasProof) and
        path.path_license.accepted and
        path.preserved_identity_ids
    )
```

### S₇: RootStemSpace

**Minimum Requirements**:
```python
def minimal_completeness_s7(root: RootStem) -> bool:
    """Root must have consonants and type."""
    return (
        len(root.root_consonants) >= 2 and  # At least bilateral
        root.root_type and
        root.root_license and
        root.preserved_identity_ids
    )
```

### S₈: WeightSpace

**Minimum Requirements**:
```python
def minimal_completeness_s8(weight: Weight) -> bool:
    """Weight must have pattern and license."""
    return (
        weight.pattern and
        weight.pattern_type and
        weight.weight_license and
        weight.preserved_identity_ids
    )
```

### S₉: MabniMuʿrabSpace

**Minimum Requirements**:
```python
def minimal_completeness_s9(mm: MabniMurab) -> bool:
    """Must declare mabnī or muʿrab status."""
    return (
        mm.category in (MabniMurabCategory.MABNI, MabniMurabCategory.MURAB) and
        mm.declension_license and
        mm.preserved_identity_ids
    )
```

### S₁₀: JamidMushtaqSpace

**Minimum Requirements**:
```python
def minimal_completeness_s10(jm: JamidMushtaq) -> bool:
    """Must declare jāmid or mushtaq status."""
    return (
        jm.category in (JamidMushtaqCategory.JAMID, JamidMushtaqCategory.MUSHTAQ) and
        jm.derivation_license and
        jm.preserved_identity_ids
    )
```

### S₁₁: LafzMufradSpace (STRICTEST)

**Minimum Requirements**:
```python
def minimal_completeness_s11(lafz: LafzMufrad) -> bool:
    """
    Single word must meet ALL constitutional requirements.
    This is the STRICTEST completeness check.
    """
    return all([
        # Surface form
        lafz.surface,

        # Complete proof
        lafz.acceptance_proof,
        isinstance(lafz.acceptance_proof, LafzMufradAcceptanceProof),

        # Preserved identities (ALL from S₀)
        len(lafz.preserved_identity_ids) > 0,
        all_identities_from_s0(lafz.preserved_identity_ids),

        # Component structure (at least stem)
        len(lafz.stem_units) > 0,

        # Residuals documented (may be empty)
        lafz.residuals is not None,

        # Rank assigned
        lafz.rank,
        lafz.rank != "ASSUMED",  # FORBIDDEN

        # Trace preserved
        lafz.trace_id,
        trace_goes_back_to_s0(lafz.trace_id),

        # Forbidden outputs = False
        lafz.produces_meaning == False,
        lafz.produces_ifadah == False,
        lafz.produces_hukm == False
    ])
```

---

## Islamic Legal Concepts as Operators

The Dal Transition Algebra integrates **wad'ī rulings** (الأحكام الوضعية) from Islamic legal theory as operational logic.

### Wad'ī Rulings (الأحكام الوضعية)

These are NOT merely descriptive categories, but **operational constraints** in the transition algebra.

#### 1. Sabab (السبب - Cause)

**Definition**: Condition that triggers a ruling/transition.

**Operator**:
```python
def sabab(condition: bool, transition: Callable) -> Optional[Result]:
    """
    Cause: If condition met, transition MAY proceed (not automatic).
    """
    if condition:
        return transition()  # Transition enabled
    else:
        return None  # ⊥ - Blocked
```

**Example**:
```python
# Sabab: Trilateral root is CAUSE for فاعِل pattern application
if root.root_type == RootType.TRILATERAL:
    # فاعِل pattern transition enabled
    apply_fail_pattern(root)
```

#### 2. Shart (الشرط - Condition)

**Definition**: Necessary condition for validity (not sufficient).

**Operator**:
```python
def shart(necessary_conditions: List[bool], transition: Callable) -> Optional[Result]:
    """
    Condition: ALL conditions must be met, but meeting them doesn't guarantee transition.
    """
    if all(necessary_conditions):
        # Conditions met, but still need proof
        return transition()
    else:
        return None  # ⊥ - Condition not met
```

**Example**:
```python
# Shart: Identity preservation is CONDITION for any transition
conditions = [
    all_identities_preserved(x),
    minimal_completeness_met(x),
    no_blocking_description(x)
]
if all(conditions):
    # Conditions met, proceed with proof check
    pass
```

#### 3. Māniʿ (المانع - Impediment)

**Definition**: Blocking condition that prevents transition even if cause and conditions met.

**Operator**:
```python
def mani(impediments: List[bool], transition: Callable) -> Optional[Result]:
    """
    Impediment: ANY impediment blocks transition.
    """
    if any(impediments):
        return None  # ⊥ - Blocked by impediment
    else:
        return transition()
```

**Example**:
```python
# Māniʿ: Invalidating difference blocks qiyās
impediments = [
    proof.invalidating_differences,
    proof.blocking_differences,
    identity_loss_detected(x)
]
if any(impediments):
    return None  # Transition blocked
```

#### 4. Ṣiḥḥah & Buṭlān (الصحة والبطلان - Validity & Nullity)

**Definition**: Valid transition vs. null transition.

**Operator**:
```python
def validate_transition(x: S_i, proof: Proof, f: Callable) -> TransitionStatus:
    """
    Validity: Transition is ṣaḥīḥ (valid) iff proof complete and no impediments.
    Otherwise: bāṭil (null/void).
    """
    if validate_proof(proof) and not has_impediments(x, proof):
        result = f(x, proof)
        return TransitionStatus.SAHIH  # Valid
    else:
        return TransitionStatus.BATIL  # Null/void
```

**Example**:
```python
# Ṣiḥḥah: Qiyās is valid (صحيح) iff all components present
if (proof.origin_id and
    proof.shared_cause and
    not proof.invalidating_differences):
    status = TransitionStatus.SAHIH
else:
    status = TransitionStatus.BATIL
```

#### 5. ʿAzīmah & Rukhṣah (العزيمة والرخصة - Original Ruling & Concession)

**Definition**: Standard path vs. exceptional path.

**Operator**:
```python
def apply_ruling(x: S_i, exception_conditions: List[bool]) -> PathType:
    """
    Original ruling (ʿazīmah) applies by default.
    Concession (rukhṣah) applies only under specific conditions.
    """
    if any(exception_conditions):
        return PathType.RUKHSAH  # Exceptional path
    else:
        return PathType.AZIMAH  # Standard path
```

**Example**:
```python
# ʿAzīmah: Standard derivation from root
# Rukhṣah: Loanword path (معرّب) - exceptional
if is_loanword(surface):
    path_type = DalPathType.LOAN  # Rukhṣah
else:
    path_type = DalPathType.MUSHTAQ  # ʿAzīmah
```

---

## Path Tree and Branching

### Branching at S₆: DalPathSpace

After syllable composition (S₅), the tree **branches into 12 competing paths**. Each requires separate qiyās proof.

```
                    S₅: SyllableComposition
                              |
                         [f₅, π₅_qiyas]
                              |
        ┌─────────────────────┼─────────────────────┐
        |                     |                     |
    Path 1: Mabnī         Path 2: Muʿrab       Path 3: Jāmid
   [QiyasProof₁]         [QiyasProof₂]        [QiyasProof₃]
        |                     |                     |
        ↓                     ↓                     ↓
    S₇: RootStem          S₇: RootStem         S₇: RootStem
    (mabnī)               (muʿrab)             (jāmid)
        |                     |                     |
        ↓                     ↓                     ↓
    [Different proofs required for each branch]
        |                     |                     |
        ↓                     ↓                     ↓
    S₁₁: LafzMufrad       S₁₁: LafzMufrad      S₁₁: LafzMufrad
    (mabnī)               (muʿrab)             (jāmid)
```

### Path Selection Logic

```python
def select_path(comp: SyllableComposition, qiyas_proofs: List[QiyasProof]) -> DalPath:
    """
    Select path with strongest qiyās proof.
    Multiple paths may be valid (competing hypotheses).
    """
    valid_paths = []

    for proof in qiyas_proofs:
        if validate_qiyas(proof):
            path = construct_path(comp, proof)
            valid_paths.append(path)

    if len(valid_paths) == 0:
        # No valid path - defer
        return DalPath(
            path_type=DalPathType.DEFERRED_UNKNOWN,
            path_rank="DEFERRED",
            rejection_reason="NO_VALID_QIYAS"
        )

    elif len(valid_paths) == 1:
        # Single valid path
        return valid_paths[0]

    else:
        # Multiple valid paths - rank by evidence strength
        ranked_paths = rank_by_evidence_strength(valid_paths)
        selected = ranked_paths[0]
        selected.competing_paths = tuple(p.path_id for p in ranked_paths[1:])
        selected.path_rank = "HYPOTHESIS_COMPETING"
        return selected
```

### Twelve Paths Detailed

1. **Mabnī (مبني)**: Indeclinable/built
   - Examples: أمْسِ (yesterday), حَيْثُ (where)
   - Qiyās origin: Known mabnī particles

2. **Muʿrab (معرب)**: Declinable
   - Examples: كِتَابٌ (book), رَجُلٌ (man)
   - Qiyās origin: Known tripartite nouns

3. **Jāmid (جامد)**: Stable/non-derived
   - Examples: شَمْس (sun), قَمَر (moon)
   - Qiyās origin: Known primitive nouns

4. **Mushtaq (مشتق)**: Derived
   - Examples: كاتب (writer), مَكْتُوب (written)
   - Qiyās origin: Known derived forms

5. **Particle (حرف)**: Function word
   - Examples: مِنْ (from), إلى (to), في (in)
   - Qiyās origin: Known particles

6. **Pronoun (ضمير)**: Pronominal
   - Examples: هو (he), أنتَ (you), نحن (we)
   - Qiyās origin: Known pronouns

7. **Verb (فعل)**: Verbal
   - Examples: كَتَبَ (wrote), يَكْتُبُ (writes)
   - Qiyās origin: Known verb patterns

8. **Augmented (مزيد)**: Augmented forms (forms II-X)
   - Examples: كَتَّبَ (form II), تَكَاتَبَ (form VI)
   - Qiyās origin: Known augmentation patterns

9. **Cliticized (متصل)**: With clitics
   - Examples: بِكَ (with you), لَهُمْ (for them)
   - Qiyās origin: Known clitic patterns

10. **Loan (معرّب)**: Loanword
    - Examples: تِلِفُون (telephone), كُمْبِيُوتَر (computer)
    - Qiyās origin: Known loans (exceptional path - rukhṣah)

11. **Proper Name (علم)**: Proper noun
    - Examples: مُحَمَّد (Muhammad), القاهرة (Cairo)
    - Qiyās origin: Known proper name patterns

12. **Deferred/Unknown (موقوف)**: Cannot decide yet
    - Insufficient evidence
    - Awaiting compositional context
    - Qiyās origin unclear

---

## Complete Worked Examples

### Example 1: كاتب (kātib - writer)

**Input**: كاتب (U+0643 U+0627 U+062A U+0628)

#### S₀ → S₁: UnicodeRaw → CarrierSpace

```python
f_0("كاتب", carrier_extraction_proof) → [
    Carrier(id="c1", unicode="U+0643", type=CONSONANT, identity="i1"),  # ك
    Carrier(id="c2", unicode="U+0627", type=LONG_VOWEL, identity="i2"),  # ا
    Carrier(id="c3", unicode="U+062A", type=CONSONANT, identity="i3"),  # ت
    Carrier(id="c4", unicode="U+0628", type=CONSONANT, identity="i4")   # ب
]
```

**Proof**: Each codepoint has effective description licensing carrier extraction.

#### S₁ → S₂: Carriers → EffectiveDescriptions

```python
f_1([c1, c2, c3, c4], description_proofs) → [
    EffectiveDescription(
        carrier_id="c1",
        code="POTENTIAL_ROOT_CONSONANT",
        licenses=["ROOT_EXTRACTION", "SYLLABLE_ONSET"],
        preserved_identity_ids=("i1",)
    ),
    EffectiveDescription(
        carrier_id="c2",
        code="LONG_VOWEL_PATTERN_COMPONENT",
        licenses=["SYLLABLE_NUCLEUS", "PATTERN_VOWEL"],
        preserved_identity_ids=("i2",)
    ),
    # ... similar for c3, c4
]
```

#### S₂ → S₃ → S₄ → S₅: Operative Units → Syllables → Composition

```python
# Syllable 1: كا (CV)
Syllable(
    onset_unit_ids=("u1",),  # ك
    nucleus_unit_ids=("u2",),  # ا
    syllable_type=CV,
    preserved_identity_ids=("i1", "i2")
)

# Syllable 2: تب (CVC)
Syllable(
    onset_unit_ids=("u3",),  # ت
    nucleus_unit_ids=("u4",),  # ب (with implicit vowel)
    coda_unit_ids=(),
    syllable_type=CVC,
    preserved_identity_ids=("i3", "i4")
)

# Composition
SyllableComposition(
    syllable_ids=("σ1", "σ2"),
    composition_type=BISYLLABIC,
    preserved_identity_ids=("i1", "i2", "i3", "i4")
)
```

#### S₅ → S₆: Composition → DalPath (CRITICAL BRANCHING)

**Qiyās Proof for Mushtaq (Derived) Path**:

```python
qiyas_katib = QiyasProof(
    # Origin: ضارب (known فاعِل active participle)
    origin_id="origin_darib",
    origin_surface="ضارب",
    origin_hukm="ACTIVE_PARTICIPLE_LICENSE",

    # Branch: كاتب
    branch_id="branch_katib",
    branch_surface="كاتب",
    branch_path_type=DalPathType.MUSHTAQ,

    # Shared cause: فاعِل pattern
    effective_description_id="ed_fail_pattern",
    shared_cause="C₁āC₂iC₃ pattern expressing agent semantic role",
    cause_applies_to_origin=True,
    cause_applies_to_branch=True,

    # No invalidating differences
    invalidating_differences=(),
    blocking_differences=(),

    evidence=(
        "Both trilateral roots",
        "Both follow C₁āC₂iC₃ pattern",
        "Both express agent/doer",
        "Both derive from Form I verbs"
    ),

    accepted=True
)

# Apply transition
f_5(composition, qiyas_katib) → DalPath(
    path_type=DalPathType.MUSHTAQ,
    path_license=qiyas_katib,
    competing_paths=(DalPathType.PROPER_NAME,),  # "كاتب" could be a name
    path_rank="HYPOTHESIS",
    preserved_identity_ids=("i1", "i2", "i3", "i4")
)
```

#### S₆ → S₇: DalPath → RootStem

```python
f_6(path_mushtaq, root_extraction_proof) → RootStem(
    root_consonants=("ك", "ت", "ب"),
    root_type=TRILATERAL,
    stem_type=SIMPLE,
    preserved_identity_ids=("i1", "i3", "i4"),
    residuals=("i2",)  # Long ا is pattern component, not root
)
```

#### S₇ → S₈: RootStem → Weight

```python
f_7(root_stem, weight_proof) → Weight(
    pattern="فاعِل",
    pattern_type=ACTIVE_PARTICIPLE,
    weight_license=WeightLicense(
        origin="known فاعِل instances",
        shared_cause="agent derivation",
        ...
    ),
    preserved_identity_ids=("i1", "i3", "i4"),
    residuals=("i2",)
)
```

#### S₈ → S₉ → S₁₀: Weight → MabniMuʿrab → JamidMushtaq

```python
# MabniMuʿrab
f_8(weight, declension_proof) → MabniMurab(
    category=MabniMurabCategory.MURAB,  # Declinable
    case_potential=CasePotential(NOM, ACC, GEN),
    preserved_identity_ids=("i1", "i3", "i4"),
    residuals=("i2",)
)

# JamidMushtaq
f_9(mabni_murab, derivation_proof) → JamidMushtaq(
    category=JamidMushtaqCategory.MUSHTAQ,  # Derived
    source_verb="كَتَبَ",
    derivation_license=DerivationLicense(...),
    preserved_identity_ids=("i1", "i3", "i4"),
    residuals=("i2",)
)
```

#### S₁₀ → S₁₁: JamidMushtaq → LafzMufrad (FINAL ACCEPTANCE)

```python
acceptance_proof = LafzMufradAcceptanceProof(
    word_id="lafz_katib",
    surface="كاتب",

    # Complete identity chain from S₀
    carrier_ids=("c1", "c2", "c3", "c4"),
    identity_ids=("i1", "i2", "i3", "i4"),

    # Proof chain
    qiyas_proof_ids=("qiyas_katib",),
    carrier_proofs=("proof_c1", "proof_c2", "proof_c3", "proof_c4"),
    syllable_proofs=("proof_σ1", "proof_σ2"),
    weight_proofs=("proof_fail_pattern",),
    mushtaq_proofs=("proof_derivation",),

    # Components
    stem_units=("كاتب",),
    prefix_units=(),
    suffix_units=(),
    clitic_units=(),

    # Residuals: pattern vowel ا
    residuals=("i2",),

    # Rank
    rank="HYPOTHESIS",

    # Trace
    trace_id="trace_katib_full_chain",

    # Forbidden outputs
    produces_meaning=False,
    produces_ifadah=False,
    produces_hukm=False
)

# Final transition
f_10(jamid_mushtaq, acceptance_proof) → LafzMufrad(
    surface="كاتب",
    acceptance_proof=acceptance_proof,
    preserved_identity_ids=("i1", "i2", "i3", "i4"),
    stem_units=("كاتب",),
    residuals=("i2",),
    rank="HYPOTHESIS",
    produces_meaning=False,
    produces_ifadah=False,
    produces_hukm=False
)
```

**Result**: كاتب accepted as **single word (كلمة مفردة)** with rank HYPOTHESIS, derived path, active participle pattern.

---

### Example 2: مِنْ (min - from)

**Input**: مِنْ (U+0645 U+0650 U+0646 U+0652)

#### Path Selection: Particle Path

At S₅ → S₆, qiyās proof selects **PARTICLE** path:

```python
qiyas_min = QiyasProof(
    # Origin: إلى (known particle)
    origin_id="origin_ila",
    origin_surface="إلى",
    origin_hukm="PARTICLE_LICENSE",

    # Branch: مِنْ
    branch_id="branch_min",
    branch_surface="مِنْ",
    branch_path_type=DalPathType.PARTICLE,

    # Shared cause
    shared_cause="Monosyllabic preposition, mabnī, governs genitive",
    cause_applies_to_origin=True,
    cause_applies_to_branch=True,

    invalidating_differences=(),

    accepted=True
)
```

#### Final Acceptance

```python
LafzMufrad(
    surface="مِنْ",
    acceptance_proof=LafzMufradAcceptanceProof(
        path_selected=DalPathType.PARTICLE,
        mabni_candidate=True,  # Indeclinable
        murab_candidate=False,
        jamid_candidate=True,  # Non-derived
        mushtaq_candidate=False,
        ...
    ),
    rank="HYPOTHESIS",
    produces_meaning=False,
    produces_ifadah=False,
    produces_hukm=False
)
```

---

### Example 3: فكتبوه (fakatabūhu - so they wrote it)

**Input**: فكتبوه (fa + katabū + hu = so + they-wrote + it)

**Complex structure**: Prefix + Verb + Suffix

#### Component Analysis

1. **ف (fa)**: Coordinating particle prefix
2. **كتبوا (katabū)**: Past tense verb, 3rd person masculine plural
3. **ه (hu)**: Object pronoun suffix

#### Path Selection: Three Separate Paths

**At S₆, this branches into THREE competing analyses**:

1. **Single word with clitics** (preferred):
   ```python
   LafzMufrad(
       surface="فكتبوه",
       prefix_units=("ف",),
       stem_units=("كتب",),
       suffix_units=("وا", "ه"),
       path_type=CLITICIZED,
       rank="HYPOTHESIS"
   )
   ```

2. **Three separate words** (rejected at composition level):
   - Rejected because ف and ه are NOT independent words

3. **Deferred** (if insufficient evidence):
   - If clitic attachment rules unclear

**Acceptance proof must show**:
- ف is licensed clitic prefix
- كتب is valid root
- وا is licensed plural marker
- ه is licensed object pronoun
- All identities preserved
- No meaning/ifādah/hukm produced

---

## Final Algebraic Formula

### The Acceptance Equation

```
∀x ∈ S₀ (UnicodeRaw):

    x is accepted as LafzMufrad in S₁₁

    ⟺

    ∃ proof chain π = (π₀, π₁, ..., π₁₀) such that:

    1. Identity Preservation:
       ∀i ∈ {0,...,10}: f_i preserves all identity_ids from x

    2. Proof Validity:
       ∀i ∈ {0,...,10}: π_i ⊢ transition f_i valid

    3. Minimal Completeness:
       ∀i ∈ {0,...,10}: f_i(x) meets minimal_completeness_s_i

    4. No Blocking:
       ∀i ∈ {0,...,10}: ¬∃ blocking_description or blocking_difference

    5. No Invalidating Differences:
       ∀i ∈ {5,...,10}: ¬∃ invalidating_difference (fariq qādih)

    6. Trace Preservation:
       trace(f₁₀(f₉(...f₀(x)...))) connects to trace(x)

    7. Rank Assignment:
       rank assigned by proof strength, NOT assumed

    8. Residual Documentation:
       All unresolved elements documented at each stage

    9. Constitutional Compliance:
       produces_meaning = False
       produces_ifadah = False
       produces_hukm = False
```

### Rejection Formula

```
x is REJECTED (⊥) at stage i

    ⟺

    ∃ rejection_reason ∈ {
        NO_PROOF,
        INVALID_PROOF,
        BLOCKING_DESCRIPTION,
        INVALIDATING_DIFFERENCE,
        IDENTITY_LOSS,
        INCOMPLETE_MINIMUM,
        FORBIDDEN_OUTPUT
    }
```

### Deferred Formula

```
x is DEFERRED (موقوف) at stage i

    ⟺

    π_i insufficient BUT no definitive rejection

    ∧

    ∃ potential_path requiring more evidence
```

---

## Supreme Algorithmic Law

```
كل انتقال لا يحمل برهانه ليس انتقالًا في هذا النظام، بل تخمين
```

**Translation**:
"Every transition that does not carry its proof is not a transition in this system, but a guess."

**Formal Statement**:

```
∀i ∈ {0,1,...,10}, ∀x ∈ S_i, ∀y ∈ S_{i+1}:

    f_i(x) = y  ⟺  ∃π_i: π_i ⊢ (x → y)

    OTHERWISE: f_i(x) = ⊥
```

**Operational Consequence**:

```python
def transition(x: S_i, f: Callable, proof: Proof) -> Optional[S_{i+1}]:
    """
    ALL transitions MUST have proof.
    Without proof: undefined (⊥).
    """
    if proof is None:
        return None  # ⊥ - NO TRANSITION WITHOUT PROOF

    if not validate_proof(proof):
        return None  # ⊥ - INVALID PROOF

    # Proof valid - proceed
    return f(x, proof)
```

---

## Verification Criteria

### System-Level Verification

```python
def verify_dta_system() -> bool:
    """
    Verify entire Dal Transition Algebra system.
    """
    return all([
        # 1. All spaces defined
        all_spaces_defined([S₀, S₁, ..., S₁₁]),

        # 2. All transitions defined
        all_transitions_defined([f₀, f₁, ..., f₁₀]),

        # 3. All proof types defined
        all_proof_types_defined(Π),

        # 4. Identity preservation enforced
        identity_preservation_enforced(),

        # 5. Minimal completeness checked at each stage
        minimal_completeness_checked(),

        # 6. Qiyās proofs validated
        qiyas_validation_enforced(),

        # 7. Residuals documented
        residuals_documented(),

        # 8. Ranks assigned (not assumed)
        ranks_assigned_not_assumed(),

        # 9. Trace preservation enforced
        trace_preservation_enforced(),

        # 10. Constitutional compliance
        constitutional_compliance_enforced()
    ])
```

---

## Summary: Operational Mathematics Complete

The Dal Transition Algebra (DTA) is now **fully specified** as operational mathematics:

1. ✅ **Twelve formal spaces** (S₀ to S₁₁) defined with types
2. ✅ **Eleven transition functions** (f₀ to f₁₀) as partial functions requiring proof
3. ✅ **Qiyās as operational function** with formal validation
4. ✅ **Node proof structure** documenting every transition
5. ✅ **Acceptance/rejection predicates** with precise criteria
6. ✅ **Minimal completeness** specified per space
7. ✅ **Islamic legal concepts** integrated as operators
8. ✅ **Path tree with 12 branches** at S₆
9. ✅ **Complete worked examples** (كاتب, مِنْ, فكتبوه)
10. ✅ **Final algebraic formula** and verification criteria

**This is NOT a conceptual diagram. This IS complete operational mathematics.**

Every transition carries proof. Every proof is auditable. Every identity is preserved. Every residual is documented. Every rank is assigned (not assumed).

**No transition without origin. No origin without effective description. No qiyās without shared cause. No cause with invalidating difference. No acceptance without identity preservation. No ascent without minimal completeness.**

---

**Version**: 1.0.0
**Status**: 📐 Complete Formal Specification
**Next**: Implementation in code (PR-A through PR-H)

