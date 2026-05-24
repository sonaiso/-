# PR-CL1: Governed Code Learning Loop MVP

**الحلقة المحكومة لتعلم الكود — Minimal Viable Product**

## Executive Summary

This PR extends the existing algebraic code learning foundation (`CodeChange`, `CodeLearningTrace`, `KnowledgeStore`) into a **governed learning loop** that transforms passive evaluation into active, constitutionally-constrained learning.

**What changed:**
- **Before**: `CodeLearningTrace` evaluated a code change in isolation
- **After**: Complete learning cycle: Problem → Proposal → Evaluation → Decision → Knowledge accumulation

**What did NOT change:**
- No AI code generation
- No auto-merge bot
- No self-modifying runtime
- No neural learners
- Still Phase-0: minimal, deterministic, append-only

---

## 1. What Became "Learning" (vs Pure Evaluation)?

### Previous State: Passive Evaluation

```python
# Old pattern: Isolated evaluation
trace = CodeLearningTrace(
    change=CodeChange(...),
    evidence=[...],
    residuals=[...],
    failures=[...]
)
result = trace.to_result()  # Get rank, done
```

This was **evaluation without memory** — each change assessed independently, no accumulation, no decision logic.

### Current State: Governed Learning Loop

```python
# New pattern: Problem-driven learning cycle
problem = ProblemTrace(
    problem_id="test_failure_123",
    description="Golden dataset test failing: UNSPECIFIED existence type",
    source="CI",
    failures=[Failure(kind="test", severity="BLOCKER", ...)]
)

proposal = PatchProposal(
    proposal_id="fix_unspecified_handling",
    problem=problem,
    changes=[CodeChange(path="name_reality_subgate.py", ...)],
    rationale="Add explicit UNSPECIFIED check per constitutional safety default",
    minimal_sufficiency="Adds single guard clause, no new abstraction",
    architectural_admission="MinimalSufficiency: Single guard, proven necessary by test failure"
)

loop = GovernedCodeLearningLoop()
decision = loop.evaluate_proposal(
    proposal,
    test_evidence=[Evidence(kind="test_pass", ...)],
    residuals=[]
)

# Decision output:
# - result.rank = CERTIFIED (tests pass, no residuals)
# - decision.decision = "merge_allowed"
# - KnowledgeStore updated with evidence
# - Full replay trace preserved
```

**What makes this "learning":**

1. **Memory Accumulation** — `KnowledgeStore` accumulates evidence kinds and residual patterns across proposals
2. **Problem Traceability** — Every patch must cite a `ProblemTrace`; no solutions without problems
3. **Constitutional Constraint** — Architectural changes require explicit admission; violations → BLOCKED
4. **Decision Logic** — System decides: merge_allowed / revise / rollback / blocked
5. **Replay Capability** — Full provenance chain: problem → proposal → evaluation → decision

This is **learning as constitutional memory**, not learning as statistical inference.

---

## 2. What Remains Out of Scope (Explicitly NOT Built)

### NOT Built in PR-CL1:

1. **AI Code Agent** — No automatic patch generation from problem descriptions
   - We take `PatchProposal` as input, not problem text
   - Human/external agent must propose changes

2. **Auto-Merge Bot** — No automatic merging based on rank
   - `decision="merge_allowed"` is **advisory only**
   - Human reviewer must execute merge
   - System provides decision + rationale, not action

3. **Self-Modifying Runtime** — No runtime code generation or hot-patching
   - All changes are proposals for review
   - No eval(), exec(), or dynamic class modification
   - System observes changes, doesn't execute them

4. **Neural/Statistical Learners** — No ML models, no embeddings, no gradient descent
   - `KnowledgeStore` is append-only tuples
   - "Learning" = accumulation, not optimization
   - Phase-0 intentionally stays deterministic

5. **Persistent Storage** — No database, no file writes
   - `KnowledgeStore` is in-memory only
   - Replay via `decision.replay()` returns dict
   - Caller responsible for persistence (if desired)

6. **Multi-Agent Coordination** — No distributed learning, no consensus
   - Single `GovernedCodeLearningLoop` instance
   - No agent communication protocol
   - No conflict resolution between proposals

