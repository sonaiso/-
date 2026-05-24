# Algebra Kernel Constitution

**Authority**: This document establishes `fvafk.algebra` as the single constitutional kernel for all governed outputs in the repository.

**Date**: 2026-05-24
**Status**: CONSTITUTIONAL LAW

---

## The Foundational Law

```
لا مخرج عارٍ.
Every Result = value + rank + evidence + residuals + failures + replay.
```

**English**: No bare output. Every governed result must carry its value, epistemic rank, supporting evidence, unresolved residuals, failures, and replay trace.

---

## Constitutional Declaration

### Article 1: Single Source of Truth

`fvafk.algebra` is declared the **SOLE constitutional kernel** for:

- **Rank** - Epistemic rank enumeration
- **Result** - Governed output structure
- **Evidence** - Supporting observations
- **Residual** - Unresolved concerns
- **Failure** - Active contradictions
- **Trace** - Provenance record

**Location**: `src/fvafk/algebra/core.py`

**Public API**: `src/fvafk/algebra/__init__.py`

### Article 2: Prohibition of Parallel Definitions

**No duplicate constitutional primitives** are permitted outside `fvafk.algebra` except:

1. **Temporary adapters** during migration (must be marked)
2. **Domain-specific extensions** that explicitly inherit from or reference the kernel
3. **Legacy compatibility shims** with explicit deprecation notices

**Violation Examples** (prohibited):
- Defining `class Rank(Enum)` outside `fvafk.algebra` without migration notice
- Creating `InspectionResult` with independent `rank/evidence/residual` fields instead of using `Result[InspectionReport]`
- Implementing `WorkflowResult` as parallel governance structure instead of `Result[WorkflowReport]`

### Article 3: Lossless Lifting Requirement

**Every governed output** must be **losslessly liftable** to `Result[T]`:

```python
# CORRECT: Domain-specific value wrapped in Result
from fvafk.algebra import Result, Rank, Evidence, Residual

@dataclass
class InspectionReport:
    """Domain-specific inspection findings"""
    findings: List[Finding]
    coverage: float

# Inspection returns Result[InspectionReport]
def inspect(code: str) -> Result[InspectionReport]:
    report = InspectionReport(findings=[...], coverage=0.95)
    return Result(
        value=report,
        rank=Rank.LICENSED,
        evidence=(Evidence("static_analysis", "pylint", "clean"),),
        residuals=(Residual("unchecked_branch", "Error path not tested"),)
    )
```

```python
# INCORRECT: Parallel governance structure
@dataclass
class InspectionResult:  # ❌ Duplicates Result structure
    status: str
    rank: str  # ❌ Parallel rank system
    evidence: List[Dict]  # ❌ Parallel evidence format
    residuals: List[str]  # ❌ Parallel residual format
```

### Article 4: Phase 0 Independence

`fvafk.algebra` (Phase 0) is **intentionally standalone**:

- Does NOT import from `fvafk.c1` / `c2a` / `c2b` / `syntax`
- Phase 2 (future) introduces **adapters** that feed layer results as `Evidence`
- This prevents circular dependencies and layer confusion

### Article 5: Domain Extensions via Value, Not Structure

**Domain-specific types** enter as the **value parameter** `T` in `Result[T]`:

```python
# Layer-specific reports
Result[MorphologyReport]
Result[SyntaxReport]
Result[SemanticReport]

# Process-specific decisions
Result[WorkflowDecision]
Result[AdmissionDecision]
Result[LearningTrace]

# Inspection findings
Result[InspectionReport]
Result[AuditReport]
```

The `Result` wrapper provides uniform:
- Epistemic rank (`Rank.CANDIDATE` → `LICENSED` → `CERTIFIED`)
- Evidence trail
- Residual tracking
- Failure recording
- Trace provenance

### Article 6: Migration Protocol

**Existing parallel definitions** must:

1. **Mark with migration notice** (do not break immediately)
2. **Document target**: Which `fvafk.algebra` primitive replaces it
3. **Plan removal**: Issue number or milestone for elimination
4. **Preserve semantics**: Ensure no loss of expressiveness

**Example migration notice**:

```python
# MIGRATION NOTICE: This Rank definition is DEPRECATED.
# TARGET: Migrate to fvafk.algebra.Rank
# TIMELINE: Remove in PR #XXX after adapter layer implemented
# DO NOT extend this enum; use fvafk.algebra.Rank for new code.

class Rank(Enum):  # TODO: MIGRATE TO fvafk.algebra.Rank
    ZERO = 0
    FORM = 1
    # ...
```

