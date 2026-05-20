# Roadmap Governance

**Purpose**: Define rules for roadmap numbering, completion claims, and audit certification

**Version**: 1.0.0
**Created**: 2026-05-20

---

## 1. PR Numbering Systems

### 1.1 Two Independent Systems

This project uses **two independent numbering systems**:

1. **Roadmap PR Numbers** (Planning Identifiers)
   - Examples: "PR #23", "PR #24", "PR #25"
   - Used in: `PROJECT_ALGEBRA_ROADMAP.md`, architectural documents
   - Purpose: Logical sequencing of planned work
   - Assignment: Manual, by project planners

2. **GitHub PR Numbers** (Repository Identifiers)
   - Examples: GitHub PR #25, GitHub PR #26
   - Used in: GitHub interface, git commits, `PR_STATUS_INDEX.md`
   - Purpose: Tracking actual pull requests
   - Assignment: Automatic, by GitHub

### 1.2 Divergence is Normal

These two systems **will diverge**, and this is acceptable:

```text
Roadmap PR #23 may become GitHub PR #27
Roadmap PR #24 may become GitHub PR #30
Roadmap PR #25 may become GitHub PR #31
```

**Divergence does not indicate failure**. It indicates:
- Intermediate PRs were created (hotfixes, documentation, refactoring)
- Planning was revised based on implementation learnings
- The project adapted to actual development needs

---

## 2. Citation Requirements

### 2.1 In Roadmap Documents

When writing in `PROJECT_ALGEBRA_ROADMAP.md` or similar planning documents:

✅ **Correct**:
```markdown
### PR #23: Minimal Dal Transition Signature
**Status**: Planned
**Deliverables**: ...
```

❌ **Wrong**:
```markdown
### PR #23: Minimal Dal Transition Signature
**Status**: Merged  ← Without citing actual GitHub PR number
```

### 2.2 In Completion Claims

When claiming work is complete:

✅ **Correct**:
```markdown
GitHub PR #22 (Roadmap PR #22: Architecture Map) is merged.
```

✅ **Also Correct**:
```markdown
Roadmap PR #23 (Minimal Dal Transition) is implemented in GitHub PR #27.
```

❌ **Wrong**:
```markdown
PR #23 is complete.  ← Ambiguous: which numbering system?
```

### 2.3 In Code Comments

When referencing PRs in code:

✅ **Correct**:
```python
# Implements roadmap PR #23 (Minimal Dal Transition Signature)
# Merged as GitHub PR #27 on 2026-05-25
```

❌ **Wrong**:
```python
# PR #23  ← Ambiguous
```

---

## 3. Completion vs. Definition

### 3.1 Three States

Every work item has one of three states:

| State | Definition | Evidence Required |
|---|---|---|
| **Defined** | Requirements and contracts documented | Document file path |
| **Implemented** | Code written and tests passing | GitHub PR number (merged) |
| **Certified** | Formal audit passed with reports | Audit report artifacts |

### 3.2 Claim Standards

| Claim | Requires | Evidence Format |
|---|---|---|
| "Roadmap PR #X is defined" | Documentation exists | `docs/FILENAME.md:line` |
| "Roadmap PR #X is implemented" | GitHub PR merged | `GitHub PR #Y merged on DATE` |
| "Roadmap PR #X is certified" | Audit reports pass | `reports/audit_X.json verdict: PASS` |

### 3.3 Forbidden Claims

❌ **Never claim**:
```text
"PR #X is done" without specifying which state (defined/implemented/certified)
"100% coverage" without audit report artifacts
"Dal-only certified" without Section J score ≥ 9
"Total-Coverage closed" without K.2-K.4 reports = ∅
```

---

## 4. Audit Framework vs. Passed Audit

### 4.1 Critical Distinction

```text
Checklist ≠ Certification
Audit framework ≠ Passed audit
Requirements defined ≠ Requirements met
```

### 4.2 Audit Status Levels

