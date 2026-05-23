# Documentation Index

**Purpose**: Navigate General Cognitive Algebra project documentation

**Start Here**: If new to the project, read in this order.

---

## Quick Navigation

### 🚀 Start Here

1. **[README.md](../README.md)** - Project overview, what it is/isn't, quick start
2. **[CLAIM_BOUNDARY_AUDIT.md](CLAIM_BOUNDARY_AUDIT.md)** - Implementation status (68 claims audited)
3. **[PROJECT_DEFINITION.md](PROJECT_DEFINITION.md)** - Core laws and boundaries

### 📋 Understanding Current State

4. **[GAP_HALLUCINATION_AUDIT.md](GAP_HALLUCINATION_AUDIT.md)** - Overclaims and governance gaps (21 issues)
5. **[NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md)** - Foundation hardening (PR-F1/F2/F3)
6. **[TERMINOLOGY.md](TERMINOLOGY.md)** - Precise definitions

### 🏗️ Architecture

7. **[ARABIC_ALGEBRA_ARCHITECTURE.md](ARABIC_ALGEBRA_ARCHITECTURE.md)** - Constitution and CPB contract
8. **[ARABIC_ALGEBRA_ROADMAP.md](ARABIC_ALGEBRA_ROADMAP.md)** - Phase plan (0-5.5 implemented)
9. **[PROJECT_ALGEBRA_ARCHITECTURE_MAP.md](PROJECT_ALGEBRA_ARCHITECTURE_MAP.md)** - 11-layer architecture (A0-A10)

### 📊 Implementation Status

| Component | Status | Tests | Documentation |
|-----------|--------|-------|---------------|
| **Constitutional Foundation** | ✅ IMPLEMENTED | Result invariants, CPB, Rank policy | ARABIC_ALGEBRA_ARCHITECTURE.md |
| **General Cognitive (5/13 layers)** | ⏳ PARTIAL | 146 tests | [GFA README](../src/gfa/README.md) |
| **Arabic Algebra Foundation** | ✅ STRONG | Dal→Wadh→Mutabaqah tests | ARABIC_ALGEBRA_ROADMAP.md |
| **DAL_CORE (Pre-Semantic)** | ✅ IMPLEMENTED | MufradProof, OperatorTrigger | [SPEC_DAL_CORE.md](SPEC_DAL_CORE.md) |
| **Governance Hardening** | ⚠️ NEEDED | PR-F1/F2/F3 required | NEXT_PHASE_PLAN.md |

---

## By Topic

### Constitution & Governance

- **[ARABIC_ALGEBRA_ARCHITECTURE.md](ARABIC_ALGEBRA_ARCHITECTURE.md)** - لا مخرج عارٍ (no bare output)
- **[CLAIM_BOUNDARY_AUDIT.md](CLAIM_BOUNDARY_AUDIT.md)** - Implementation audit
- **[GAP_HALLUCINATION_AUDIT.md](GAP_HALLUCINATION_AUDIT.md)** - Governance gaps
- **[NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md)** - Foundation hardening plan

### Arabic Algebra

- **[ARABIC_ALGEBRA_ROADMAP.md](ARABIC_ALGEBRA_ROADMAP.md)** - Phase-by-phase development
- **[ARABIC_ALGEBRA_DECISION_TREE.md](ARABIC_ALGEBRA_DECISION_TREE.md)** - Worked example (كاتب)
- **[DAL_ALGEBRA_SIGNATURE.md](DAL_ALGEBRA_SIGNATURE.md)** - Dal algebra specification
- **[ATOMIC_ALGEBRA_BOUNDARY.md](ATOMIC_ALGEBRA_BOUNDARY.md)** - 𝔄₀ boundary laws

### General Cognitive Algebra

- **[GFA README](../src/gfa/README.md)** - General Foundational Algebra overview
- **[PROJECT_ALGEBRA_ARCHITECTURE_MAP.md](PROJECT_ALGEBRA_ARCHITECTURE_MAP.md)** - 11-layer map (A0-A10)
- **[GENERAL_ALGEBRA_FORMAL_SPEC_V01.md](GENERAL_ALGEBRA_FORMAL_SPEC_V01.md)** - Formal specification

### DAL_CORE (Pre-Semantic)