### Article 7: Guard Tests Required

A test suite **MUST** enforce uniqueness:

**Test**: `tests/test_algebra_kernel_uniqueness.py`

Verifies:
- No `class Rank(Enum)` outside `fvafk.algebra` (except marked adapters)
- No `class.*Result` implementing parallel governance
- No duplicate `Evidence`, `Residual`, `Failure`, `Trace` definitions

---

## The Seven Critical Laws

### Law 1: No Rank Outside Rank
**Only one epistemic rank system** may exist: `fvafk.algebra.Rank`.

### Law 2: No Result Outside Result
**Every governed output** must be `Result[T]` or losslessly convertible.

### Law 3: No Evidence Outside Evidence
**Supporting observations** use `fvafk.algebra.Evidence` structure.

### Law 4: No Residual Outside Residual
**Unresolved concerns** use `fvafk.algebra.Residual` structure.

### Law 5: No Failure Outside Failure
**Active contradictions** use `fvafk.algebra.Failure` structure.

### Law 6: No Trace Outside Trace
**Provenance records** use `fvafk.algebra.Trace` structure.

### Law 7: No Parallel Governance Systems
**Domain-specific types** enter as values (`T`), not as parallel governance structures.

---

## Verification Commands

### Find Parallel Rank Definitions
```bash
# Should only find fvafk.algebra.core.py (canonical)
# + marked adapters with migration notices
grep -r "class Rank(Enum)" src/ --include="*.py"
```

### Find Parallel Result Structures
```bash
# Inspect for governance duplication
grep -r "class.*Result.*:" src/ --include="*.py" | \
  grep -v "fvafk/algebra" | \
  xargs grep -l "rank.*evidence.*residual"
```

### Run Uniqueness Test
```bash
pytest tests/test_algebra_kernel_uniqueness.py -v
```

---

## Compliance Checklist

For **every new PR** adding governed outputs:

- [ ] Uses `Result[T]` from `fvafk.algebra`
- [ ] Uses `Rank` from `fvafk.algebra.Rank`
- [ ] Uses `Evidence` from `fvafk.algebra.Evidence`
- [ ] Uses `Residual` from `fvafk.algebra.Residual`
- [ ] Uses `Trace` from `fvafk.algebra.Trace`
- [ ] Does NOT create parallel `rank`/`evidence`/`residual` fields
- [ ] Passes `test_algebra_kernel_uniqueness.py`

---

## Migration Timeline

### Identified Parallel Definitions

1. **`src/gfa/proto_prior/first_prior_unit.py:46`**
   - Parallel `Rank` enum
   - Status: Marked for migration
   - Target: `fvafk.algebra.Rank`

2. **`src/dal_core/pipeline.py:9`**
   - Parallel `Rank` enum
   - Status: Marked for migration
   - Target: `fvafk.algebra.Rank`

### Migration Strategy

1. **Phase 1** (Current): Mark + Document
   - Add migration notices to parallel definitions
   - Document in this constitution
   - Add guard tests

2. **Phase 2** (Next): Adapter Layer
   - Create adapters mapping legacy → kernel
   - Ensure semantic preservation
   - Update call sites incrementally

3. **Phase 3** (Future): Removal
   - Remove parallel definitions
   - Collapse to single source
   - Verify guard tests pass

---

## Authority and Enforcement

**This constitution supersedes** all prior conventions regarding:
- Result structures
- Rank systems
- Evidence formats
- Residual tracking
- Governance patterns

**Enforcement mechanism**:
- CI guard test (`test_algebra_kernel_uniqueness.py`)
- PR review requirement
- Architectural admission checker

**Amendment process**:
- Requires explicit PR with "CONSTITUTIONAL AMENDMENT" label
- Must preserve Laws 1-7
- Must maintain lossless lifting property

---

## References

- **Source**: `src/fvafk/algebra/core.py`
- **Public API**: `src/fvafk/algebra/__init__.py`
- **Phase 0 Roadmap**: `docs/ARABIC_ALGEBRA_ROADMAP.md`
- **No Bare Output**: Constitution line 5-6 in `src/fvafk/algebra/__init__.py`

---

**Signed**: Claude Code Agent
**Date**: 2026-05-24
**Status**: ACTIVE CONSTITUTIONAL LAW
