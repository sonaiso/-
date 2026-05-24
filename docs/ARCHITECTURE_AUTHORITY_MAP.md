# ARCHITECTURE AUTHORITY MAP

> **PR-ARCH0 — Architecture Unification and Kernel Authority Map**
>
> هذه الوثيقة تُعلن، رسميًا، **من هو الأصل، ومن هو المجال، ومن هو adapter،
> ومن هو legacy** داخل المستودع. لا يجوز فتح طبقة حوكمة (GOV1) أو هندسة عمل
> (Workflow / Inspection) جديدة قبل توحيد سلطة النواة المُعلنة هنا.

---

## 1. الإعلان الحاكم (Constitutional declaration)

```text
fvafk.algebra هو constitutional kernel.

Rank / Result / Evidence / Residual / Failure / Trace
لها أصل واحد، ومنشأ واحد، وتعريف واحد:

    src/fvafk/algebra/

أي تعريف آخر لهذه المفاهيم هو واحد من ثلاثة فقط:
  1. legacy surface  (سيُهاجَر، موثّق في KERNEL_MIGRATION_GAPS.md)
  2. domain-local structure  (لا يحمل اسم النواة، ولا يدّعي حُكمًا دستوريًا)
  3. adapter  (يُحوِّل قيمة محلية إلى Result[T] / Trace / Evidence دستورية)

أي شيء آخر = violation.
```

The single source of truth for the governing algebra is declared in
[`src/fvafk/algebra/__init__.py`](../src/fvafk/algebra/__init__.py) and
[`docs/ALGEBRA_KERNEL_CONSTITUTION.md`](./ALGEBRA_KERNEL_CONSTITUTION.md):

> لا مخرج عارٍ.
> Every Result = value + rank + evidence + residuals + failures + replay.

This map extends the constitution by naming **who is the kernel**, **who is a
domain**, **who is an adapter**, and **who is legacy** across the full
repository, so that subsequent work (GOV1, WorkflowGeometry,
AgentPermissions, Inspection Algebra) can only land **on top of** a single
kernel — never alongside it.

---

## 2. لماذا الآن؟ (Why this PR before GOV1)

A repository audit identified several parallel centres of authority:

```text
src/fvafk/algebra      ← Result / Rank / Evidence / Residual / Trace kernel
src/dal_core           ← signifier (دال) proof kernel, 8-layer domain D0..D7
src/gfa                ← governed form algebra, gates, prior information
src/maqam_theory       ← gates, minimizers, proofs
src/syntax_theory      ← syntax graph, operators, proofs
src/engines            ← 66 grammar engines (catalog)
root *_engine.py       ← legacy engines, Excel export
```

Each of these is genuinely valuable, but **multiple centres of authority is the
single largest structural risk** in the repository today. The next step is
therefore not a new gate, not GOV1, not a new workflow — it is a written,
testable declaration of who governs what.

The governing law for this phase:

```text
لا GOV1 قبل ARCH0.
لا Workflow قبل Kernel Authority.
لا Inspection Result موازية لـ Result.
لا Trace موازية لـ Trace.
لا Rank موازية لـ Rank.
```

---

## 3. خريطة المكوّنات (Component authority map)

