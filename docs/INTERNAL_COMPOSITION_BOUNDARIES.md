# Internal Composition Boundaries

**PR #21**: Ordered Dal Form Governance
**Document**: Internal composition boundary specification
**Created**: 2026-05-20

---

## Purpose

This document specifies how **internal boundaries** within a dal unit must be represented to support ordered composition.

---

## Boundary Types

### 1. Position Boundaries

Every unit has two position boundaries:

```python
class PositionBoundary(Enum):
    """Position-based boundaries"""
    SEQUENCE_START = "بداية_التسلسل"  # First position
    SEQUENCE_END = "نهاية_التسلسل"    # Last position
    INTERNAL = "داخلي"                # Middle position
```

### 2. Linguistic Boundaries

Boundaries aligned with linguistic structure:

```python
class LinguisticBoundary(Enum):
    """Linguistic structure boundaries"""
    WORD_START = "بداية_كلمة"
    WORD_END = "نهاية_كلمة"
    SYLLABLE_START = "بداية_مقطع"
    SYLLABLE_END = "نهاية_مقطع"
    MORPHEME_START = "بداية_صرفية"
    MORPHEME_END = "نهاية_صرفية"
    ROOT_START = "بداية_جذر"
    ROOT_END = "نهاية_جذر"
    AFFIX_START = "بداية_لاحقة_بادئة"
    AFFIX_END = "نهاية_لاحقة_بادئة"
```

### 3. Compositional Boundaries

Boundaries created by composition operations:

```python
class CompositionalBoundary(Enum):
    """Composition-created boundaries"""
    FOLD_START = "بداية_طي"
    FOLD_END = "نهاية_طي"
    CONCAT_POINT = "نقطة_ربط"
    SPLIT_POINT = "نقطة_فصل"
```

---

## Boundary Rules

### Rule 1: Every Unit Has Exactly Two Boundaries

```python
@dataclass
class BoundedUnit:
    """Every unit must have left and right boundaries"""
    left_boundary: BoundarySpec
    right_boundary: BoundarySpec
    span: Tuple[int, int]  # (start_index, end_index)
```

### Rule 2: Boundaries Must Align with Parent Sequence

```python
# Child boundaries must be within parent span
assert child.span[0] >= parent.span[0]
assert child.span[1] <= parent.span[1]

# Boundary positions must match indices
assert child.left_boundary.index == child.span[0]
assert child.right_boundary.index == child.span[1]
```

### Rule 3: Adjacent Units Share Boundary

```python
# If unit1 is immediately before unit2:
if unit1.next_unit == unit2:
    assert unit1.right_boundary.index == unit2.left_boundary.index - 1
    # Shared boundary point: unit1.span[1] == unit2.span[0]
```

---

## Composition Operations

### Fold (Aggregate)

Combining multiple units into one higher-level unit:

```python
def fold_units(units: List[BoundedUnit]) -> BoundedUnit:
    """
    Fold multiple bounded units into single unit.

    Requirements:
    1. Units must be consecutive (no gaps)
    2. Result span = (first.span[0], last.span[1])
    3. Left boundary from first unit
    4. Right boundary from last unit
    5. Must preserve source_trace
    """
    assert are_consecutive(units), "Cannot fold non-consecutive units"

    result = BoundedUnit(
        left_boundary=units[0].left_boundary,
        right_boundary=units[-1].right_boundary,
        span=(units[0].span[0], units[-1].span[1]),
        source_trace=[u.get_trace() for u in units],
        fold_operation="aggregate",
    )

    return result
```

### Split (Segment)

Dividing one unit into multiple sub-units:

```python
def split_unit(unit: BoundedUnit, split_points: List[int]) -> List[BoundedUnit]:
    """
    Split bounded unit into sub-units.

    Requirements:
    1. Split points must be within unit span
    2. Each sub-unit gets appropriate boundaries
    3. Sub-units must be consecutive
    4. Must preserve reverse_trace to parent
    """
    sub_units = []
    prev_index = unit.span[0]

    for split_point in split_points + [unit.span[1]]:
        sub_unit = BoundedUnit(
            left_boundary=get_boundary_at(prev_index),
            right_boundary=get_boundary_at(split_point),
            span=(prev_index, split_point),
            reverse_trace=unit.get_trace(),
            split_operation="segment",
        )
        sub_units.append(sub_unit)
        prev_index = split_point

    return sub_units
```

### Concatenate (Join)

Joining units while preserving internal boundaries:

```python
def concatenate_units(units: List[BoundedUnit]) -> BoundedUnit:
    """
    Concatenate units preserving internal structure.

    Requirements:
    1. Units need not be from same parent
    2. Result span includes all units
    3. Internal boundaries preserved as concat_points
    4. Must track composition_trace
    """
    internal_boundaries = []
    for i in range(len(units) - 1):
        internal_boundaries.append(
            CompositionalBoundary.CONCAT_POINT,
            index=units[i].right_boundary.index
        )

    result = BoundedUnit(
        left_boundary=units[0].left_boundary,
        right_boundary=units[-1].right_boundary,
        span=(units[0].span[0], units[-1].span[1]),
        internal_boundaries=internal_boundaries,
        composition_trace=[u.get_trace() for u in units],
    )

    return result
```

---

## Boundary Violation Detection

### Invalid Boundary Scenarios

**1. Overlapping Units**:
```python
# FORBIDDEN: Units with overlapping spans
unit1.span = (0, 5)
unit2.span = (3, 8)  # Overlaps with unit1!
```

