# Bidirectional Analysis Charter

**PR #21**: Ordered Dal Form Governance
**Document**: Bidirectional analysis specification
**Created**: 2026-05-20

---

## Purpose

This charter establishes the rules for **bidirectional form analysis** within ordered dal sequences.

**Critical Principle**: Bidirectional analysis produces **FORM EVIDENCE**, not syntax.

---

## Core Distinction

### Form Analysis vs Syntax Analysis

**Form Analysis** (this document):
- Operates on ordered bounded sequences
- Produces morphological/phonological evidence
- Direction: forward scan, backward scan, bidirectional
- Output: Form candidates with positional context
- Example: "م at index 0 with pattern مَفْعَل suggests place noun candidate"

**Syntax Analysis** (future PRs):
- Operates on mufrad vectors after closure
- Applies nahw operators
- Produces grammatical relations (ISN, TADMN, TAQYID)
- Output: Relation candidates with case effects
- Example: "Word at position 2 is mubtada candidate (pre-syntax), then confirmed mubtada after إبتداء operator"

**Rule**: Form analysis MUST NOT produce syntax claims.

---

## Two Scan Directions

### Forward Scan (Left-to-Right)

**Direction**: `previous → current → next`

**Purpose**: Identify morphological structure from word start:
- Prefixes (بادئة)
- Root-initial position (أول الجذر)
- Front augments (زيادة أمامية)
- Pattern-initial matching

**Operates on**:
- Letter sequences
- Syllable sequences
- Morpheme boundaries

**Output**: Forward form candidates

**Example**:
```python
# Input: "مَكْتَب"
forward_scan(atoms) → [
    PrefixCandidate(letter="م", index=0, hypothesis="MAKAN"),
    RootStartCandidate(letter="ك", index=1),
    RootContinueCandidate(letter="ت", index=2),
    RootEndCandidate(letter="ب", index=3),
]
```

---

### Backward Scan (Right-to-Left)

**Direction**: `next → current → previous`

**Purpose**: Identify morphological structure from word end:
- Suffixes (لاحقة)
- Case marks (علامة إعرابية)
- Attached pronouns (ضمير متصل)
- Number/gender markers (عدد/جنس)
- Pattern-final matching

**Operates on**:
- Letter sequences (reversed)
- Syllable sequences (reversed)
- Morpheme boundaries

**Output**: Backward form candidates

**Example**:
```python
# Input: "كِتَابٌ"
backward_scan(atoms) → [
    CaseMarkCandidate(mark="DAMMA+TANWEEN", index=4, hypothesis="NOMINATIVE"),
    RootFinalCandidate(letter="ب", index=3),
    RootMiddleCandidate(letter="ت", index=2),  # or augment
    RootInitialCandidate(letter="ك", index=0),
]
```

---

## Bidirectional Analysis Rules

### Rule 1: Scan Produces Candidates, Not Certainties

```text
Forward scan → forward candidates
Backward scan → backward candidates
Bidirectional → competing candidates from both directions
```

**Forbidden**: "Forward scan proves م is prefix" ❌

**Allowed**: "Forward scan produces prefix candidate for م at index 0" ✅

---

### Rule 2: Candidates Must Carry Direction

```python
@dataclass
class DirectionalCandidate:
    """Form candidate with direction"""
    unit: BoundedUnit
    scan_direction: ScanDirection  # FORWARD | BACKWARD | BIDIRECTIONAL
    hypothesis: str
    confidence: float
    evidence: List[Evidence]
```

---

### Rule 3: Direction Affects Evidence Scope

**Forward scan evidence**:
- Previous unit context
- Left boundary type
- Pattern prefix matching
- Lexicon prefix lookup

**Backward scan evidence**:
- Next unit context
- Right boundary type
- Pattern suffix matching
- Case mark detection

**Bidirectional evidence**:
- Both prev and next context
- Full span boundaries
- Complete pattern matching
- Lexicon full-word lookup