### Why These Are Out of Scope

**Constitutional principle**: "الجبر العام لا يتوسع بالتراكم، بل يتدرج بالحد الأدنى الكافي"

We build the **minimal loop** that exercises the constitution. Heavy learners come later (Phase 3+), after the algebra has been wired through all layers.

---

## 3. Guarantee Against Arbitrary Self-Modification

### Three-Layer Defense

#### Layer 1: Immutability (Type-Level Enforcement)

```python
@dataclass(frozen=True)
class ProblemTrace:
    """Cannot be modified after creation."""
    problem_id: str
    # ... all fields immutable

@dataclass(frozen=True)
class PatchProposal:
    """Cannot be modified after creation."""
    # ... all fields immutable

@dataclass(frozen=True)
class CodeLearningDecision:
    """Cannot be modified after creation."""
    # ... all fields immutable
```

**Guarantee**: No object can mutate its own state. Dataclasses are `frozen=True`.

#### Layer 2: No-Execute Contract (Operational Enforcement)

```python
class GovernedCodeLearningLoop:
    def evaluate_proposal(self, proposal: PatchProposal, ...) -> CodeLearningDecision:
        # WE NEVER:
        # - Execute proposal.changes (no write to filesystem)
        # - Import modified code (no dynamic import)
        # - Eval proposal code (no eval/exec)
        # - Modify self._knowledge_store entries (append-only)

        # WE ONLY:
        # - Read proposal fields
        # - Create CodeLearningTrace
        # - Apply rank policy
        # - Append to KnowledgeStore
        # - Return decision (advisory)
```

**Guarantee**: The loop is **observational only** — it reads proposals, applies rank policy, accumulates knowledge, returns decisions. It does NOT execute changes.

#### Layer 3: Constitutional Gates (Algebraic Enforcement)

**8 Critical Laws** enforced in `evaluate_proposal`:

1. **No Evidence → CANDIDATE** — Without passing tests, patch stays candidate → decision="revise"
2. **No CERTIFIED with Residuals** — Untested branches prevent certification → decision="revise"
3. **No CERTIFIED without Evidence** — Must have passing tests → decision="revise"
4. **Fatal Failure → REFUTED** — Broken tests → decision="rollback"
5. **Architectural Change without Admission → max LICENSED** → decision="blocked" if no admission
6. **Passing Tests ≠ Architectural Correctness** — Tests alone cannot promote architectural changes
7. **Every Decision Carries Trace** — Full replay chain preserved
8. **KnowledgeStore Accumulates** — Evidence and residuals accumulated across proposals

**Guarantee**: Even if we wanted to auto-merge, the gates prevent it:
- Architectural change without admission → BLOCKED
- Any residual → max LICENSED (not CERTIFIED) → decision != "merge_allowed"
- Fatal failure → REFUTED → decision="rollback"

### Runtime Enforcement Example

```python
# Attempt to bypass constitution
proposal = PatchProposal(
    proposal_id="evil_bypass",
    problem=problem,
    changes=[CodeChange(path="core.py", ...)],  # Architectural change
    architectural_admission=None,  # No admission!
)

decision = loop.evaluate_proposal(proposal, test_evidence=[...])

# Result:
# decision.decision == "blocked"
# decision.reason == "Architectural change requires admission (minimal sufficiency check)"
# decision.result.rank == BLOCKED (custom gate enforcement)
```

**The system cannot bypass its own gates** because:
1. `evaluate_proposal` enforces gates before decision
2. Decision is advisory (caller must execute)
3. Gates are pure functions (deterministic, no side effects)
4. No runtime code generation

---

## 4. Architecture

### Data Flow

```
┌─────────────┐
│ ProblemTrace│ ← Observation (CI, tests, dashboard, manual review)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│PatchProposal│ ← Human/external agent proposes solution
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│GovernedCodeLearningLoop  │
│ evaluate_proposal()      │
│  1. Validate admission   │ ← Constitutional gates enforce laws
│  2. Create trace         │
│  3. Apply rank policy    │
│  4. Decide outcome       │
│  5. Update knowledge     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────┐
│CodeLearningDecision│ ← Advisory output (merge_allowed/revise/rollback/blocked)
│ + KnowledgeStore  │ ← Accumulated evidence/residuals
└───────────────────┘
```