| Level | Definition | Evidence |
|---|---|---|
| **Level 0: No Audit** | No checklist exists | N/A |
| **Level 1: Framework Defined** | `DAL_FORMAL_AUDIT_CHECKLIST.md` exists | Document file |
| **Level 2: Partial Compliance** | Some checklist items pass | Cited evidence in checklist |
| **Level 3: Framework Complete** | All checklist items have evidence | J score 7-8 |
| **Level 4: Dal-Only Certified** | No semantic leakage, dal-only proven | J score 9-10 |
| **Level 5: Total-Coverage Closed** | All reports ∅, 100% corpus covered | K.1-K.4 artifacts + J ≥ 9 |

### 4.3 Current Status Guard

As of 2026-05-20, this project is at:

```text
✅ Level 1: Framework Defined (DAL_FORMAL_AUDIT_CHECKLIST.md exists with Section K)
❌ Level 2: Partial Compliance (checklist items not yet filled)
❌ Level 3: Framework Complete (evidence not yet generated)
❌ Level 4: Dal-Only Certified (J score not yet calculated)
❌ Level 5: Total-Coverage Closed (K reports not yet generated)
```

**Forbidden claims**:
```text
❌ "Dal-only is certified" → Requires Level 4
❌ "100% coverage achieved" → Requires Level 5
❌ "Total-Coverage closed" → Requires Level 5
❌ "Audit passed" → Requires Level 3 minimum
```

**Allowed claims**:
```text
✅ "Audit framework is defined"
✅ "Checklist exists with Total-Coverage requirements (Section K)"
✅ "Requirements are documented for dal-only certification"
```

---

## 5. Evidence Requirements

### 5.1 Every Claim Needs Evidence

| Claim Type | Evidence Type | Example |
|---|---|---|
| Code exists | File path + line range | `src/dal_core/dal_algebra.py:1-400` |
| Test passes | Test file + function | `tests/dal_core/test_dal_algebra.py::test_domain_enum` |
| PR merged | GitHub PR number + date | `GitHub PR #22 merged 2026-05-20` |
| Rule defined | Document section | `docs/DAL_ALGEBRA_SIGNATURE.md:167-182` |
| Audit item passed | Checklist reference + artifact | `DAL_FORMAL_AUDIT_CHECKLIST.md:A2 + test_semantic_leak.py` |

### 5.2 Evidence Must Be Reproducible

✅ **Reproducible**:
```markdown
Evidence: `src/dal_core/d_mufrad.py:16-29` prohibits `meaning` field
Verification: `grep -r "meaning" src/dal_core/d_mufrad.py` returns nothing
```

❌ **Not Reproducible**:
```markdown
Evidence: "I checked and there's no meaning field"
```

### 5.3 Evidence Must Be Current

- Evidence with file:line citations must be verified to still exist
- Test references must be to tests that currently pass
- PR references must be to actually merged PRs

**Update frequency**: Evidence must be re-verified:
- When cited file changes
- When roadmap is revised
- Before any completion claim
- During formal audit

---

## 6. Roadmap Revision Protocol

### 6.1 When to Revise Roadmap

Revise `PROJECT_ALGEBRA_ROADMAP.md` when:
- Implementation order changes
- New intermediate PRs are needed
- Scope of planned PR changes
- Numbering divergence occurs

### 6.2 Revision Requirements

When revising roadmap:

1. **Update `PR_STATUS_INDEX.md` first**
   - Map any new GitHub PRs to roadmap identifiers
   - Document any numbering divergence

2. **Update roadmap document**
   - Clearly mark revised sections
   - Preserve old numbering in comments if helpful
   - Update status of all affected PRs

3. **Update related documents**
   - Search for references to renumbered PRs
   - Update citations in all documents
   - Add clarifying notes where needed

4. **Create revision note**
   - Document what changed and why
   - Reference the GitHub PR that made the change
   - Update "Version" and "Last Updated" fields

### 6.3 Backward Compatibility

When renumbering:
- Old roadmap PR numbers can be preserved in comments
- Use format: `PR #X (originally planned as PR #Y)`
- Keep `PR_STATUS_INDEX.md` as canonical mapping

---

## 7. Governance Test Requirements

### 7.1 Required Governance Tests

File: `tests/dal_core/test_project_roadmap_consistency.py`

Must test:

1. **No Premature Certification**
   ```python
   def test_no_certification_claim_without_reports():
       """Prevent claiming certification without required reports"""
   ```

2. **Evidence Exists for Claims**
   ```python
   def test_completed_pr_has_github_reference():
       """Every 'merged' claim must cite GitHub PR number"""
   ```