---

## Directional Analysis Operations

### Forward Scan Algorithm

```python
def forward_scan(units: List[BoundedUnit]) -> List[ForwardCandidate]:
    """
    Scan left-to-right producing forward form candidates.

    For each unit at index i:
    1. Check left boundary (is it word/morpheme/root start?)
    2. Examine previous unit (if exists)
    3. Build forward hypothesis
    4. Check forward patterns
    5. Emit forward candidate
    """
    candidates = []

    for i, unit in enumerate(units):
        previous = units[i-1] if i > 0 else None

        # Check for boundary indicators
        if unit.left_boundary in [WORD_START, MORPHEME_START]:
            # Potential prefix or root start
            candidates.extend(
                check_forward_patterns(unit, previous, units[i+1:])
            )

        # Check for continuation patterns
        elif previous:
            candidates.extend(
                check_forward_continuation(unit, previous)
            )

    return candidates
```

### Backward Scan Algorithm

```python
def backward_scan(units: List[BoundedUnit]) -> List[BackwardCandidate]:
    """
    Scan right-to-left producing backward form candidates.

    For each unit at index i (from end):
    1. Check right boundary (is it word/morpheme/root end?)
    2. Examine next unit (if exists)
    3. Build backward hypothesis
    4. Check backward patterns
    5. Emit backward candidate
    """
    candidates = []

    for i in range(len(units)-1, -1, -1):
        unit = units[i]
        next_unit = units[i+1] if i < len(units)-1 else None

        # Check for boundary indicators
        if unit.right_boundary in [WORD_END, MORPHEME_END]:
            # Potential suffix or root end
            candidates.extend(
                check_backward_patterns(unit, next_unit, units[:i])
            )

        # Check for continuation patterns
        elif next_unit:
            candidates.extend(
                check_backward_continuation(unit, next_unit)
            )

    return candidates
```

### Bidirectional Merge

```python
def merge_directional_candidates(
    forward: List[ForwardCandidate],
    backward: List[BackwardCandidate]
) -> List[BidirectionalCandidate]:
    """
    Merge forward and backward candidates.

    Rules:
    1. If same unit has both forward and backward candidates, create bidirectional
    2. If only forward candidate, keep as forward-only
    3. If only backward candidate, keep as backward-only
    4. If contradictory, preserve both as competitors
    """
    merged = {}

    # Index by unit span
    for f_cand in forward:
        key = f_cand.unit.span
        if key not in merged:
            merged[key] = {'forward': [], 'backward': []}
        merged[key]['forward'].append(f_cand)

    for b_cand in backward:
        key = b_cand.unit.span
        if key not in merged:
            merged[key] = {'forward': [], 'backward': []}
        merged[key]['backward'].append(b_cand)

    # Create bidirectional candidates
    bidirectional = []
    for span, candidates in merged.items():
        if candidates['forward'] and candidates['backward']:
            # Both directions agree - strong candidate
            bidirectional.append(
                BidirectionalCandidate(
                    span=span,
                    forward_evidence=candidates['forward'],
                    backward_evidence=candidates['backward'],
                    agreement_level=compute_agreement(...),
                )
            )
        elif candidates['forward']:
            # Forward-only
            bidirectional.append(
                ForwardOnlyCandidate(candidates['forward'])
            )
        else:
            # Backward-only
            bidirectional.append(
                BackwardOnlyCandidate(candidates['backward'])
            )

    return bidirectional
```

---

## Form Evidence Types

### Prefix Evidence (Forward)

```python
@dataclass
class PrefixEvidence:
    """Evidence from forward scan"""
    letter: str
    index: int
    left_boundary: BoundaryType
    pattern_match: Optional[str]  # e.g., "مَفْعَل"
    lexicon_entry: Optional[str]  # e.g., "مكان_prefix"
    next_letters: List[str]  # Following context
    hypothesis: str  # "MAKAN_PREFIX" | "ROOT_START" | ...
```

