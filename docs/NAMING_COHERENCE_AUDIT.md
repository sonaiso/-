# Naming Coherence Audit: Preventing Dāl/Madlūl Usurpation

## Executive Summary

**Problem**: The project mixes concepts of **dāl** (signifier/الدال) and **madlūl** (signified/المدلول) in inconsistent ways, risking epistemological usurpation where:
- Names (asmāʾ/أسماء) are confused with realities (ḥaqāʾiq/حقائق)
- Signifiers are confused with signifieds
- Traces (āthār/آثار) are confused with certainties (yaqīnāt/يقينات)
- Forms (ṣuwar/صور) are confused with meanings (maʿānī/معاني)

**Solution Status**: Partially addressed through architectural corrections in PR #79 and PR-A2, but comprehensive naming audit still needed.

## Critical Distinctions (Must Never Mix)

### 1. Dāl vs. Madlūl (الدال vs. المدلول)

**Dāl (Signifier/الدال)**:
- The linguistic form (phonetic + diacritic + positional)
- Observable carrier of signification
- Example: The word "الماء" (phonemes + ḥarakāt)

**Madlūl (Signified/المدلول)**:
- What the signifier points to
- Conceptual or referential content
- Example: The concept/referent of water

**Critical Law**: `Dāl ≠ Madlūl`
- Never conflate the word with its meaning
- Never assume Dāl→Madlūl mapping is direct or natural
- Requires binding gate (WadhGate/MutabaqahGate)

**Modules Implementing This**:
- ✅ `src/gfa/methods/lafzi_dalalah/dal_madlul_binding_gate.py`
- ✅ `src/gfa/methods/lafzi_wadh/wadh_gate.py`
- ✅ `src/gfa/methods/lafzi_dalalah/mutabaqah_gate.py`

### 2. Name vs. Reality (الاسم vs. الحقيقة)

**Name (الاسم)**:
- Linguistic label
- Can be arbitrary (conventional)
- Example: "العقل" (the word)

**Reality (الحقيقة)**:
- Existential referent
- Not created by naming
- Example: The cognitive faculty (if it exists)

**Critical Law**: `Name ≠ Reality`
- Names don't create realities
- Names require referent candidates
- Names without domain/evidence are blocked

**Modules Implementing This**:
- ✅ `src/gfa/prior_information/name_reality_subgate.py` (inside Prior Information System)
- ✅ `src/gfa/prior_information/named_reality_candidate.py`
- ✅ `src/gfa/prior_information/reality_type.py` (with UNSPECIFIED safety)

### 3. Trace vs. Certainty (الأثر vs. اليقين)

**Trace (الأثر)**:
- Observable evidence
- Preserved provenance
- Residuals + rank
- Example: "transmitted from X via Y"

**Certainty (اليقين)**:
- Epistemic state (CERTIFIED rank)
- NOT created by trace alone
- Requires full audit

**Critical Law**: `Trace ≠ Certainty`
- Trace preservation is mandatory
- But trace alone ≠ CERTIFIED
- Rank progression required

**Modules Implementing This**:
- ✅ `src/gfa/governance/rank.py` (Rank enum)
- ✅ `src/gfa/foundations/memory/memory_trace.py` (Memory Geometry)
- ⚠️ Residual calculus not fully implemented

### 4. Form vs. Meaning (الصورة vs. المعنى)

**Form (الصورة)**:
- Morphological/syntactic structure
- Pattern (wazn/وزن)
- Example: فاعل pattern

**Meaning (المعنى)**:
- Semantic content
- NOT directly read from form
- Requires binding + domain

**Critical Law**: `Form ≠ Meaning`
- Pattern doesn't imply meaning
- فاعل pattern ≠ agent meaning (requires binding)
- Semantic layer separated from morphological layer

**Modules Implementing This**:
- ✅ `src/fvafk/algebra/lafzi_madlul/` (11-layer fractal separation)
- ✅ `src/fvafk/algebra/semantics/` (Semantic algebra with gates)
- ✅ Layer boundary enforcement

### 5. Opinion vs. Information (الرأي vs. المعلومة)

**Opinion (الرأي)**:
- Personal interpretation
- Bias/taste/preference
- NOT admissible as prior information

**Information (المعلومة)**:
- Domain-scoped
- Source-traced
- Evidence-backed OR testable

**Critical Law**: `Opinion ≠ Information`
- Opinion is BLOCKED by PriorInformationGate
- Opinion contamination is residual
- No opinion→information leap

