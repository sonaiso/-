# Governance Roadmap

**Status:** authoritative ordering after [PR-POST80 truth audit](./POST_MERGE_TRUTH_AUDIT_PR80.md)
**Rule:** every step here must be proposable as a single PR with its own
admission check; the *label* of a PR must match its *diff*.

This roadmap supersedes any ordering implied by the title or body of PR #80.
PR #80 is recorded as A2 + CL1 + INS1 (partial); the GOV1 label it carried
is not honored by this document because the corresponding runtime artifacts
were not delivered. See `POST_MERGE_TRUTH_AUDIT_PR80.md`.

---

## Order of Work

```text
ARCH0           Kernel Authority Map
INS1-complete   Governed Inspection Checker, fully governed (no bare booleans)
WF1             Workflow Geometry Specification
GOV1-real       WorkUnit + AgentPermission + DashboardGovernance (runtime)
A3              Actual PR body/diff admission enforcement
```

Each step is gated on the previous one. Re-ordering requires a new audit
document of the same shape as `POST_MERGE_TRUTH_AUDIT_PR80.md`.

---

## ARCH0 — Kernel Authority Map

**Goal.** Produce the *single source of truth* for which module is the
authority for which decision. The map is data, not code: a graph of
(decision → owning module → admission rule).

**Deliverables.**
- `docs/KERNEL_AUTHORITY_MAP.md` listing every governing module and the
  decisions it owns (e.g., rank, residuals, inspection, prior information).
- A static check that fails if two modules claim the same decision.

**Out of scope.** Any runtime change to who emits a decision; this step is
purely descriptive and locks the current authority layout.

---

## INS1-complete — Governed Inspection Checker

**Goal.** Bring `tools/project_audit/check_architectural_admission.py` to
full INS1 compliance: every public output is an `InspectionResult` (or its
documented legacy projection); no bare booleans remain on any code path,
including legacy fallback.

**Deliverables.**
- Removal of the residual legacy branch in `check_pr_description` or its
  explicit conversion through `to_legacy_validation_result`.
- Golden tests that exercise both branches and prove identical externally
  observable behavior.

**Out of scope.** New checks; this is a closure exercise, not an extension.

---

## WF1 — Workflow Geometry Specification

**Goal.** Specify the geometry of CI workflows themselves as a governed
artifact: each workflow has a typed role (admission gate, hardening,
publication, audit), and a workflow cannot mix roles silently.

**Deliverables.**
- `docs/WORKFLOW_GEOMETRY.md`.
- A linter that classifies each `.github/workflows/*.yml` file and refuses
  unclassified or mixed-role workflows.

**Out of scope.** Replacing existing workflows; only classification + linter.

---

## GOV1-real — WorkUnit + AgentPermission + DashboardGovernance

**Goal.** Implement the runtime governance layer that PR #80 *named* but did
not *deliver*.

**Deliverables.**
- `WorkUnit` runtime model: a typed unit of work with explicit inputs,
  evidence, residuals, rank, and trace.
- `AgentPermission` runtime model: a typed capability bound to a `WorkUnit`
  class; an agent without the required permission cannot emit a `WorkUnit`
  of that class.
- `DashboardGovernance`: a read-only governed projection of the above for
  inspection (no side effects, no rank inflation).
- `tools/project_audit/check_work_unit.py` and
  `tools/project_audit/verify_pr_admission.py` admission helpers.
- A `MinimalSufficiencyCheck` block in the PR proving this is the smallest
  form of the governance runtime, with at least two existing constructs
  examined and rejected with rank-/trace-specific reasons.

**Hard precondition.** ARCH0 and INS1-complete must both be merged first so
that GOV1-real has a stable authority map and a fully governed inspection
checker to lean on.

---

## A3 — PR body / diff admission enforcement

**Goal.** Close the loop that PR-POST80 opened: every PR's body claims must
align with its diff. A PR that claims a file or class not present in
`changed_files` must fail admission with a `CLAIM_INFLATION` residual.

**Deliverables.**
- Promotion of `tests/tools/test_claim_evidence_alignment.py` from a local
  fixture-based test to a CI step that runs against the actual GitHub PR
  metadata.
- Integration into the architectural-admission workflow.

**Hard precondition.** GOV1-real, because A3 needs a real `WorkUnit` and
`AgentPermission` to attach the admission decision to.

---

## Invariants Across the Roadmap

1. **Label = Diff.** No PR is admitted whose title or body claims work not
   present in its diff.
2. **No bare output.** Every governance decision returns an
   `InspectionResult`-shaped object with evidence, rank, residuals, trace.
3. **Prior information is governed.** The merge history itself is a piece
   of prior information; if it is wrong, it is corrected by an audit PR
   (the shape of PR-POST80), not by re-titling.
4. **No leapfrog.** Each step here must be merged before the next is
   proposed.
