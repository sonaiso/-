# KERNEL MIGRATION GAPS

> **PR-ARCH0 companion document.**
>
> هذه قائمة الفجوات المعروفة بين الواقع الحالي للمستودع وبين
> [`ARCHITECTURE_AUTHORITY_MAP.md`](./ARCHITECTURE_AUTHORITY_MAP.md). كل بند
> هنا هو إمّا (أ) رمز قديم سيُهاجَر إلى نواة `fvafk.algebra`، أو (ب) سطح
> adapter سيبقى لكن **بشرط** أن يكون موثقًا صراحةً كadapter (وليس كأصل
> دستوري ثانٍ).

The guard test
[`tests/test_algebra_kernel_uniqueness.py`](../tests/test_algebra_kernel_uniqueness.py)
enforces this list: any source file that redefines one of the kernel names
(`Rank`, `Result`, `Evidence`, `Residual`, `Failure`, `Trace`) must either
live inside `fvafk.algebra/` **or** be listed in
`ALLOWED_REDEFINING_PATHS` *and* contain an explicit adapter marker
referencing this document.

---

## 1. Open migration gaps

### G1 — `src/gfa/governance/rank.py`

- **Status**: Legacy parallel `Rank` enum still imported by
  `src/gfa/governance/__init__.py` and `tests/gfa/governance/test_status_gate.py`.
- **Target**: Replace the local `class Rank(Enum)` with a re-export of
  `fvafk.algebra.Rank`, mapping any legacy member names (`ZERO`, `ZANNI`,
  `BLOCKED`, etc.) to the canonical kernel ranks (`UNRESOLVED`, `CANDIDATE`,
  `LICENSED`, `CERTIFIED`, `REFUTED`) via an adapter function — not by
  redefining the enum.
- **Adapter requirement**: until the migration lands, the file must carry a
  top-of-file note declaring itself a migration-gap adapter and referencing
  this document.
- **Owner PR**: TBD (post-ARCH0). Must not be bundled with GOV1.

### G2 — `src/fvafk/c1/trace_v1.py`

- **Status**: Pre-kernel surface that exposes `Trace = C1Trace` as a
  backward-compatible alias for the C1 phase.
- **Target**: Already documented and tested (see
  `tests/test_algebra_kernel_uniqueness.py::test_trace_v1_*`). No code change
  required, but the alias must remain a **pre-kernel adapter only** with a
  documented `to_algebra_trace()` lift into `fvafk.algebra.Trace`.
- **Adapter requirement**: keeps existing pre-kernel marker, `adapter`
  language, and reference to
  [`ALGEBRA_KERNEL_CONSTITUTION.md`](./ALGEBRA_KERNEL_CONSTITUTION.md).
- **Owner PR**: stable; revisited only if `Trace` semantics change.

### G3 — `src/dal_core/evidence.py` and `src/dal_core/residuals.py`

- **Status**: `dal_core` carries its own `DalEvidence` / residual records as
  part of the 8-layer domain proof kernel (D0–D7). These are **domain
  structures**, not kernel redefinitions, but the file names collide with
  forbidden bare class names if a future refactor renames them to
  `Evidence` / `Residual`.
- **Target**: Provide explicit `to_algebra_evidence()` /
  `to_algebra_residual()` adapter functions that lift the `dal_core`
  domain structures into `fvafk.algebra.Evidence` / `Residual` whenever a
  governed `Result[T]` boundary is crossed.
- **Adapter requirement**: the modules already appear in the
  `ALLOWED_REDEFINING_PATHS` whitelist; they must each contain an adapter
  note referencing this document (added in this PR if missing).
- **Owner PR**: post-ARCH0, paired with a `dal_core` → algebra boundary
  test.

### G4 — `src/dal_core/pipeline.py`

- **Status**: `dal_core` pipeline currently returns domain-specific result
  shapes (`MufradProof`, `MorphProof`, etc.) rather than `Result[T]`.