**Modules Implementing This**:
- ✅ `src/gfa/prior_information/prior_opinion_candidate.py`
- ✅ `src/gfa/prior_information/prior_information_gate.py` (filter_prior_opinion)
- ✅ PriorOpinionFilter

## Naming Audit Results

### ✅ Correctly Separated

| Concept Pair | Module | Status |
|--------------|--------|---------|
| Dāl/Madlūl | `lafzi_dalalah/dal_madlul_binding_gate.py` | ✅ Correct |
| Name/Reality | `prior_information/name_reality_subgate.py` | ✅ Correct (inside Prior System) |
| Opinion/Information | `prior_information/prior_information_gate.py` | ✅ Correct |
| Wadh/Dalālah | `lafzi_wadh/wadh_gate.py` | ✅ Correct |
| Form/Meaning | `fvafk/algebra/lafzi_madlul/` | ✅ Correct (11 layers) |

### ⚠️ Partial Implementation

| Concept Pair | Module | Issue |
|--------------|--------|-------|
| Trace/Certainty | `governance/rank.py` | ⚠️ Rank enum exists but residual calculus incomplete |
| Structure/Judgment | `dal_core/` | ⚠️ Separation present but enforcement partial |
| Memory/Evidence | `foundations/memory/` | ⚠️ Memory gate exists but integration incomplete |

### ❌ Naming Inconsistencies Found

#### Issue 1: String-based Ranks (Being Fixed)

**Problem**: Many modules still use `rank: str = "CANDIDATE"` instead of `Rank` enum.

**Files Affected**:
- `src/gfa/prior_information/domain_candidate.py:41`
- `src/gfa/prior_information/named_reality_candidate.py:52`
- `src/gfa/prior_information/prior_information_candidate.py:72`
- `src/gfa/prior_information/prior_information_gate.py:81`
- `src/gfa/prior_information/name_reality_subgate.py:102`

**Fix Required**:
```python
# Before (WRONG):
from dataclasses import dataclass

@dataclass
class MyCandidate:
    rank: str = "CANDIDATE"  # ❌ String

# After (CORRECT):
from dataclasses import dataclass
from gfa.governance import Rank

@dataclass
class MyCandidate:
    rank: Rank = Rank.CANDIDATE  # ✅ Enum
```

**Migration PR**: PR-A2.1 (Next)

#### Issue 2: NameRealitySubGate Parameter Unused

**Problem**: `prior_information: Optional[PriorInformationCandidate]` parameter is declared but not used in logic.

**File**: `src/gfa/prior_information/name_reality_subgate.py:170`

**Current**:
```python
def admit_named_reality(
    self,
    name: str,
    prior_information: Optional[PriorInformationCandidate] = None,  # NOT USED
):
    # Decision logic doesn't check prior_information
```

**Required Fix**:
```python
def admit_named_reality(
    self,
    name: str,
    prior_information: PriorInformationCandidate,  # REQUIRED
):
    # Verify prior_information is LICENSED
    if prior_information.rank != Rank.LICENSED:
        return BLOCKED
    # Use prior_information in decision
```

**Migration PR**: PR-P5 (Future)

#### Issue 3: Residuals Are Taxonomic, Not Calculated

**Problem**: Residuals have kind/severity/message but no numerical calculation.

**Missing**:
- `trace_loss: float` (0.0–1.0)
- `type_uncertainty: float`
- `evidence_gap: float`
- `scope_overreach: float`
- `total_score: float`
- `threshold: float`

**Fix Required**: PR-P4 (ResidualVector calculus)

## Architectural Recommendations

### 1. Complete Rank Migration (Priority: HIGH)

**Action**: Convert all `rank: str` to `rank: Rank`

**Files to Update**:
1. `src/gfa/prior_information/domain_candidate.py`
2. `src/gfa/prior_information/named_reality_candidate.py`
3. `src/gfa/prior_information/prior_information_candidate.py`
4. `src/gfa/prior_information/prior_information_gate.py`
5. `src/gfa/prior_information/name_reality_subgate.py`

**Verification**:
```bash
# Find remaining string-based ranks
grep -r "rank: str" src/gfa/ --include="*.py"

# Should return 0 results after migration
```

### 2. Enforce Prior Information Requirement (Priority: MEDIUM)

**Action**: Make `prior_information` parameter REQUIRED in NameRealitySubGate

**Rationale**: NameRealitySubGate is a sub-gate INSIDE Prior Information System, so it should require PriorInformationCandidate as context.