- **[SPEC_DAL_CORE.md](SPEC_DAL_CORE.md)** - Dal Core specification
- **[DAL_CORE_MUFRAD_PROOF.md](DAL_CORE_MUFRAD_PROOF.md)** - MufradProof details
- **[OPERATOR_TRIGGER_POTENTIAL.md](OPERATOR_TRIGGER_POTENTIAL.md)** - OperatorTrigger layer

### Testing & Validation

- **Tests Location**: `tests/` directory
  - `tests/fvafk/algebra/` - Algebra governance tests
  - `tests/gfa/` - General Cognitive Algebra tests
  - `tests/dal_core/` - DAL_CORE tests
- **Test Count**: 497+ passing
- **Coverage**: See individual README files in source directories

---

## By Audience

### New Contributors

Read in order:
1. [README.md](../README.md) - Overview
2. [CLAIM_BOUNDARY_AUDIT.md](CLAIM_BOUNDARY_AUDIT.md) - What's implemented
3. [TERMINOLOGY.md](TERMINOLOGY.md) - Key concepts
4. [NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md) - How to contribute

### Researchers

Focus on:
- [PROJECT_DEFINITION.md](PROJECT_DEFINITION.md) - Theoretical foundation
- [PROJECT_ALGEBRA_ARCHITECTURE_MAP.md](PROJECT_ALGEBRA_ARCHITECTURE_MAP.md) - 11-layer architecture
- [ARABIC_ALGEBRA_ARCHITECTURE.md](ARABIC_ALGEBRA_ARCHITECTURE.md) - Constitutional framework
- [GFA README](../src/gfa/README.md) - General Cognitive Algebra

### Developers

Start with:
- [CLAIM_BOUNDARY_AUDIT.md](CLAIM_BOUNDARY_AUDIT.md) - Implementation status
- [NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md) - Next PRs (PR-F1/F2/F3)
- [ARABIC_ALGEBRA_ROADMAP.md](ARABIC_ALGEBRA_ROADMAP.md) - Phase plan
- Source code README files

### Arabic Linguists

Recommended:
- [ARABIC_ALGEBRA_DECISION_TREE.md](ARABIC_ALGEBRA_DECISION_TREE.md) - Worked example
- [DAL_ALGEBRA_SIGNATURE.md](DAL_ALGEBRA_SIGNATURE.md) - Dal algebra
- [ATOMIC_ALGEBRA_BOUNDARY.md](ATOMIC_ALGEBRA_BOUNDARY.md) - Atomic analysis
- [SPEC_DAL_CORE.md](SPEC_DAL_CORE.md) - Pre-semantic layers

---

## Implementation Audits

### Current Status Audits

- **[CLAIM_BOUNDARY_AUDIT.md](CLAIM_BOUNDARY_AUDIT.md)** - 68 claims audited (2026-05-23)
- **[GAP_HALLUCINATION_AUDIT.md](GAP_HALLUCINATION_AUDIT.md)** - 21 issues identified (2026-05-23)
- **[GFA_BASELINE_AFTER_PR53.md](GFA_BASELINE_AFTER_PR53.md)** - GFA audit after PR #53

### Phase Completions

- **[SPRINT2_COMPLETION_SUMMARY.md](SPRINT2_COMPLETION_SUMMARY.md)** - Sprint 2 summary
- **[D1_STATUS_POST_PR32.md](D1_STATUS_POST_PR32.md)** - D1 status after PR #32
- **[DAL_CORE_PHASE2.5_STATUS.md](DAL_CORE_PHASE2.5_STATUS.md)** - DAL_CORE Phase 2.5

### PR Summaries