**2. Gap Between Adjacent Units**:
```python
# FORBIDDEN: Gap between consecutive units
unit1.span = (0, 3)
unit2.span = (5, 8)  # Gap at indices 3-4!
```

**3. Boundary Mismatch**:
```python
# FORBIDDEN: Boundary type doesn't match position
unit.left_boundary = WORD_START
unit.span = (3, 7)  # But index 3 is not word start!
```

**4. Fold Without Consecutive Source**:
```python
# FORBIDDEN: Folding non-consecutive units
units = [unit_at_0, unit_at_5]  # Gap between them
folded = fold_units(units)  # VIOLATION!
```

---

## Boundary-Preserving Transformations

### Layer Transitions

When moving from layer N to layer N+1:

```python
def layer_transition(
    lower_units: List[BoundedUnit],
    higher_level_constructor
) -> BoundedUnit:
    """
    Transition from lower to higher layer.

    Boundary preservation rules:
    1. Higher unit span encompasses all lower spans
    2. Higher unit boundaries reference lowest-level boundaries
    3. Intermediate boundaries preserved in trace
    """
    # Get outermost boundaries
    left_most = min(u.span[0] for u in lower_units)
    right_most = max(u.span[1] for u in lower_units)

    # Preserve original boundary types
    left_boundary = get_deepest_boundary(lower_units[0].left_boundary)
    right_boundary = get_deepest_boundary(lower_units[-1].right_boundary)

    higher_unit = higher_level_constructor(
        span=(left_most, right_most),
        left_boundary=left_boundary,
        right_boundary=right_boundary,
        source_units=lower_units,
        boundary_trace=collect_all_boundaries(lower_units),
    )

    return higher_unit
```

---

## Practical Examples

### Example 1: Syllable Composition

```python
# Input: Positioned atoms
atoms = [
    Atom(char="ك", haraka="FATHA", index=0, span=(0,1)),
    Atom(char="ت", haraka="FATHA", index=1, span=(1,2)),
    Atom(char="ب", haraka="FATHA", index=2, span=(2,3)),
]

# Fold into syllables
syllable1 = fold_units(atoms[0:2])  # كَتَ → /ka/
# span=(0, 2), left_boundary=WORD_START, right_boundary=SYLLABLE_END

syllable2 = fold_units([atoms[2]])  # بَ → /ba/
# span=(2, 3), left_boundary=SYLLABLE_START, right_boundary=WORD_END

# syllables are consecutive and bounded
assert syllable1.span[1] == syllable2.span[0]
```

### Example 2: Root Extraction with Boundaries

```python
# Input: Word "مَكْتَب"
atoms = [
    Atom(char="م", index=0, span=(0,1), left_boundary=WORD_START),
    Atom(char="ك", index=1, span=(1,2)),
    Atom(char="ت", index=2, span=(2,3)),
    Atom(char="ب", index=3, span=(3,4), right_boundary=WORD_END),
]

# Root extraction (selective fold)
root = selective_fold(
    atoms=atoms,
    selected_indices=[1, 2, 3],  # ك ت ب
    operation="root_extraction"
)

# Result boundary tracking:
root.span = (1, 4)  # Encompasses ك-ت-ب
root.left_boundary = atoms[1].left_boundary  # From ك
root.right_boundary = atoms[3].right_boundary  # From ب
root.source_trace = [atoms[1], atoms[2], atoms[3]]
root.skipped_units = [atoms[0]]  # م was skipped (prefix)
```

---

## Validation Functions

```python
def validate_boundaries(unit: BoundedUnit) -> bool:
    """Validate unit satisfies all boundary rules."""

    # Rule 1: Has both boundaries
    if not (unit.left_boundary and unit.right_boundary):
        return False

    # Rule 2: Span matches boundary indices
    if unit.left_boundary.index != unit.span[0]:
        return False
    if unit.right_boundary.index != unit.span[1]:
        return False

    # Rule 3: Positive span
    if unit.span[0] >= unit.span[1]:
        return False

    # Rule 4: If has previous, check adjacency
    if unit.previous_unit:
        if unit.previous_unit.span[1] != unit.span[0]:
            return False

    # Rule 5: If has next, check adjacency
    if unit.next_unit:
        if unit.span[1] != unit.next_unit.span[0]:
            return False

    return True


def validate_composition(
    result: BoundedUnit,
    sources: List[BoundedUnit]
) -> bool:
    """Validate composition preserves boundaries."""

    # Result must encompass all sources
    leftmost = min(s.span[0] for s in sources)
    rightmost = max(s.span[1] for s in sources)

    if result.span != (leftmost, rightmost):
        return False

    # Must have source trace
    if not hasattr(result, 'source_trace'):
        return False

    # If sources are consecutive, result must be fold
    if are_consecutive(sources):
        if not hasattr(result, 'fold_operation'):
            return False

    return True
```

---

## Conclusion

Internal composition boundaries ensure that:

1. ✅ Every unit has definite position and extent
2. ✅ Composition operations preserve traceability
3. ✅ Adjacent units align correctly
4. ✅ Layer transitions maintain boundary consistency
5. ✅ No "floating" claims without positional context

All future dal_core implementations must enforce these boundary rules.

---

**Status**: ✅ Governance specified (no implementation)
**Next**: BIDIRECTIONAL_ANALYSIS_CHARTER.md
