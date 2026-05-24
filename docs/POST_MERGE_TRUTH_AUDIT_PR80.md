# Post-Merge Architectural Truth Audit — PR #80

**Status:** Truth correction (no runtime additions)
**Subject:** PR #80, merged with the title and body of **GOV1**
**Author law invoked:** *Prior information ≠ prior opinion*. The repository's own merge history is itself a piece of prior information; when its name does not match the diff, that record must be governed and corrected.

---

## 1. Summary

PR #80 was merged successfully **as code**. The build is green, the tests
listed in the PR body pass, and the CodeQL scan reports no alerts. As a
hardening change, it is sound.

However, the **title and body of PR #80 overstate its scope**. They claim to
deliver **GOV1** — the runtime Project Operating System layer composed of
`WorkUnit`, `AgentPermission`, and `DashboardGovernance`, together with the
admission helpers `check_work_unit.py` and `verify_pr_admission.py`. The
actual diff contains none of these artifacts.

If left unchallenged, the merged record acts as **contaminated prior
information**: any future agent that reads `git log` or the GitHub PR list
will start from the false premise that "GOV1 is already done." This document
records the correction so that future work begins from the true rank of the
merged artifact, not its label.

---

## 2. Actual Delivered Scope

The files changed by PR #80 (and the prior fixes it consolidated) fall under
the following sub-PRs, all of which are real and accepted:

### 2.1 PR-A2 — CI visibility and prior-information safety hardening

- CI workflow changes that surface failing jobs and protect the
  `prior-information` test path.
- Prior-information related repairs in `src/gfa/foundations/prior_information/`
  and adjacent tests.

### 2.2 PR-CL1 — Governed Code Learning Loop MVP

- `src/fvafk/algebra/code_learning_loop.py` and `code_learning.py`.
- Tests under `tests/fvafk/algebra/test_code_learning_loop*.py`.

### 2.3 PR-INS1 (partial) — Governed Inspection Algebra core

- `src/fvafk/algebra/governance/inspection.py` defining `InspectionArtifact`,
  `InspectionFinding`, `InspectionResidual`, `InspectionResult`, and
  `InspectionResidualKind`.
- Integration in `tools/project_audit/check_architectural_admission.py`
  through `_check_pr_governed` / `_validate_check_content_governed`.
- Tests: `tests/fvafk/algebra/test_inspection_algebra.py`,
  `tests/tools/test_architectural_admission.py` (14/14 passing).

### 2.4 Algebra kernel uniqueness notes/tests

- Adjustments and uniqueness checks in `rank.py`, golden/specificity tests
  for the inspection layer.

---

## 3. Not Delivered (despite the GOV1 label)

The following GOV1 components are **not** present anywhere in PR #80's diff
and are **not** yet implemented in the repository:

- `WorkUnit` runtime model — there is no `src/.../work_unit.py` or
  equivalent class.
- `AgentPermission` runtime model — no permission/capability registry.
- `DashboardGovernance` — no governed dashboard module.
- `tools/project_audit/check_work_unit.py` — does not exist.
- `tools/project_audit/verify_pr_admission.py` — does not exist.
- Full *Project Operating System GOV1* runtime — i.e., the layer that would
  govern who can ship what under which evidence — is **unimplemented**.

The reader can verify this directly:

```bash
git ls-files | grep -E "work_unit|agent_permission|dashboard_governance|check_work_unit|verify_pr_admission"
# expected output: (empty)
```

---

## 4. Truth Rank of PR #80

Following the constitutional rank vocabulary used elsewhere in this
repository:

| Claim                                            | Rank        | Justification                                                                 |
|--------------------------------------------------|-------------|-------------------------------------------------------------------------------|
| "PR #80 is a successful merge"                   | CERTIFIED   | Code merged, tests pass, CodeQL clean.                                        |
| "PR #80 delivers A2 / CL1 / INS1 (partial)"      | LICENSED    | Files in the diff match the descriptions in §2.                                |
| "PR #80 delivers GOV1 runtime"                   | REFUTED     | No `WorkUnit`, `AgentPermission`, `DashboardGovernance`, or admission helpers in the diff. |
| "GOV1 is therefore complete in this repository"  | REFUTED     | Follows from the line above.                                                  |

The merged PR is **valid hardening** but **invalid as a GOV1 acceptance
record**.

---

## 5. Why this audit exists *before* ARCH0

The natural next step in the roadmap is `ARCH0: Kernel Authority Map`,
followed by completing INS1 and starting the real GOV1. None of those steps
can begin from a clean prior if the project's own history says
"GOV1 already merged." Per the project's own rule:

> Prior information must be governed like any other artifact: it requires
> evidence, rank, and trace. An ungoverned `git log` entry that misnames its
> diff becomes ungoverned prior **opinion**.

Therefore this audit is sequenced **before** ARCH0:

```text
PR-POST80 (this audit)  →  ARCH0  →  INS1-complete  →  WF1  →  GOV1-real  →  A3
```

---

## 6. Scope of this PR (PR-POST80)

This PR is intentionally narrow:

- Adds `docs/POST_MERGE_TRUTH_AUDIT_PR80.md` (this file).
- Adds `docs/GOVERNANCE_ROADMAP.md` with the corrected ordering.
- Adds `tests/tools/test_claim_evidence_alignment.py` to prevent recurrence
  of the same class of error: PR body claims a file that is not in the
  changed-files set ⇒ `CLAIM_INFLATION` residual.

It does **not** add `WorkUnit`, `AgentPermission`, `DashboardGovernance`, or
any other runtime governance object. Those belong to `GOV1-real` and must be
proposed under their own admission check.

---

## 7. Verification Commands

```bash
# Evidence that GOV1 runtime artifacts are absent
git ls-files | grep -E "work_unit|agent_permission|dashboard_governance|check_work_unit|verify_pr_admission" || echo "ABSENT"

# Existing tests remain green
pytest tests/tools/test_architectural_admission.py -q -ra
pytest tests/tools/test_claim_evidence_alignment.py -q -ra
pytest tests/fvafk/algebra/test_inspection_algebra.py -q -ra
```

---

**Conclusion.** PR #80 succeeded as code and failed as a label. This document
corrects the label so that the next step — `ARCH0` and then a *real* GOV1 —
starts from the true prior, not from the merged opinion.