| Component | Path | Role | Owns kernel concepts? | Notes |
|---|---|---|---|---|
| **`fvafk.algebra`** | `src/fvafk/algebra/` | **Constitutional kernel** | ✅ Yes — sole owner of `Rank`, `Result`, `Evidence`, `Residual`, `Failure`, `Trace` | The only place these names may be defined. See [`ALGEBRA_KERNEL_CONSTITUTION.md`](./ALGEBRA_KERNEL_CONSTITUTION.md). |
| `fvafk.c1` / `c2a` / `c2b` / `c2c` / `c2d` / `c2e` | `src/fvafk/` | Linguistic pipeline layers (phonology → morphology) | ❌ No | Consumes kernel; may keep pre-kernel adapter surfaces (e.g. `C1Trace` in `c1/trace_v1.py`) only when documented as adapters. |
| `fvafk.phonology` / `phonology_v2` / `syntax` / `algebra/*subpackages` | `src/fvafk/` | Domain layers | ❌ No | Domain values flow through `Result[T]`. |
| `dal_core` | `src/dal_core/` | Signifier (دال) proof kernel, 8-layer domain (D0–D7) | ❌ No — domain only | Must adapt its internal evidence / residuals / claim records into `fvafk.algebra.Evidence` / `Residual` / `Result[T]` at the kernel boundary. Internal `DalEvidence` / `DalTrace` are **domain structures, not kernel redefinitions**. |
| `gfa` (Governed Form Algebra) | `src/gfa/` | Governed gates, prior information, methods (Wadh, Mutabaqah, Dāl-Madlūl binding, ...) | ❌ No — domain methods + governance gates | Must consume kernel primitives. Legacy `gfa.governance.rank.Rank` is an **explicit migration gap** — see [`KERNEL_MIGRATION_GAPS.md`](./KERNEL_MIGRATION_GAPS.md). |
| `maqam_theory` | `src/maqam_theory/` | Constraint / proof domain (gates, minimizers, 11 theorems) | ❌ No | Must expose its hard/soft gate outcomes and theorem results as `Evidence` / `Residual` carried in `Result[T]`. |
| `syntax_theory` | `src/syntax_theory/` | Graph-based syntax domain (ISN / TADMN / TAQYID, operators, proofs) | ❌ No | Same boundary as `maqam_theory`: kernel-shaped outputs only. |
| `engines` | `src/engines/` (+ root `*_engine.py`) | Legacy / pragmatic grammar catalog (66 engines + ~70 root legacy modules) | ❌ No | Pragmatic catalog. Outputs are pandas DataFrames + Excel exports; no kernel concepts. Treated as **legacy surface** for any future governed pipeline. |
| `web_app` | `web_app/` | Optional FastAPI surface | ❌ No | UI/transport only; carries `Result[T]` payloads, never defines them. |
| `tools/` workflow & inspection checkers | `tools/`, `tests/tools/` | Inspection evidence producers | ❌ No | Must produce `Result[InspectionReport]` / `Result[WorkflowReport]` once lifted (see migration gaps). |
| `coq/`, `coq_proofs/`, `theories/`, `type_system/`, `trace_system/` | top-level | Formal / theoretical scaffolding | ❌ No | Out-of-band proof artifacts; not part of the runtime kernel surface. |

---

## 4. حقوق التعريف (Who may define what)

| Concept | Allowed definer | Forbidden elsewhere? |
|---|---|---|
| `Rank` enum (with the dotted name `Rank` and kernel semantics) | `fvafk.algebra.core.Rank` only | ✅ Yes — see `tests/test_algebra_kernel_uniqueness.py` |
| `Result[T]` (governed output container) | `fvafk.algebra.core.Result` only | ✅ Yes |
| `Evidence` (governed evidence record) | `fvafk.algebra.core.Evidence` only | ✅ Yes — `dal_core.DalEvidence` is a domain object, not a kernel redefinition |
| `Residual` (governed residual record) | `fvafk.algebra.core.Residual` only | ✅ Yes |
| `Failure` (governed failure record) | `fvafk.algebra.core.Failure` only | ✅ Yes |
| `Trace` (constitutional replay trace) | `fvafk.algebra.core.Trace` only | ✅ Yes — `fvafk.c1.trace_v1.C1Trace` is a documented **pre-kernel adapter**, not a parallel kernel class |
| Inspection report shape | Domain dataclass, carried by `Result[InspectionReport]` | n/a — not a parallel kernel |
| Workflow report shape | Domain dataclass, carried by `Result[WorkflowReport]` | n/a |
| Dal/Mufrad/Murakkab evidence | Domain structure in `dal_core`, adapted at the boundary | Must not be named `Evidence` |

---

## 5. ما لا يجوز الآن (Out-of-scope for PR-ARCH0)

The following are explicitly **not** part of this PR and **must not** be added
on top of an un-unified kernel:

```text
❌ GOV1 (Governance v1)
❌ WorkUnit / WorkflowGeometry
❌ AgentPermission
❌ DashboardGovernance
❌ New gates inside gfa
❌ New extensions to dal_core
❌ A parallel "InspectionResult" / "WorkflowResult" type
```

Each of these is legitimate future work, but each one requires the authority
map declared here to be in force first.

---

## 6. خطوات ما بعد الدمج (After this PR)

1. Treat any new PR that introduces a class named `Rank` / `Result` / `Evidence`
   / `Residual` / `Failure` / `Trace` outside `fvafk.algebra` as a violation,
   unless it is added to the documented adapter list with a migration plan.
2. Resolve the items in [`KERNEL_MIGRATION_GAPS.md`](./KERNEL_MIGRATION_GAPS.md)
   one at a time, each in its own PR.
3. Only after the migration list is closed (or each entry has a tracked,
   bounded plan) may **PR-GOV1** be opened.

---

**Authoritative references**

- [`docs/ALGEBRA_KERNEL_CONSTITUTION.md`](./ALGEBRA_KERNEL_CONSTITUTION.md) — the
  "no bare output" constitution.
- [`docs/KERNEL_MIGRATION_GAPS.md`](./KERNEL_MIGRATION_GAPS.md) — the working
  list of legacy/adapter surfaces still pointing at parallel definitions.
- [`tests/test_algebra_kernel_uniqueness.py`](../tests/test_algebra_kernel_uniqueness.py)
  — the enforcement test for this map.
