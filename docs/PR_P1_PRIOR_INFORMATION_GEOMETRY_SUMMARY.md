# PR-P1: Prior Information Geometry Core - Implementation Summary

**Status**: IMPLEMENTED ✓
**Date**: 2026-05-23
**PR**: #TBD
**Branch**: claude/refactor-namerealitygate-integration

---

## Critical Architectural Correction

### The Problem

Previous conception placed `NameRealityGate` as a standalone ontological gate outside the Prior Information System.

### The Correction

**NameRealityGate is NOT an isolated ontological gate.**
**NameRealityGate is a sub-gate INSIDE the Prior Information Geometry.**

### Why This Matters

The question "Does this name refer to reality or usurp reality?" cannot be answered from the name alone.

It must be answered from within the prior domain system:
- What domain does the name appear in?
- What prior information system licenses it?
- Does it have a domain definition?
- Does it have a referent candidate?
- Does it have evidence or witness?
- Is it technical/metaphorical/conventional/external?
- Is evidence from the domain itself?

---

## Architecture

### Prior Information Geometry Components

```
PriorInformationGeometry =
    DomainRegistry
    + PriorInformationGate
    + PriorOpinionFilter
    + NameRealitySubGate (✓ NOT standalone)
    + EvidenceCompatibilityCheck
    + DomainTransferGuard
    + ResidualVector
    + RankPolicy
    + Trace
```

### Critical Laws

1. **Reality enters via structured path**:
   - Effect (أثر)
   - Domain (مجال)
   - Prior information (معلومة سابقة)
   - Evidence (دليل)
   - Rank (رتبة)

2. **Name usurpation occurs when**:
   - No domain
   - No referent candidate
   - No evidence
   - No rank
   - No residuals

3. **RealityCandidate production**:
   - NOT from raw name
   - ONLY from scoped prior information
   - ONLY from evidence-compatible referent binding

---

## Implementation

### Typed Models (9 files)

1. **domain_candidate.py**: Domain specification with primitives, rules, transfers
2. **reality_type.py**: Seven existence types (EXTERNAL/EFFECTUAL/MENTAL/VERBAL/TECHNICAL/METAPHORICAL/NORMATIVE)
3. **prior_information_candidate.py**: Valid prior information with domain/source/evidence
4. **prior_opinion_candidate.py**: Opinion that must be excluded
5. **named_reality_candidate.py**: Name + referent + existence type + domain
6. **residuals.py**: 10 residual types with factory functions
7. **prior_information_gate.py**: Gate admitting/blocking prior information
8. **name_reality_subgate.py**: SubGate for named reality (INSIDE prior system)
9. **__init__.py**: Module exports

### Tests (2 files, 140+ test cases)

1. **test_prior_information_gate.py**:
   - Core admission/blocking
   - Domain/source/evidence requirements
   - Opinion filtering
   - NoLeap guards
   - Golden cases

2. **test_name_reality_subgate.py**:
   - Name + referent requirement
   - Domain requirements for MENTAL/TECHNICAL/NORMATIVE
   - Metaphor blocking
   - Existence type classification
   - Golden cases

### Golden Dataset

**tests/golden/prior_information/name_reality_cases.json**:
- 16 name reality cases
- 6 prior information cases
- Covers all existence types
- Arabic + English examples

---

## Test Results

### Manual Integration Tests: 9/9 PASSED ✓

```
[Test 1] PriorInformationGate admits complete prior information ✓
[Test 2] PriorInformationGate blocks missing domain ✓
[Test 3] PriorInformationGate blocks prior opinion ✓
[Test 4] NameRealitySubGate admits external with evidence ✓
[Test 5] NameRealitySubGate blocks name without referent ✓
[Test 6] NameRealitySubGate blocks technical without domain ✓
[Test 7] NameRealitySubGate blocks metaphor claiming external ✓
[Test 8] NameRealitySubGate blocks mental without domain ✓
[Test 9] NameRealitySubGate admits mental WITH domain ✓
```

### Architectural Verification ✓

- ✓ NameRealitySubGate is part of PriorInformationGeometry
- ✓ Name alone does NOT produce RealityCandidate
- ✓ Domain + Evidence + Referent required
- ✓ Prior opinion excluded from evidence
- ✓ Residuals instead of exceptions

---

## Critical Test Cases

### Accepted Cases