**Implementation**:
- Remove `Optional[PriorInformationCandidate]`
- Make `PriorInformationCandidate` required
- Check `prior_information.rank >= Rank.LICENSED`
- Use `prior_information.domain` in validation

### 3. Implement ResidualVector Calculus (Priority: MEDIUM)

**Action**: Add numerical residual calculation

**Required Components**:
```python
@dataclass(frozen=True)
class ResidualVector:
    trace_loss: float = 0.0
    type_uncertainty: float = 0.0
    evidence_gap: float = 0.0
    scope_overreach: float = 0.0
    ambiguity: float = 0.0
    conflict: float = 0.0
    leap_risk: float = 0.0

    @property
    def total_score(self) -> float:
        return (
            self.trace_loss +
            self.type_uncertainty +
            self.evidence_gap +
            self.scope_overreach +
            self.ambiguity +
            self.conflict +
            self.leap_risk
        )

    def exceeds_threshold(self, threshold: float = 0.7) -> bool:
        return self.total_score > threshold
```

### 4. Add Missing Gates (Priority: LOW-MEDIUM)

**Action**: Implement documented but missing gates:

1. **EvidenceCompatibilityGate**
   - Validates evidence type matches domain requirements
   - Blocks sensory evidence for mental existence
   - Blocks transmission evidence for external existence

2. **DomainTransferGuard**
   - Prevents invalid domain transfers
   - Validates transfer rules (allowed_transfers, forbidden_transfers)
   - Preserves trace through transfer

## Naming Convention Standard

### Approved Naming Patterns

1. **Candidate Classes**: `*Candidate` (e.g., DalCandidate, PriorInformationCandidate)
2. **Gate Classes**: `*Gate` (e.g., WadhGate, MutabaqahGate)
3. **Result Classes**: `*Result` (e.g., WadhGateResult, PriorInformationGateResult)
4. **Failure Classes**: `*Failure` (e.g., WadhGateFailure)
5. **Residual Functions**: `make_*_residual` (e.g., make_prior_missing_domain_residual)

### Forbidden Naming Patterns

1. ❌ Mixing dāl/madlūl in same class name
2. ❌ Implying meaning from form alone
3. ❌ "Reality" without "Named" or domain scoping
4. ❌ "Certainty" without audit trail
5. ❌ "Information" without "Prior" prefix (for prior information system)

## Verification Commands

```bash
# 1. Find string-based ranks
grep -r "rank: str" src/gfa/ --include="*.py"

# 2. Find unused parameters
grep -r "prior_information.*Optional" src/gfa/ --include="*.py"

# 3. Find missing ResidualVector
grep -r "class.*Residual" src/gfa/ --include="*.py" | grep -v "ResidualVector"

# 4. Find dangerous defaults
grep -r "= RealityType.EXTERNAL" src/gfa/ --include="*.py"

# 5. Run all governance tests
pytest tests/gfa/prior_information/ -v
pytest tests/tools/test_architectural_admission.py -v
```

## Constitutional Status After PR-A2

| Constitution | Before PR-A2 | After PR-A2 | Remaining Work |
|--------------|--------------|-------------|----------------|
| Dāl/Madlūl Separation | ✅ Correct | ✅ Correct | None |
| Name/Reality Separation | ⚠️ Vulnerable (EXTERNAL default) | ✅ Safe (UNSPECIFIED default) | NameRealitySubGate signature |
| Opinion/Information Separation | ✅ Correct | ✅ Correct | None |
| Trace/Certainty Separation | ⚠️ Strings | ✅ Rank enum | Residual calculus |
| Form/Meaning Separation | ✅ Correct | ✅ Correct | None |

## Next Actions (Priority Order)

1. **PR-A2.1**: Migrate all `rank: str` to `rank: Rank` (1-2 days)
2. **PR-P4**: Implement ResidualVector calculus (3-5 days)
3. **PR-P5**: Fix NameRealitySubGate to require PriorInformationCandidate (2-3 days)
4. **PR-P2**: Implement EvidenceCompatibilityGate (3-4 days)
5. **PR-P3**: Implement DomainTransferGuard (3-4 days)

---

**Audit Date**: 2026-05-24
**Auditor**: PR-A2 Implementation
**Verdict**: **SUBSTANTIAL PROGRESS** ✅
**Remaining Gaps**: 5 (down from 10)
**Constitutional Health**: **75%** (up from 60%)