### Components

#### 1. ProblemTrace
**Purpose**: Immutable record of a problem requiring intervention

**Fields**:
- `problem_id`: Unique identifier
- `description`: Human-readable problem statement
- `source`: Origin (CI, tests, dashboard, manual_review)
- `affected_paths`: Files touched by problem
- `residuals`: Missing facts blocking resolution
- `failures`: Actively failing facts
- `trace`: Optional provenance

**Validation**:
- `problem_id` must be non-empty
- At least one of `residuals` or `failures` must be present (no problem without evidence)

#### 2. PatchProposal
**Purpose**: Proposed solution to a ProblemTrace

**Fields**:
- `proposal_id`: Unique identifier
- `problem`: The ProblemTrace being addressed
- `changes`: Sequence of CodeChange (before/after pairs)
- `rationale`: Why this solution?
- `minimal_sufficiency`: Why minimal?
- `architectural_admission`: If architectural change, justification
- `expected_evidence`: What tests/proofs should pass?
- `risk`: low/medium/high

**Architectural Detection**:
```python
def is_architectural_change(self) -> bool:
    """Detect if changes modify core/gates/bridges."""
    arch_patterns = ["core", "gate", "bridge", "policy", "constitution"]
    return any(
        any(pat in change.path.lower() for pat in arch_patterns)
        for change in self.changes
    )
```

**Validation**:
- `proposal_id` and `rationale` must be non-empty
- Architectural changes require `architectural_admission`

#### 3. CodeLearningDecision
**Purpose**: Immutable decision output with full provenance

**Fields**:
- `result`: Full algebraic Result[CodeLearningTrace]
- `decision`: Literal["merge_allowed", "revise", "rollback", "blocked"]
- `reason`: Human-readable explanation
- `next_residuals`: Residuals to address in next iteration

**Replay**:
```python
def replay(self) -> Mapping[str, object]:
    return {
        "decision": self.decision,
        "reason": self.reason,
        "rank": self.result.rank.name,
        "evidence_count": len(self.result.evidence),
        "residual_count": len(self.result.residuals),
        "failure_count": len(self.result.failures),
        "next_residuals": [r.__dict__ for r in self.next_residuals],
    }
```

#### 4. GovernedCodeLearningLoop
**Purpose**: Stateful learning loop with constitutional enforcement

**State**:
- `_knowledge_store`: Append-only accumulator
- `_proposal_count`: Counter for processed proposals

**Core Method**:
```python
def evaluate_proposal(
    self,
    proposal: PatchProposal,
    test_evidence: Sequence[Evidence] | None = None,
    test_failures: Sequence[Failure] | None = None,
    residuals: Sequence[Residual] | None = None,
) -> CodeLearningDecision:
    """
    Evaluate proposal under constitutional gates.

    Returns:
        CodeLearningDecision with rank, decision, reason, trace
    """
```

**Decision Logic**:
- **merge_allowed**: Rank.CERTIFIED + no architectural or low-risk architectural with admission
- **revise**: Rank.LICENSED or CANDIDATE (has residuals or insufficient evidence)
- **rollback**: Rank.REFUTED (fatal failures)
- **blocked**: Architectural change without admission

---

## 5. Critical Laws Enforcement

### Law 1: No Evidence → CANDIDATE
```python
# No test_evidence provided
if not evidence:
    base_rank = Rank.UNRESOLVED
# After policy: Rank.CANDIDATE
# Decision: "revise" (need evidence)
```

### Law 2: No CERTIFIED without Evidence
```python
# Empty evidence
if not evidence:
    # Cannot reach CERTIFIED
    # max(CANDIDATE, LICENSED)
```

### Law 3: No CERTIFIED with Residuals
```python
if residuals and rank == Rank.CERTIFIED:
    # Policy demotes to LICENSED
    final_rank = Rank.LICENSED
# Decision: "revise" (address residuals)
```