- **[PR_L4_DAL_MADLUL_BINDING_SUMMARY.md](PR_L4_DAL_MADLUL_BINDING_SUMMARY.md)** - Dal/Madlul binding (PR #64)
- **[PR_L5A_WADH_GEOMETRY_SUMMARY.md](PR_L5A_WADH_GEOMETRY_SUMMARY.md)** - Wadh geometry (PR #65)
- **[PR_L5B_WADH_GATE_SUMMARY.md](PR_L5B_WADH_GATE_SUMMARY.md)** - WadhGate (PR #66)
- **[PR_L6A_MUTABAQAH_GATE_SUMMARY.md](PR_L6A_MUTABAQAH_GATE_SUMMARY.md)** - Mutabaqah (PR #67)
- **[PR_G1_MEMORY_GEOMETRY_SUMMARY.md](PR_G1_MEMORY_GEOMETRY_SUMMARY.md)** - Memory geometry

---

## Roadmaps & Plans

### Active Roadmaps

- **[NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md)** - **START HERE** for next work
- **[ARABIC_ALGEBRA_ROADMAP.md](ARABIC_ALGEBRA_ROADMAP.md)** - Arabic algebra phases
- **[PROJECT_ALGEBRA_ROADMAP.md](PROJECT_ALGEBRA_ROADMAP.md)** - Overall project plan

### Completed Plans

- Phase 0-5.5 of Arabic Algebra (see ARABIC_ALGEBRA_ROADMAP.md)
- Layers -2 through 2 of General Cognitive Algebra (see GFA README)
- D0-D7 of DAL_CORE (see SPEC_DAL_CORE.md)

---

## Critical Documents

### Must Read Before Contributing

1. **[PROJECT_DEFINITION.md](PROJECT_DEFINITION.md)** - Core laws
2. **[CLAIM_BOUNDARY_AUDIT.md](CLAIM_BOUNDARY_AUDIT.md)** - Current status
3. **[NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md)** - Next PRs (PR-F1/F2/F3)
4. **[TERMINOLOGY.md](TERMINOLOGY.md)** - Precise definitions

### Forbidden Claims

See [PROJECT_DEFINITION.md - Forbidden Claims](PROJECT_DEFINITION.md#forbidden-claims):
- ❌ Complete General Cognitive Algebra (only 5/13 layers)
- ❌ Full semantic understanding (Ifādah/Murad/Hukm not implemented)
- ❌ Production NLP tool (research implementation)

### Allowed Claims

See [PROJECT_DEFINITION.md - Allowed Claims](PROJECT_DEFINITION.md#allowed-claims):
- ✅ General Cognitive Algebra foundation (5/13 layers)
- ✅ Constitutional enforcement (no bare output, CPB, rank discipline)
- ✅ Arabic as revealing model (first testbed)

---

## Documentation Status

| Document | Status | Last Updated | Verified |
|----------|--------|--------------|----------|
| README.md | ✅ Current | 2026-05-23 (PR-F0) | Yes |
| PROJECT_DEFINITION.md | ✅ Current | 2026-05-23 (PR-F0) | Yes |
| CLAIM_BOUNDARY_AUDIT.md | ✅ Current | 2026-05-23 (PR-F0) | Yes |
| GAP_HALLUCINATION_AUDIT.md | ✅ Current | 2026-05-23 (PR-F0) | Yes |
| NEXT_PHASE_PLAN.md | ✅ Current | 2026-05-23 (PR-F0) | Yes |
| TERMINOLOGY.md | ✅ Current | 2026-05-23 (PR-F0) | Yes |
| ARABIC_ALGEBRA_ROADMAP.md | ⚠️ Needs update | Pre-PR-F0 | Partial (Phase 5 overclaim) |
| PROJECT_ALGEBRA_ARCHITECTURE_MAP.md | ✅ Current | Planning doc | Yes |

---

## Quick Links

### Source Code

- [src/fvafk/algebra/](../src/fvafk/algebra/) - Arabic Algebra implementation
- [src/gfa/](../src/gfa/) - General Foundational Algebra
- [src/dal_core/](../src/dal_core/) - Pre-Semantic Dal Algebra

### Tests

- [tests/fvafk/algebra/](../tests/fvafk/algebra/) - Algebra tests
- [tests/gfa/](../tests/gfa/) - GFA tests
- [tests/dal_core/](../tests/dal_core/) - DAL_CORE tests

### Package Metadata

- [pyproject.toml](../pyproject.toml) - Package configuration
- [requirements.txt](../requirements.txt) - Dependencies

---

## External Resources

- **GitHub Repository**: https://github.com/sonaiso/Eqratech_Hussein_Hiyassat_Project
- **Package Name**: `bayan-fvafk`
- **License**: MIT
- **Python**: 3.10+

---

**Last Updated**: 2026-05-23 (PR-F0)
**Status**: Documentation governance reset complete
**Next Action**: Implement PR-F1 (Residual Taxonomy)