### Suffix Evidence (Backward)

```python
@dataclass
class SuffixEvidence:
    """Evidence from backward scan"""
    letters: str  # May be multi-letter (ـون، ـات)
    index: int
    right_boundary: BoundaryType
    case_mark: Optional[str]  # DAMMA, FATHA, etc.
    pronoun: Optional[str]  # هُ، هَا، هُم، etc.
    number_gender: Optional[str]  # DUAL, PLURAL, FEM, etc.
    previous_letters: List[str]  # Preceding context
    hypothesis: str  # "PRONOUN_HU" | "PLURAL_MASC" | ...
```

### Root Pattern Evidence (Bidirectional)

```python
@dataclass
class RootPatternEvidence:
    """Evidence from full pattern match"""
    root_letters: Tuple[str, ...]
    letter_indices: Tuple[int, ...]
    pattern: str  # "فَعَلَ" | "فاعِل" | "مَفْعول" | ...
    left_boundary: BoundaryType
    right_boundary: BoundaryType
    augments: List[AugmentCandidate]  # Detected augments
    hypothesis: str  # "PAST_VERB" | "ACTIVE_PARTICIPLE" | ...
```

---

## Adjacency Relations

### Previous-to-Next Relation

```python
@dataclass
class ForwardAdjacency:
    """Forward adjacency relation"""
    previous_unit: BoundedUnit
    current_unit: BoundedUnit
    relation_type: str  # "PREFIX_TO_ROOT" | "ROOT_TO_SUFFIX" | ...
    boundary_at: int  # Shared boundary index
    evidence: List[Evidence]
```

**Example**:
```python
# م → ك in "مَكْتَب"
ForwardAdjacency(
    previous_unit=Atom(char="م", index=0),
    current_unit=Atom(char="ك", index=1),
    relation_type="PREFIX_TO_ROOT_START",
    boundary_at=1,
    evidence=[PrefixPatternEvidence(...)]
)
```

### Next-to-Previous Relation

```python
@dataclass
class BackwardAdjacency:
    """Backward adjacency relation"""
    next_unit: BoundedUnit
    current_unit: BoundedUnit
    relation_type: str  # "SUFFIX_TO_ROOT" | "CASE_TO_STEM" | ...
    boundary_at: int
    evidence: List[Evidence]
```

**Example**:
```python
# ـٌ ← ب in "كِتَابٌ"
BackwardAdjacency(
    next_unit=Atom(haraka="TANWEEN_DAMMA", index=4),
    current_unit=Atom(char="ب", index=3),
    relation_type="CASE_MARK_TO_ROOT_END",
    boundary_at=4,
    evidence=[CaseMarkEvidence(...)]
)
```

---

## Prohibited Syntax Claims

### What Bidirectional Analysis MUST NOT Produce

❌ **FORBIDDEN** (syntax claims):
- "Word is فاعل" (grammatical subject)
- "Word is مفعول" (grammatical object)
- "Word is mubtada"
- "Word is khabar"
- "Word is مضاف إليه"
- Any ISN/TADMN/TAQYID relation
- Any case effect assignment (مرفوع، منصوب، مجرور، مجزوم by operator)

✅ **ALLOWED** (form evidence):
- "Word matches فاعِل pattern candidate"
- "Word matches مَفْعول pattern candidate"
- "Word has nominative case sign potential"
- "Word has genitive case sign potential"
- "Word ends with مضاف construction marker"
- Form adjacency relation (prefix-to-root, root-to-suffix)
- Positional evidence for future operator application

---

## Integration with Future Syntax Layer

### Handoff to Syntax Analysis

```python
# Bidirectional analysis produces form candidates:
form_candidates = bidirectional_analysis(ordered_atoms)

# These become inputs to pre-syntax layer:
presyntax_vector = build_presyntax_vector(form_candidates)

# Pre-syntax allows operator consumption:
if presyntax_vector.allows_operator_consumption(operator):
    # Operator application (future PR)
    syntax_candidates = operator.apply(presyntax_vector)
```