### Law 4: Fatal Failure → REFUTED
```python
if any(f.is_fatal() for f in failures):
    rank = Rank.REFUTED
# Decision: "rollback" (broken tests)
```

### Law 5: Architectural Change without Admission → BLOCKED
```python
if proposal.is_architectural_change() and not proposal.architectural_admission:
    # Special gate: set rank to BLOCKED
    decision = "blocked"
    reason = "Architectural change requires admission (minimal sufficiency check)"
```

### Law 6: Passing Tests ≠ Architectural Correctness
```python
if proposal.is_architectural_change():
    # Tests alone cannot certify
    # Must have architectural_admission
    if final_rank == Rank.CERTIFIED and proposal.risk != "low":
        decision = "revise"  # Need architectural review
```

### Law 7: Every Decision Carries Trace
```python
result = Result(
    value=trace,
    rank=final_rank,
    evidence=evidence,
    residuals=residuals,
    failures=failures,
    trace=Trace(operation=f"code_learning:{proposal.proposal_id}"),
)
# Trace preserved in result
# Replay via decision.replay()
```

### Law 8: KnowledgeStore Accumulates
```python
self._knowledge_store.ingest(result)
# Evidence kinds accumulated
# Residual counts tracked
# results_ingested incremented
```

---

## 6. Usage Examples

### Example 1: Simple Bug Fix (Merge Allowed)

```python
from fvafk.algebra import (
    GovernedCodeLearningLoop,
    ProblemTrace,
    PatchProposal,
    CodeChange,
    Evidence,
)

# 1. Observe problem
problem = ProblemTrace(
    problem_id="bug_123",
    description="Null pointer in user authentication",
    source="CI",
    failures=[Failure(kind="test", severity="BLOCKER", message="NPE in auth.py:42")],
)

# 2. Propose solution
proposal = PatchProposal(
    proposal_id="fix_bug_123",
    problem=problem,
    changes=[CodeChange(
        path="src/auth.py",
        before="user.name",
        after="user.name if user else 'anonymous'"
    )],
    rationale="Add null check before access",
    minimal_sufficiency="Single guard clause, no abstraction",
    risk="low",
)

# 3. Evaluate
loop = GovernedCodeLearningLoop()
decision = loop.evaluate_proposal(
    proposal,
    test_evidence=[
        Evidence(kind="test_pass", source="test_auth.py", detail="test_null_user", weight=1.0)
    ],
    residuals=[],  # All branches tested
)

# 4. Check decision
assert decision.decision == "merge_allowed"
assert decision.result.rank == Rank.CERTIFIED
print(decision.reason)  # "Patch certified: evidence present, no residuals, low risk"
```

### Example 2: Architectural Change (Blocked without Admission)

```python
# Architectural change without admission
proposal = PatchProposal(
    proposal_id="refactor_core",
    problem=problem,
    changes=[CodeChange(path="src/fvafk/algebra/core.py", ...)],
    rationale="Refactor Rank enum",
    minimal_sufficiency="???",  # Insufficient
    architectural_admission=None,  # Missing!
    risk="high",
)

decision = loop.evaluate_proposal(proposal, test_evidence=[...])

assert decision.decision == "blocked"
assert "requires admission" in decision.reason
```

### Example 3: Passing Tests with Residuals (Revise)

```python
decision = loop.evaluate_proposal(
    proposal,
    test_evidence=[Evidence(kind="test_pass", ...)],
    residuals=[Residual(kind="untested_branch", severity="MAJOR", ...)],
)

assert decision.decision == "revise"
assert decision.result.rank == Rank.LICENSED  # Not CERTIFIED due to residuals
assert len(decision.next_residuals) == 1
```

### Example 4: Fatal Failure (Rollback)

```python
decision = loop.evaluate_proposal(
    proposal,
    test_failures=[Failure(kind="test", severity="BLOCKER", message="Regression", fatal=True)],
)

assert decision.decision == "rollback"
assert decision.result.rank == Rank.REFUTED
```

---

## 7. Testing Strategy

Test suite (`tests/test_algebra_code_learning_loop.py`) covers:

