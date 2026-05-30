# LughaRank vs Foundation Rank: Constitutional Distinction

## Critical Issue: Two Separate Rank Systems

The codebase has **two distinct rank systems** that must not be conflated:

### 1. `LughaRank` (src/dal_core/ranks.py)
**Purpose**: Linguistic attestation ranks - tracks how Arabic linguistic facts are known

```python
class LughaRank(Enum):
    ZERO = 0      # غير ثابت - Not attested at all
    FORM = 1      # صورة فقط - Valid form/pattern only
    QIYAS = 2     # قياس مرخص - Permitted by analogy
    SAMA = 3      # سماع خاص - Specific hearing/citation
    AHAD = 4      # آحاد لغوي - Singular linguistic transmission
    TAWATUR = 5   # تواتر - Mass transmission
```

**Domain**: Arabic grammatical knowledge (نحو، صرف، لغة)
**Evidence**: Linguistic authority (قياس، سماع، تواتر)
**Used by**: `CaseEffectCandidate`, `FactorMarkEquation`, `PreSyntaxVector`

### 2. `Rank` (src/dal_core/foundation/rank.py)
**Purpose**: Epistemic ranks - tracks computational confidence across all carrier layers

```python
class Rank(Enum):
    ZERO = auto()                # No classification
    CANDIDATE = auto()           # Potential classification
    HYPOTHESIS = auto()          # Weak evidence
    STRONG_HYPOTHESIS = auto()   # Strong evidence
    CERTIFICATE = auto()         # Certified by policy
    BLOCKED = auto()             # Terminal failure
```

**Domain**: Computational carrier layers (U₀-U₁₅)
**Evidence**: Computational evidence, blocking conditions
**Used by**: Foundation layer, RankVector

---

## The Constitutional Violation: Rank Inflation

### What Happened (PR #161)
Test fixtures used `LughaRank.QIYAS` as a substitute for non-existent `LughaRank.CANDIDATE`:

```python
# ❌ WRONG - Rank inflation
CaseSignPotential(
    rank=LughaRank.QIYAS,  # This is قياس مرخص!
    ...
)
```

### Why This Is Wrong

`LughaRank.QIYAS` means **"قياس مرخص"** (permitted by analogy):
- Requires analogical reasoning evidence
- Implies linguistic authority for the structure
- Is NOT equivalent to computational "candidate"

Using `QIYAS` for mere structural candidates without qiyas evidence:
- Promotes candidate to qiyas without justification
- Conflates computational potential with linguistic authority
- Violates constitutional separation between layers

### The Correct Fix

Use `LughaRank.FORM` for structural candidates without qiyas evidence:

```python
# ✅ CORRECT - Structural candidate
CaseSignPotential(
    rank=LughaRank.FORM,  # صورة فقط - valid form only
    ...
)
```

---

## When to Use Each LughaRank

### `LughaRank.ZERO`
**Meaning**: غير ثابت - Not attested at all
**Use**: Invalid or rejected structures
**Evidence**: None / Blocker present

### `LughaRank.FORM`
**Meaning**: صورة فقط - Valid form/pattern only
**Use**:
- Structural candidates without linguistic authority
- Computationally valid patterns
- Test fixtures for candidate structures
**Evidence**: Form validity only, no qiyas/sama

### `LughaRank.QIYAS`
**Meaning**: قياس مرخص - Permitted by analogy
**Use**:
- Structures permitted by qiyas reasoning
- Analogical extension from attested patterns
- **Requires qiyas evidence**
**Evidence**: Qiyas procedure executed, source pattern identified

### `LughaRank.SAMA`
**Meaning**: سماع خاص - Specific hearing/citation
**Use**: Directly attested in corpus
**Evidence**: Specific textual citation

### `LughaRank.AHAD`
**Meaning**: آحاد لغوي - Singular linguistic transmission
**Use**: Transmitted by single chain
**Evidence**: Transmission chain

### `LughaRank.TAWATUR`
**Meaning**: تواتر - Mass transmission
**Use**: Massively attested patterns
**Evidence**: Multiple independent transmissions

---

## Mapping: Foundation.Rank ≠ LughaRank

**NO direct equivalence exists**. They measure different dimensions:

| Foundation.Rank | LughaRank | Relationship |
|-----------------|-----------|--------------|
| `CANDIDATE` | `FORM` | Similar level: potential/structural |
| `HYPOTHESIS` | `QIYAS`? | NO - different evidence types |
| `CERTIFICATE` | `TAWATUR`? | NO - different domains |

**Forbidden**:
```python
# ❌ NEVER do this
if foundation_rank == Rank.CANDIDATE:
    lugha_rank = LughaRank.QIYAS  # WRONG!
```

**Correct thinking**:
- Foundation.Rank → computational confidence
- LughaRank → linguistic authority
- They can coexist independently in different fields

---

## Constitutional Laws

### Law 1: No Rank Conflation
```
LughaRank ≠ Foundation.Rank
```
Never convert between them automatically.

### Law 2: No Rank Inflation
```
Candidate structure → LughaRank.FORM
NOT → LughaRank.QIYAS (without qiyas evidence)
```

### Law 3: Evidence Required for Promotion
```
FORM → QIYAS requires: qiyas procedure + source pattern
QIYAS → SAMA requires: textual citation
SAMA → TAWATUR requires: multiple attestations
```

### Law 4: Test Fixture Default
```
Test fixtures without linguistic authority → LughaRank.FORM
NOT → LughaRank.QIYAS
```

---

## Audit Checklist

When using `LughaRank` in code:

- [ ] Is this structure just computationally valid? → `FORM`
- [ ] Was qiyas procedure executed? → `QIYAS` (with evidence)
- [ ] Is this from corpus citation? → `SAMA`/`AHAD`/`TAWATUR`
- [ ] Am I in a test fixture without linguistic evidence? → `FORM`
- [ ] Did I write `QIYAS` because `CANDIDATE` doesn't exist? → **FIX TO `FORM`**

---

## References

- `src/dal_core/ranks.py` - LughaRank definition
- `src/dal_core/foundation/rank.py` - Foundation.Rank definition
- PR #161 - Where rank inflation occurred
- This document - Constitutional correction

**Created**: 2026-05-30
**Purpose**: Prevent rank inflation before AmilMamulEquation layer