- **Target**: At the outermost pipeline boundary, wrap pipeline outputs as
  `Result[MufradProof]`, `Result[MorphProof]`, ... using
  `fvafk.algebra.Result`. Internal stage handoffs may keep domain types.
- **Adapter requirement**: pipeline.py is in `ALLOWED_REDEFINING_PATHS` for
  legacy reasons; must carry an adapter-status note.
- **Owner PR**: post-ARCH0.

### G5 — `src/gfa/proto_prior/first_prior_unit.py`

- **Status**: Currently in `ALLOWED_REDEFINING_PATHS` (uses a kernel-name
  class for backward compatibility).
- **Target**: Convert to a domain dataclass with a clearly different name and
  expose a lift function returning `Result[FirstPriorUnit]`.
- **Adapter requirement**: must carry an adapter-status note referencing this
  document until the rename lands.
- **Owner PR**: post-ARCH0.

### G6 — Inspection results

- **Status**: `tools/` and `tests/tools/test_architectural_admission.py`
  produce inspection outputs as plain dicts / dataclasses.
- **Target**: Lift them into `Result[InspectionReport]`, where
  `InspectionReport` is a domain dataclass and `Result` is the constitutional
  one from `fvafk.algebra`.
- **Adapter requirement**: no parallel `InspectionResult` class is allowed.
- **Owner PR**: prerequisite for any future Inspection Algebra / GOV1 step.

### G7 — Workflow results

- **Status**: No central `WorkflowResult` exists yet, but several modules are
  trending toward one as governance discussion grows.
- **Target**: Pre-empt the divergence by declaring that any workflow outcome
  must surface as `Result[WorkflowReport]`. No new `WorkflowResult` /
  `WorkflowOutcome` class outside the kernel.
- **Adapter requirement**: kernel-uniqueness guard already enforces this; no
  code change required until a workflow layer is actually added.
- **Owner PR**: prerequisite for any future WorkflowGeometry / GOV1 step.

---

## 2. Closed / accepted adapters

The following are intentionally kept as adapter surfaces and are not migration
gaps. They are listed here for completeness so future contributors know they
were reviewed:

- `src/fvafk/c1/trace_v1.py::Trace` — pre-kernel alias (covered by G2).
- `src/dal_core/evidence.py`, `src/dal_core/residuals.py`,
  `src/dal_core/pipeline.py` — domain structures with adapter notes
  (covered by G3, G4).
- `src/gfa/proto_prior/first_prior_unit.py` — domain backwards-compatibility
  (covered by G5).

---

## 3. Enforcement

The list above is enforced mechanically by
[`tests/test_algebra_kernel_uniqueness.py`](../tests/test_algebra_kernel_uniqueness.py):

1. **No parallel kernel definitions.** Any `class Rank` / `class Result` /
   `class Evidence` / `class Residual` / `class Failure` / `class Trace`
   outside `src/fvafk/algebra/` is a test failure **unless** the file is
   added to `ALLOWED_REDEFINING_PATHS`.
2. **Allowed paths must be documented as adapters.** Every file in
   `ALLOWED_REDEFINING_PATHS` must contain an explicit adapter marker —
   either the word `adapter` and a reference to this document
   (`KERNEL_MIGRATION_GAPS`) — or the suite fails. This prevents the
   whitelist from silently growing into a parallel kernel.
3. **No silent additions to the whitelist.** Adding an entry to
   `ALLOWED_REDEFINING_PATHS` without also adding it (or an explicit
   "Closed / accepted adapters" entry) here is itself the violation that
   ARCH0 was created to prevent.

---

## 4. Governing law

```text
لا GOV1 قبل ARCH0.
لا Workflow قبل Kernel Authority.
لا Inspection Result موازية لـ Result.
لا Trace موازية لـ Trace.
لا Rank موازية لـ Rank.
```

See [`ARCHITECTURE_AUTHORITY_MAP.md`](./ARCHITECTURE_AUTHORITY_MAP.md) for the
full authority declaration.