1. **All 8 critical laws** — Individual tests per law
2. **Edge cases**:
   - Empty proposal (no changes)
   - Problem without residuals/failures (invalid)
   - Multiple architectural changes
3. **Integration test** — Full cycle: problem → proposal → decision → knowledge accumulation
4. **Replay verification** — All decisions preserve full trace

**Test organization**:
```python
class TestGovernedCodeLearningLoop:
    # Law 1: No evidence → CANDIDATE
    def test_law_1_no_evidence_candidate(self): ...

    # Law 2: No CERTIFIED without evidence
    def test_law_2_evidence_required_for_certified(self): ...

    # ... (20+ tests)

    # Integration
    def test_full_learning_cycle(self): ...
```

---

## 8. Comparison: Before vs After

| Aspect | Before (CodeLearningTrace) | After (GovernedCodeLearningLoop) |
|--------|---------------------------|----------------------------------|
| **Input** | CodeChange + evidence/residuals/failures | ProblemTrace + PatchProposal |
| **Output** | Result[CodeLearningTrace] | CodeLearningDecision |
| **Memory** | None (stateless) | KnowledgeStore (accumulates) |
| **Decision** | None (just rank) | merge_allowed / revise / rollback / blocked |
| **Traceability** | Single change | Problem → Proposal → Decision chain |
| **Constitutional Enforcement** | Rank policy only | 8 critical laws + gates |
| **Architectural Gate** | No | Yes (requires admission) |
| **Replay** | Change-level | Full cycle (problem → decision) |

---

## 9. Future Extensions (Out of Scope for PR-CL1)

**Phase 2+** (after algebra wired through layers):
- Adapter from CI failures → ProblemTrace
- Adapter from architectural review → admission validation
- Statistical learner over KnowledgeStore (pattern mining)

**Phase 3+** (heavy learning):
- Code embedding model for similarity
- Automated proposal generation (given ProblemTrace)
- Multi-proposal ranking
- Persistent KnowledgeStore with versioning

**Never**:
- Ungovernod auto-merge
- Runtime self-modification
- Untraced decisions

---

## 10. Verification Checklist

- [x] All 8 critical laws enforced in code
- [x] Comprehensive test suite (20+ tests)
- [x] Immutability via `frozen=True` dataclasses
- [x] No-execute contract (observational only)
- [x] Replay capability for all decisions
- [x] KnowledgeStore accumulation
- [x] Architectural admission gate
- [x] Integration with existing algebra (Rank, Evidence, Residual, Failure)
- [x] Documentation (this file)
- [x] Exported in `fvafk.algebra.__init__.py`

---

## 11. Summary

**PR-CL1 adds**:
1. **ProblemTrace** — Immutable problem record
2. **PatchProposal** — Proposed solution with admission
3. **CodeLearningDecision** — Decision output with trace
4. **GovernedCodeLearningLoop** — Stateful learning cycle with constitutional enforcement

**PR-CL1 does NOT add**:
- AI code generation
- Auto-merge bot
- Self-modifying runtime
- Neural learners
- Persistent storage

**What makes this "learning"**:
- Memory accumulation (KnowledgeStore)
- Problem traceability (ProblemTrace → PatchProposal → Decision)
- Constitutional constraint (8 critical laws)
- Decision logic (merge/revise/rollback/blocked)
- Replay capability (full provenance)

**Guarantee against arbitrary self-modification**:
- Immutability (frozen dataclasses)
- No-execute contract (observational only)
- Constitutional gates (8 critical laws)

**الحلقة المحكومة لتعلم الكود** — Learning as constitutional memory, not statistical inference.

---

**Files Modified**:
- `src/fvafk/algebra/code_learning_loop.py` (new)
- `src/fvafk/algebra/__init__.py` (exports added)
- `tests/test_algebra_code_learning_loop.py` (new)
- `docs/PR_CL1_CODE_LEARNING_LOOP.md` (new)

**Depends On**: PR-A2 (Rank enum, safety defaults, constitutional enforcement)

**Next Steps**: Integration with CI (Phase 2) — auto-generate ProblemTrace from test failures