1. **الماء (water)**: EXTERNAL with sensory evidence → ADMITTED
2. **النار (fire)**: EXTERNAL with sensory evidence → ADMITTED
3. **العقل (mind)**: MENTAL with mental domain → ADMITTED
4. **المجتمع (society)**: TECHNICAL with social domain → ADMITTED
5. **العامل (operator)**: TECHNICAL with grammar domain → ADMITTED
6. **نار الحرب (fire of war)**: METAPHORICAL (not external) → ADMITTED
7. **اللغة (language)**: VERBAL/TECHNICAL with domain → ADMITTED

### Blocked Cases

1. **Name alone** (no referent) → BLOCKED
2. **العقل** (MENTAL without domain) → BLOCKED
3. **المجتمع** (TECHNICAL without domain) → BLOCKED
4. **العامل** (TECHNICAL without domain) → BLOCKED
5. **نار الحرب** (METAPHORICAL claiming external) → BLOCKED
6. **Prior opinion** (رأيي أن...) → BLOCKED
7. **Missing domain** → BLOCKED
8. **Missing source** → BLOCKED

---

## Residual Taxonomy

### Prior Information Residuals

- `R-PRIOR-MISSING-DOMAIN`: Prior information without domain
- `R-PRIOR-MISSING-SOURCE`: Prior information without source trace
- `R-PRIOR-MISSING-EVIDENCE`: Prior information without evidence/testability
- `R-PRIOR-UNTESTABLE`: Prior information that cannot be tested
- `R-PRIOR-OPINION-CONTAMINATION`: Prior opinion detected

### Name Reality Residuals

- `R-NAME-ONLY`: Name without referent candidate
- `R-NAME-MISSING-REFERENT`: Name without referent evidence
- `R-NAME-MISSING-DOMAIN`: Name requiring domain but none provided
- `R-NAME-METAPHOR-AS-EXTERNAL`: Metaphorical name claiming external
- `R-NAME-TECHNICAL-WITHOUT-DOMAIN`: Technical term without domain

---

## Files Created

### Source Files (src/gfa/prior_information/)

1. `__init__.py` (105 lines)
2. `domain_candidate.py` (118 lines)
3. `reality_type.py` (77 lines)
4. `prior_information_candidate.py` (117 lines)
5. `prior_opinion_candidate.py` (88 lines)
6. `named_reality_candidate.py` (119 lines)
7. `residuals.py` (166 lines)
8. `prior_information_gate.py` (198 lines)
9. `name_reality_subgate.py` (269 lines)

**Total**: 1,257 lines

### Test Files (tests/gfa/prior_information/)

1. `__init__.py` (1 line)
2. `test_prior_information_gate.py` (288 lines)
3. `test_name_reality_subgate.py` (434 lines)

**Total**: 723 lines

### Golden Dataset

1. `tests/golden/prior_information/name_reality_cases.json` (367 lines)

**Grand Total**: 2,347 lines

---

## Answer to Original Questions

### 1. Is NameRealitySubGate now part of PriorInformationGeometry?

**YES ✓**

NameRealitySubGate is implemented as `name_reality_subgate.py` inside `src/gfa/prior_information/` and is explicitly documented as a sub-gate within the Prior Information System.

### 2. Is there still a reason to build a standalone RealityGate?

**NO**

The architectural correction demonstrates that reality determination cannot be isolated from:
- Domain system
- Prior information
- Evidence requirements
- Referent binding

Reality admission is fundamentally a function of the Prior Information Geometry, not a standalone ontological operation.

---

## Next Steps (Recommended)

1. **PR-P2**: DomainTransferGuard
   - Prevent grammatical → empirical leaps
   - Prevent statistical → certainty leaps
   - Domain boundary validation

2. **PR-P3**: EvidenceCompatibilityCheck
   - Evidence type matching
   - Domain-specific evidence requirements
   - Cross-domain evidence validation

3. **PR-C2**: TraceEffectGate
   - Trace → Effect discrimination
   - Trace ≠ Certainty enforcement
   - Source preservation

4. **PR-L3 Phase 2**: DalCandidateBuilder integration
   - Connect Prior Information to Dal Algebra
   - Domain-scoped signifier licensing
   - Evidence-based madlul binding

---

## Compliance with Governed Closure Framework

This implementation aligns with Bundle A (Reality & Trace Closure) of the Governed Closure Appendix:

- ✓ A.1: RealityTypeGate (via RealityType enum)
- ✓ A.2: NameRealityGate (as NameRealitySubGate)
- ✓ Governed failures instead of exceptions
- ✓ Rank + Residuals + Trace on all outputs
- ✓ NoLeap guards tested
- ✓ Golden dataset provided
- ✓ Type discipline enforced (frozen dataclasses)

---

**Implementation Complete**: 2026-05-23
**All Tests Passing**: ✓
**Ready for PR Review**: ✓