**Separation of concerns**:
1. **Bidirectional analysis** (this PR governance): Form evidence from ordered sequence
2. **Pre-syntax layer** (existing): Readiness for operator consumption
3. **Operator application** (future): Syntax candidates with case effects
4. **Relation building** (future): ISN/TADMN/TAQYID graphs

---

## Verification Rules

```python
def verify_form_analysis_output(candidates):
    """Verify bidirectional analysis produces only form evidence."""

    for candidate in candidates:
        # Must have direction
        assert hasattr(candidate, 'scan_direction')

        # Must have position
        assert hasattr(candidate, 'span')
        assert hasattr(candidate, 'index')

        # Must have boundaries
        assert hasattr(candidate, 'left_boundary')
        assert hasattr(candidate, 'right_boundary')

        # Must NOT have syntax claims
        forbidden_fields = [
            'case_effect',  # Syntax judgment
            'relation_type',  # ISN/TADMN/TAQYID
            'operator_id',  # Operator assignment
            'grammatical_function',  # فاعل/مفعول/mubtada
        ]
        for field in forbidden_fields:
            assert not hasattr(candidate, field), \
                f"Form analysis must not produce {field}"

        # Must have form evidence
        assert hasattr(candidate, 'hypothesis')
        assert hasattr(candidate, 'evidence')
```

---

## Practical Examples

### Example 1: Forward Scan of "مَكْتَب"

```python
atoms = parse_to_atoms("مَكْتَب")

forward_candidates = forward_scan(atoms)

# Expected output:
[
    PrefixCandidate(
        letter="م",
        index=0,
        span=(0, 1),
        hypothesis="MAKAN_PREFIX",
        pattern_match="مَفْعَل",
        left_boundary=WORD_START,
        scan_direction=FORWARD,
    ),
    RootStartCandidate(
        letter="ك",
        index=1,
        span=(1, 2),
        hypothesis="ROOT_INITIAL",
        scan_direction=FORWARD,
    ),
    # ... etc
]
```

### Example 2: Backward Scan of "كِتَابٌ"

```python
atoms = parse_to_atoms("كِتَابٌ")

backward_candidates = backward_scan(atoms)

# Expected output:
[
    CaseMarkCandidate(
        mark="TANWEEN_DAMMA",
        index=4,
        span=(4, 5),
        hypothesis="NOMINATIVE_SIGN",
        right_boundary=WORD_END,
        scan_direction=BACKWARD,
    ),
    RootFinalCandidate(
        letter="ب",
        index=3,
        span=(3, 4),
        hypothesis="ROOT_FINAL",
        scan_direction=BACKWARD,
    ),
    # ... etc
]
```

### Example 3: Bidirectional Merge

```python
forward = forward_scan(atoms)
backward = backward_scan(atoms)

bidirectional = merge_directional_candidates(forward, backward)

# If both scans agree on root letters ك-ت-ب:
[
    BidirectionalCandidate(
        span=(0, 5),
        root_letters=("ك", "ت", "ب"),
        pattern="فِعَال",
        forward_evidence=[...],
        backward_evidence=[...],
        agreement_level=0.95,  # High agreement
        hypothesis="NOUN_FIAL_PATTERN",
    )
]
```

---

## Conclusion

Bidirectional analysis establishes:

1. ✅ Two scan directions (forward, backward)
2. ✅ Directional candidates with position
3. ✅ Form evidence, NOT syntax claims
4. ✅ Adjacency relations with direction
5. ✅ Clean handoff to future syntax layer

**Critical invariant**:
> Bidirectional analysis produces morphological form candidates.
> It does NOT produce grammatical relations or case effects.

All future form analysis implementations must respect this boundary.

---

**Status**: ✅ Governance specified (no implementation)
**Next**: Create lightweight doc-presence tests
