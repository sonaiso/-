# PR Status Index

**Purpose**: Map actual GitHub PR numbers to planned roadmap PR identifiers

**Last Updated**: 2026-05-20

---

## Critical Distinction

**Roadmap PR Numbers** (e.g., "PR #23", "PR #24") in documentation are **planning identifiers**, not necessarily GitHub PR numbers.

**GitHub PR Numbers** are assigned sequentially by GitHub when PRs are created.

**These two numbering systems may diverge**, and this document tracks that divergence.

---

## Actual Merged GitHub PRs

| GitHub PR | Title | Merged Date | Roadmap Correspondence |
|---|---|---|---|
| #7 | MufradProof Contract | Merged | Roadmap PR #7 ✅ |
| #9 | SentenceFrameCandidate | Merged | Roadmap PR #9 ✅ |
| #10 | PreSyntaxMufradVector | Merged | Roadmap PR #10 ✅ |
| #11 | PreSyntax Interface Hardening | Merged | (Hardening of #10) |
| #12 | CaseSignMatrix | Merged | Roadmap PR #12 ✅ |
| #14 | OperatorTriggerPotential | Merged | Roadmap PR #14 ✅ |
| #16 | NahwOperatorRegistry | Merged | Roadmap PR #16 ✅ |
| #18 | OperatorCandidate | Merged | Roadmap PR #18 ✅ |
| #21 | Ordered Dal Form Governance | Merged | Roadmap PR #21 ✅ |
| #22 | Project Algebra Architecture Map | Merged | Roadmap PR #22 ✅ |
| #23 | (Not created yet) | — | (Reserved for Minimal Dal Transition) |
| #24 | (Not created yet) | — | (Reserved for future work) |
| #25 | Explain Repository Structure | Merged 2026-05-20 | ❌ No roadmap correspondence |
| #26 | Create Implementation Plan | In Progress | **This PR** (Roadmap Reconciliation) |

---

## Roadmap PRs (From PROJECT_ALGEBRA_ROADMAP.md)

| Roadmap ID | Title | Status | Actual GitHub PR |
|---|---|---|---|
| PR #22 | Project Algebra Architecture Map | ✅ Merged | GitHub PR #22 |
| PR #23 | Minimal Dal Transition Signature | 📋 Planned | (To be created) |
| PR #24 | Rank Algebra | 📋 Planned | (To be created) |
| PR #25 | Residual Algebra | 📋 Planned | (To be created) |
| PR #26 | CandidateSet Contract | 📋 Planned | (Renamed: now PR #29 in updated roadmap) |
| PR #27 | Stage-Aware NoMeaning Invariant | 📋 Planned | (Renamed: now PR #31 in updated roadmap) |

---

## Numbering Divergence Event

**What happened**:
- GitHub PRs #23-24 were not created immediately after #22
- GitHub PR #25 was created for "Explain Repository Structure" (documentation)
- GitHub PR #26 is "Create Implementation Plan" → **Became Roadmap Reconciliation**

**Resolution**:
- Roadmap PR numbers (#23, #24, #25...) remain as **planning identifiers**
- Future GitHub PRs will be created with higher numbers (likely #27+)
- This document tracks the mapping

---

## How to Use This Index

### When Reading Roadmap Documents

If you see "PR #23: Minimal Dal Transition Signature" in `PROJECT_ALGEBRA_ROADMAP.md`:
- This is a **planning identifier**
- Check this index to find the actual GitHub PR number (when created)
- Currently: "PR #23" → Not yet created

### When Creating New PRs

1. Check this index for the next available GitHub PR number
2. Map your work to the appropriate roadmap identifier
3. Update this index with the mapping
4. Update roadmap documents if needed

### When Claiming Completion

- ✅ **Correct**: "GitHub PR #22 (Roadmap PR #22: Architecture Map) is merged"
- ❌ **Wrong**: "PR #23 is complete" (without clarifying which numbering system)

---

## Governance Rules

See `ROADMAP_GOVERNANCE.md` for:
- When to use roadmap numbers vs GitHub numbers
- How to handle divergence
- Citation requirements
- Completion claim standards

---

## Future Updates

This index must be updated:
- When any GitHub PR is created that corresponds to a roadmap PR
- When any roadmap PR is renumbered or redefined
- When divergence occurs between the two numbering systems

---

**Maintained by**: Project team
**Update frequency**: On every PR creation or roadmap revision
**Canonical source**: This file is the single source of truth for PR number mapping