3. **No Semantic Leakage Claims**
   ```python
   def test_no_meaning_field_in_dal_core():
       """Verify no semantic fields in dal_core dataclasses"""
   ```

### 7.2 Test Enforcement

These tests run in CI and:
- **MUST pass** before merging any roadmap update
- **MUST fail** if premature claims are made
- **MUST be updated** when governance rules change

---

## 8. Communication Guidelines

### 8.1 In Documentation

When writing docs:
- Be explicit about which numbering system you're using
- Cite evidence for every completion claim
- Distinguish between defined/implemented/certified
- Link to `PR_STATUS_INDEX.md` for clarity

### 8.2 In Commit Messages

When committing:
```text
✅ Good: "docs: implement roadmap PR #23 (Minimal Dal Transition)"
✅ Good: "feat: add rank algebra (GitHub PR #27, roadmap PR #24)"
❌ Bad: "implement PR #23" ← Which system?
```

### 8.3 In Issue Tracking

When creating issues:
```text
Title: "Implement Roadmap PR #24: Rank Algebra"
Body: "This implements roadmap PR #24 as defined in PROJECT_ALGEBRA_ROADMAP.md:116-143"
Labels: roadmap-pr-24, algebra, foundation
```

---

## 9. Audit Claim Guards

### 9.1 Certification Claims Require Artifacts

| Claim | Required Artifacts | Location |
|---|---|---|
| "Dal-only certified" | J score 9-10 + no semantic leakage | `DAL_FORMAL_AUDIT_CHECKLIST.md` Section J |
| "Total-Coverage closed" | K.1 ledger + K.2-K.4 reports = ∅ | `reports/coverage_ledger.json`, `reports/*_report.json` |
| "Audit framework complete" | All checklist items with evidence | All sections A-K filled |
| "Rank Algebra proven" | Rank algebra laws + tests pass | `src/dal_core/rank_algebra.py` + tests |

### 9.2 Report Generation Requirements

Before claiming "Total-Coverage closed":

```bash
# Must run successfully and produce ∅ reports
python -m dal_core.audit.build_ledger --corpus <path>
python -m dal_core.audit.find_holes    # → holes == []
python -m dal_core.audit.find_jumps    # → jumps == []
python -m dal_core.audit.find_leaks    # → leaks == []
```

**If any command**:
- Doesn't exist → Claim fails (tools not implemented)
- Returns non-empty → Claim fails (violations found)
- Errors → Claim fails (implementation incomplete)

### 9.3 Gradual Progress is Allowed

You can claim:
```text
✅ "10% of audit checklist complete"
✅ "Section A (Scope Guard) passes with evidence"
✅ "Working toward dal-only certification"
✅ "Audit tools under development"
```

You cannot claim:
```text
❌ "Audit complete" (without all checklist items filled)
❌ "Dal-only certified" (without J ≥ 9)
❌ "100% coverage" (without K reports ∅)
❌ "Fully proven" (without all theorems tested)
```

---

## 10. Version Control

### 10.1 Document Versioning

All governance documents must have:
```markdown
**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Change Log**: See CHANGELOG.md or git history
```

### 10.2 Breaking Changes

When governance rules change in a way that invalidates previous claims:
- Increment major version (X.0.0)
- Update all affected documents
- Create migration guide if needed
- Re-audit all completion claims

---

## Summary

**Core Principles**:

1. **Roadmap numbers ≠ GitHub numbers** (and that's OK)
2. **Checklist ≠ Certification** (framework vs. passed)
3. **Every claim requires evidence** (file:line or test or artifact)
4. **Status must be explicit** (defined/implemented/certified)
5. **Audit reports required for certification** (not just checkboxes)

**Governance Files**:
- This file: `ROADMAP_GOVERNANCE.md` (rules)
- `PR_STATUS_INDEX.md` (numbering mapping)
- `DAL_FORMAL_AUDIT_CHECKLIST.md` (certification framework)
- `test_project_roadmap_consistency.py` (enforcement)

---

**Maintained by**: Project governance team
**Applies to**: All roadmap documents, PR descriptions, completion claims
**Enforcement**: CI tests + peer review
**Updates**: Any governance change requires team consensus
