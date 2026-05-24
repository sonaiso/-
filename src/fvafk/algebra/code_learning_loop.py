"""Governed Code Learning Loop - حلقة التعلم المحكومة للكود

Extends CodeLearningTrace from passive evaluation to active learning cycle:

    ProblemTrace
    → PatchProposal (with architectural admission)
    → CodeChange
    → TestEvidence
    → Result (with rank policy)
    → Decision (merge/revise/rollback/blocked)
    → KnowledgeStore update

Critical Laws:
1. No Patch without ProblemTrace
2. No CERTIFIED without evidence
3. No CERTIFIED with residuals
4. Fatal failure → REFUTED
5. Architectural change without admission → max LICENSED, never CERTIFIED
6. Passing tests ≠ architectural correctness (tests are technical evidence only)
7. Every decision must carry trace/replay
8. KnowledgeStore accumulates evidence/residuals

This is Phase-6 governed learning: the system learns from failures, proposes
patches, validates them architecturally, then decides merge/revise/rollback.

NOT in scope:
- Auto-generation of patches (Phase 7+)
- Auto-merge without review (forbidden)
- Self-modifying runtime (forbidden)
- Statistical/neural learners (Phase 7+)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping, Sequence

from .code_learning import CodeChange, CodeLearningTrace
from .core import Evidence, Failure, Rank, Residual, Result, Trace
from .learning import KnowledgeStore
from .policies import apply_policy, default_policy


@dataclass(frozen=True)
class ProblemTrace:
    """Trace of a problem requiring code intervention.

    A problem is NOT a "desire to change code" but an observed failure,
    residual, or gap that prevents rank promotion or causes regression.

    Attributes:
        problem_id: Unique identifier for this problem.
        description: Human-readable problem description.
        source: Where the problem was detected (CI, tests, dashboard, manual).
        affected_paths: Files/modules affected by this problem.
        residuals: Residuals preventing rank promotion.
        failures: Active failures/regressions.
        trace: Provenance of problem detection.
    """

    problem_id: str
    description: str
    source: str  # CI, tests, dashboard, manual_review, etc.
    affected_paths: Sequence[str] = field(default_factory=tuple)
    residuals: Sequence[Residual] = field(default_factory=tuple)
    failures: Sequence[Failure] = field(default_factory=tuple)
    trace: Trace | None = None

    def __post_init__(self) -> None:
        if not self.problem_id:
            raise ValueError("ProblemTrace.problem_id must be non-empty")
        if not self.source:
            raise ValueError("ProblemTrace.source must be non-empty")


@dataclass(frozen=True)
class PatchProposal:
    """Proposed patch to address a ProblemTrace.

    Separates proposal from execution. A proposal must justify its necessity,
    demonstrate minimal sufficiency, and obtain architectural admission if
    it introduces new constructs.

    Attributes:
        proposal_id: Unique identifier for this proposal.
        problem: The problem this patch addresses.
        changes: Sequence of code changes proposed.
        rationale: Why this patch is necessary.
        minimal_sufficiency: Evidence this is the smallest sufficient fix.
        architectural_admission: Admission check result if architectural change.
        expected_evidence: What evidence (tests/types/proofs) is expected.
        risk: Risk assessment (low/medium/high).
    """

    proposal_id: str
    problem: ProblemTrace
    changes: Sequence[CodeChange] = field(default_factory=tuple)
    rationale: str = ""
    minimal_sufficiency: str = ""
    architectural_admission: str | None = None  # Required for architectural changes
    expected_evidence: Sequence[str] = field(default_factory=tuple)
    risk: str = "medium"  # low | medium | high

    def __post_init__(self) -> None:
        if not self.proposal_id:
            raise ValueError("PatchProposal.proposal_id must be non-empty")
        if not self.changes:
            raise ValueError("PatchProposal.changes must be non-empty")

    def is_architectural_change(self) -> bool:
        """Check if this proposal introduces architectural constructs.

        Architectural changes include:
        - New layer
        - New gate
        - New domain
        - New rank policy
        - New residual taxonomy
        - CI workflow changes
        """
        # Detect architectural changes by path patterns
        arch_patterns = [
            "core.py",
            "/gate",
            "/bridge",
            "/policy",
            "/policies",
            "/constitution",
            "algebra/core",
            "algebra/policies",
            ".github/workflows",
            "/residual",
            "/rank",
        ]
        return any(
            any(pat in change.path.lower() for pat in arch_patterns)
            for change in self.changes
        )


@dataclass(frozen=True)
class CodeLearningDecision:
    """Decision output from governed learning loop.

    After evaluating a patch (applying it, testing it, ranking it), the loop
    decides whether to:
    - merge_allowed: Patch can be merged (LICENSED or CERTIFIED)
    - revise: Patch needs revision due to residuals
    - rollback: Patch causes regression (REFUTED)
    - blocked: Patch violates architectural admission

    Attributes:
        result: The Result from evaluating the patch.
        decision: Action to take.
        reason: Human-readable explanation of decision.
        next_residuals: Residuals to address in next iteration.
    """

    result: Result[CodeLearningTrace]
    decision: Literal["merge_allowed", "revise", "rollback", "blocked"]
    reason: str
    next_residuals: Sequence[Residual] = field(default_factory=tuple)

    def replay(self) -> Mapping[str, object]:
        """Return JSON-friendly replay of this decision."""
        return {
            "result": {
                "rank": self.result.rank.name,
                "trace": self.result.trace.operation if self.result.trace else None,
            },
            "decision": self.decision,
            "reason": self.reason,
            "next_residuals": [
                {"kind": r.kind, "description": r.description}
                for r in self.next_residuals
            ],
        }


class GovernedCodeLearningLoop:
    """Governed code learning loop - الحلقة المحكومة لتعلم الكود

    This is NOT an autonomous agent. It is a governed process that:
    1. Takes a PatchProposal (problem + proposed changes)
    2. Validates architectural admission if needed
    3. Simulates/applies the patch
    4. Collects test evidence
    5. Produces CodeLearningTrace
    6. Applies rank policy
    7. Updates KnowledgeStore
    8. Decides: merge/revise/rollback/blocked

    Critical Laws Enforced:
    - No CERTIFIED with residuals
    - No CERTIFIED for architectural change without admission
    - Passing tests alone ≠ CERTIFIED (needs admission too)
    - Fatal failure → REFUTED → rollback
    - Every decision preserved in trace

    This loop does NOT:
    - Generate patches automatically (takes proposals)
    - Merge automatically (returns decision for review)
    - Modify itself at runtime (forbidden)
    """

    def __init__(self, knowledge_store: KnowledgeStore | None = None):
        """Initialize the learning loop.

        Args:
            knowledge_store: Optional knowledge store. If None, creates new one.
        """
        self._knowledge_store = knowledge_store or KnowledgeStore()
        self._proposal_count = 0

    def evaluate_proposal(
        self,
        proposal: PatchProposal,
        test_evidence: Sequence[Evidence] | None = None,
        test_failures: Sequence[Failure] | None = None,
        residuals: Sequence[Residual] | None = None,
    ) -> CodeLearningDecision:
        """Evaluate a patch proposal and decide action.

        This is the core learning cycle:
        1. Validate architectural admission (if architectural change)
        2. Create CodeLearningTrace with evidence/failures/residuals
        3. Apply rank policy
        4. Update knowledge store
        5. Decide action based on rank

        Args:
            proposal: The patch proposal to evaluate.
            test_evidence: Evidence from tests/type-checks/proofs.
            test_failures: Failures from tests.
            residuals: Residuals (untested branches, missing docs, etc.).

        Returns:
            CodeLearningDecision with result and recommended action.

        Critical Laws:
        - Architectural change without admission → BLOCKED
        - Fatal failure → REFUTED → rollback
        - Residuals present → LICENSED max → revise
        - No evidence → CANDIDATE → revise
        - Evidence + no residuals + admission → CERTIFIED → merge_allowed
        """
        ev = tuple(test_evidence or ())
        fl = tuple(test_failures or ())
        res = tuple(residuals or ())

        # Law 1: Check architectural admission
        if proposal.is_architectural_change():
            if not proposal.architectural_admission:
                # No admission for architectural change → BLOCKED
                return CodeLearningDecision(
                    result=self._create_blocked_result(proposal),
                    decision="blocked",
                    reason="Architectural change without admission (violates constitution)",
                    next_residuals=res,
                )
            elif "FAILED" in proposal.architectural_admission or "REJECTED" in proposal.architectural_admission:
                # Failed admission check
                return CodeLearningDecision(
                    result=self._create_blocked_result(proposal),
                    decision="blocked",
                    reason=f"Architectural admission failed: {proposal.architectural_admission}",
                    next_residuals=res,
                )

        # Law 2: Create CodeLearningTrace for first change
        # (In real implementation, would handle multiple changes)
        change = proposal.changes[0] if proposal.changes else CodeChange(
            path="<no-change>", before="", after=""
        )

        trace = CodeLearningTrace(
            change=change,
            evidence=ev,
            residuals=res,
            failures=fl,
        )

        # Law 3: Apply rank policy
        result = trace.to_result()

        # Law 4: Special handling for architectural changes
        # Even with passing tests, architectural changes cannot be CERTIFIED
        # without architectural admission passing
        if proposal.is_architectural_change() and result.rank == Rank.CERTIFIED:
            # Architectural change + tests passing + no residuals + admission present
            # Check if admission actually PASSED
            if "PASSED" not in (proposal.architectural_admission or ""):
                # Admission exists but didn't pass → cap at LICENSED
                result = result.with_rank(Rank.LICENSED)
                res = tuple(res) + (
                    Residual(
                        kind="architectural.admission_incomplete",
                        description="Architectural admission present but not fully passed",
                    ),
                )

        # Law 5: Update knowledge store
        self._knowledge_store.ingest(result)
        self._proposal_count += 1

        # Law 6: Decide action based on rank
        decision, reason = self._decide_action(result, proposal)

        return CodeLearningDecision(
            result=result,
            decision=decision,
            reason=reason,
            next_residuals=res,
        )

    def _create_blocked_result(self, proposal: PatchProposal) -> Result[CodeLearningTrace]:
        """Create a BLOCKED result for rejected proposals."""
        change = proposal.changes[0] if proposal.changes else CodeChange(
            path="<no-change>", before="", after=""
        )

        trace = CodeLearningTrace(
            change=change,
            evidence=(),
            residuals=(
                Residual(
                    kind="architectural.admission_missing",
                    description="Architectural change requires admission",
                ),
            ),
            failures=(),
        )

        # Force rank to CANDIDATE (blocked from promotion)
        result = trace.to_result()
        return result.with_rank(Rank.CANDIDATE)

    def _decide_action(
        self,
        result: Result[CodeLearningTrace],
        proposal: PatchProposal,
    ) -> tuple[Literal["merge_allowed", "revise", "rollback", "blocked"], str]:
        """Decide action based on result rank.

        Decision rules:
        - REFUTED → rollback (regression detected)
        - CANDIDATE/UNRESOLVED → revise (insufficient evidence)
        - LICENSED → revise if high risk, else merge_allowed
        - CERTIFIED → merge_allowed
        """
        if result.rank == Rank.REFUTED:
            return ("rollback", "Fatal failure detected - regression must be rolled back")

        if result.rank in (Rank.CANDIDATE, Rank.UNRESOLVED):
            return ("revise", "Insufficient evidence - patch needs tests/documentation")

        if result.rank == Rank.LICENSED:
            if result.residuals:
                residual_kinds = ", ".join(r.kind for r in result.residuals)
                return ("revise", f"Residuals present: {residual_kinds}")
            # LICENSED with no residuals → likely architectural admission incomplete
            return ("merge_allowed", "Licensed but residuals remain - review before merge")

        if result.rank == Rank.CERTIFIED:
            return ("merge_allowed", "Certified - all evidence present, no residuals")

        return ("blocked", f"Unknown rank: {result.rank}")

    def replay_decision(self, decision: CodeLearningDecision) -> Mapping[str, object]:
        """Return full replay of decision including problem/proposal/result."""
        return decision.replay()


__all__ = [
    "ProblemTrace",
    "PatchProposal",
    "CodeLearningDecision",
    "GovernedCodeLearningLoop",
]
