"""Learner: Self-learning loop for general algebraic rules.

Core Principle:
    التعلم الذاتي هو البرهان أن الجبر عام.
    "Self-learning is the proof that the algebra is general."

Central Law:
    المتعلم يجب أن:
    ١. يستخرج الأصول
    ٢. يكتشف الثوابت
    ٣. يحدد المناط
    ٤. يختبر على الأمثلة
    ٥. يواجه الأمثلة المضادة
    ٦. يعدل القاعدة
    ٧. يحفظ الأثر والبقايا
    ٨. يفسر التغيير

    "The learner must:
    1. Extract origins
    2. Discover invariants
    3. Determine manaat
    4. Test on examples
    5. Face counterexamples
    6. Modify the rule
    7. Preserve trace and residuals
    8. Explain the change"

Architecture:
    The **GeneralLearner** implements the complete learning cycle:

    ```
    Origins → Invariants → Manaat → RuleCandidate
                                         ↓
                                    Verification
                                         ↓
                              Counterexamples? ──No──→ Confirmed
                                         ↓
                                        Yes
                                         ↓
                                    Refinement
                                         ↓
                                    Explanation
                                         ↓
                                   Updated Rule
                                         ↓
                                  (cycle repeats)
    ```

    A **LearningCycle** is one iteration of:
    - Extract/refine rule
    - Verify against examples
    - Handle counterexamples
    - Generate explanations
    - Update rule

Example (فاعل Pattern):
    Cycle 1:
        Origins: كاتب، زارع، عامل
        Rule: "All فاعل → agentive"
        Rank: CANDIDATE

    Cycle 2:
        Test: طاهر، حامض، بارد
        Counterexamples: All 3 (qualitative, not agentive)
        Refinement: "فاعل → agentive OR qualitative"
        Rank: LICENSED (after refinement)

    Cycle 3:
        Test: More examples
        No counterexamples
        Rank: CERTIFIED (stable)
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Tuple, Mapping, Any

from fvafk.algebra import Evidence, Residual, Rank, Trace

from .origin import Origin, OriginSet, make_origin_set
from .invariant import detect_invariants, InvariantSet
from .manaat import determine_manaat, Manaat
from .rule_candidate import RuleCandidate, RuleStatus, make_rule_candidate
from .verification import verify_rule, VerificationResult, Counterexample
from .explanation import Explanation, ExplanationKind, explain_modification, explain_rank_change


# ===========================================================================
# Learning Cycle
# ===========================================================================


@dataclass(frozen=True)
class LearningCycle:
    """One iteration of the learning loop.

    Attributes:
        cycle_number: Cycle iteration number (1, 2, 3, ...).
        rule_before: Rule state before this cycle.
        rule_after: Rule state after this cycle.
        verification: Verification results.
        explanations: Explanations for changes.
        evidence: Evidence collected this cycle.
        residuals: Residuals from this cycle.
        trace: Provenance trace.

    Example:
        >>> cycle = LearningCycle(
        ...     cycle_number=1,
        ...     rule_before=initial_rule,
        ...     rule_after=refined_rule,
        ...     verification=verification_result,
        ...     explanations=(explanation,),
        ... )
        >>> cycle.cycle_number
        1
        >>> cycle.had_counterexamples
        True
    """

    cycle_number: int
    rule_before: RuleCandidate
    rule_after: RuleCandidate
    verification: VerificationResult | None = None
    explanations: Tuple[Explanation, ...] = ()
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    trace: Trace = field(default_factory=lambda: Trace(operation="learning_cycle"))

    @property
    def had_counterexamples(self) -> bool:
        """Check if this cycle found counterexamples."""
        return self.verification is not None and self.verification.has_counterexamples

    @property
    def rule_changed(self) -> bool:
        """Check if rule changed in this cycle."""
        return self.rule_before.description != self.rule_after.description

    @property
    def rank_changed(self) -> bool:
        """Check if rank changed in this cycle."""
        return self.rule_before.rank != self.rule_after.rank

    @property
    def was_successful(self) -> bool:
        """Check if cycle was successful (no unresolved counterexamples)."""
        return not self.had_counterexamples or self.rule_changed


# ===========================================================================
# General Learner
# ===========================================================================


@dataclass
class GeneralLearner:
    """Self-learning engine for general algebraic rules.

    The learner implements the complete cycle:
    1. Extract origins
    2. Detect invariants
    3. Determine manaat
    4. Create rule candidate
    5. Verify against examples
    6. Handle counterexamples
    7. Refine rule
    8. Explain changes
    9. Repeat

    Attributes:
        current_rule: Current rule being learned/refined.
        cycles: History of learning cycles.
        origin_set: Set of origin examples.
        invariant_set: Set of detected invariants.
        manaat: Current manaat (scope/basis).
        knowledge: Accumulated knowledge.

    Example:
        >>> learner = GeneralLearner()
        >>> learner.add_origins(origin1, origin2, origin3)
        >>> rule = learner.extract_rule()
        >>> learner.verify_and_refine(test_examples)
        >>> learner.current_rule.rank
        <Rank.LICENSED: 2>
    """

    current_rule: RuleCandidate | None = None
    cycles: Tuple[LearningCycle, ...] = ()
    origin_set: OriginSet | None = None
    invariant_set: InvariantSet | None = None
    manaat: Manaat | None = None
    knowledge: Mapping[str, Any] = field(default_factory=dict)

    def add_origins(self, *origins: Origin) -> None:
        """Add origin examples to the learner.

        Args:
            origins: Origin instances to add.

        Raises:
            ValueError: If origins is empty.

        Example:
            >>> learner = GeneralLearner()
            >>> learner.add_origins(origin1, origin2, origin3)
            >>> len(learner.origin_set.origins)
            3
        """
        if not origins:
            raise ValueError("At least one origin required")

        # Create or update origin set
        if self.origin_set is None:
            self.origin_set = make_origin_set(origins=origins)
        else:
            # Merge with existing origins
            all_origins = self.origin_set.origins + origins
            self.origin_set = make_origin_set(origins=all_origins)

    def extract_rule(self) -> RuleCandidate:
        """Extract a rule from current origins.

        This is the main rule extraction process:
        1. Detect invariants from origins
        2. Determine manaat (scope/basis)
        3. Create rule candidate
        4. Set initial rank

        Returns:
            Newly extracted RuleCandidate.

        Raises:
            ValueError: If no origins have been added.

        Example:
            >>> learner = GeneralLearner()
            >>> learner.add_origins(origin1, origin2, origin3)
            >>> rule = learner.extract_rule()
            >>> rule.pattern
            'فاعل'
        """
        if self.origin_set is None or not self.origin_set.origins:
            raise ValueError("No origins available; add origins first")

        # Detect invariants
        self.invariant_set = detect_invariants(origins=self.origin_set.origins)

        # Determine manaat
        self.manaat = determine_manaat(
            invariants=self.invariant_set.invariants,
            positive_examples=self.origin_set.origins,
        )

        # Build rule description
        description = self._build_rule_description()

        # Extract pattern from invariants or origins
        pattern = self._extract_pattern()

        # Create rule candidate
        self.current_rule = make_rule_candidate(
            description=description,
            pattern=pattern,
            manaat=self.manaat,
            origins=self.origin_set.origins,
            invariants=self.invariant_set.invariants,
            evidence=self._collect_evidence(),
            residuals=self._collect_residuals(),
        )

        return self.current_rule

    def verify_and_refine(
        self,
        test_examples: Tuple[Origin, ...],
        max_cycles: int = 5,
    ) -> RuleCandidate:
        """Verify rule and refine if counterexamples found.

        This runs the learning cycle:
        1. Verify rule against test examples
        2. If counterexamples found, refine rule
        3. Explain changes
        4. Repeat until stable or max cycles reached

        Args:
            test_examples: Examples to test against.
            max_cycles: Maximum refinement cycles (default: 5).

        Returns:
            Final refined RuleCandidate.

        Example:
            >>> learner = GeneralLearner()
            >>> learner.add_origins(origin1, origin2, origin3)
            >>> learner.extract_rule()
            >>> final_rule = learner.verify_and_refine(test_examples)
            >>> final_rule.status
            <RuleStatus.STABLE: 4>
        """
        if self.current_rule is None:
            raise ValueError("No rule to verify; call extract_rule() first")

        for cycle_num in range(1, max_cycles + 1):
            # Verify current rule
            verification = verify_rule(self.current_rule, test_examples)

            # Check if refinement needed
            if not verification.needs_refinement:
                # No refinement needed; mark as stable
                # CRITICAL: No counterexamples does NOT mean CERTIFIED
                # Add residual indicating search was incomplete
                from .residual_taxonomy import make_counterexample_search_incomplete

                search_scope = f"{len(test_examples)} examples tested"
                search_residual = make_counterexample_search_incomplete(scope=search_scope)

                self.current_rule = self.current_rule.with_status(RuleStatus.STABLE)
                self.current_rule = self.current_rule.with_rank(verification.rank)
                self.current_rule = self.current_rule.with_residual(search_residual)

                # Record cycle
                cycle = LearningCycle(
                    cycle_number=cycle_num,
                    rule_before=self.current_rule,
                    rule_after=self.current_rule,
                    verification=verification,
                    explanations=(
                        explain_rank_change(
                            before_rank=self.current_rule.rank,
                            after_rank=verification.rank,
                            trigger="No counterexamples found in tested scope",
                            learned="Rule is stable within tested scope (not proven complete)",
                        ),
                    ),
                )
                self.cycles = self.cycles + (cycle,)
                break

            # Refine rule based on counterexamples
            rule_before = self.current_rule
            self.current_rule = self._refine_from_counterexamples(
                verification.counterexamples,
                verification.refinement_suggestions,
            )

            # Generate explanations
            explanations = self._generate_cycle_explanations(
                rule_before, self.current_rule, verification
            )

            # Record cycle
            cycle = LearningCycle(
                cycle_number=cycle_num,
                rule_before=rule_before,
                rule_after=self.current_rule,
                verification=verification,
                explanations=explanations,
            )
            self.cycles = self.cycles + (cycle,)

        return self.current_rule

    # -- Helpers ------------------------------------------------------------

    def _build_rule_description(self) -> str:
        """Build human-readable rule description from invariants and manaat."""
        if not self.invariant_set or not self.invariant_set.invariants:
            return "Rule description unclear"

        primary_inv = self.invariant_set.primary
        if primary_inv is None:
            return "No primary invariant found"

        pattern = primary_inv.value
        # Look for interpretation invariant
        interp = None
        for inv in self.invariant_set.invariants:
            if hasattr(inv, "kind") and str(inv.kind).endswith("INTERPRETATION_TYPE"):
                interp = inv.value
                break

        if interp:
            return f"{pattern} pattern licenses {interp} interpretation"
        else:
            return f"{pattern} pattern (interpretation unclear)"

    def _extract_pattern(self) -> str:
        """Extract pattern from invariants or origins."""
        if self.invariant_set and self.invariant_set.primary:
            return self.invariant_set.primary.value

        if self.origin_set and self.origin_set.origins:
            # Use pattern from first origin
            return self.origin_set.origins[0].pattern

        return "unknown"

    def _collect_evidence(self) -> Tuple[Evidence, ...]:
        """Collect evidence from origins, invariants, and manaat."""
        evidence_list = []

        # Evidence from origins
        if self.origin_set:
            evidence_list.append(
                Evidence(
                    kind="rule.extraction",
                    source="origin_set",
                    detail=f"Rule extracted from {len(self.origin_set.origins)} origin(s)",
                    weight=min(len(self.origin_set.origins) / 3.0, 1.0),
                )
            )

        # Evidence from invariants
        if self.invariant_set:
            evidence_list.append(
                Evidence(
                    kind="invariant.detection",
                    source="invariant_set",
                    detail=f"{len(self.invariant_set.invariants)} invariant(s) detected",
                    weight=self.invariant_set.strongest.strength if self.invariant_set.invariants else 0.5,
                )
            )

        return tuple(evidence_list)

    def _collect_residuals(self) -> Tuple[Residual, ...]:
        """Collect residuals from origins, invariants, and manaat."""
        residuals_list = []

        # Check origin sufficiency
        if self.origin_set and len(self.origin_set.origins) < 3:
            residuals_list.append(
                Residual(
                    kind="origin.insufficient",
                    description=f"Only {len(self.origin_set.origins)} origin(s); recommend ≥3",
                )
            )

        # Check invariant clarity
        if self.invariant_set and not self.invariant_set.all_stable:
            residuals_list.append(
                Residual(
                    kind="invariant.unclear",
                    description="Some invariants are unstable or low-confidence",
                )
            )

        # Check manaat clarity
        if self.manaat and self.manaat.is_ambiguous:
            residuals_list.append(
                Residual(
                    kind="manaat.ambiguous",
                    description="Rule scope/basis is unclear or low-confidence",
                )
            )

        return tuple(residuals_list)

    def _refine_from_counterexamples(
        self,
        counterexamples: Tuple[Counterexample, ...],
        suggestions: Tuple[str, ...],
    ) -> RuleCandidate:
        """Refine rule based on counterexamples."""
        if not counterexamples:
            return self.current_rule

        # Simplified refinement: broaden rule to include alternative interpretations
        # In real implementation, this would use more sophisticated logic

        # Extract unique actual interpretations from counterexamples
        actual_interps = {ce.actual for ce in counterexamples}

        # Build new description
        current_interp = _extract_interpretation_from_description(self.current_rule.description)
        all_interps = {current_interp} | actual_interps
        interp_str = " OR ".join(sorted(all_interps))

        new_description = f"{self.current_rule.pattern} pattern licenses {interp_str} interpretation (context-dependent)"

        # Create new manaat with additional constraints
        # (simplified: just copy old manaat)
        new_manaat = self.manaat

        # Create refinement trigger
        trigger = f"{len(counterexamples)} counterexample(s): " + ", ".join(ce.surface for ce in counterexamples)

        return self.current_rule.with_refinement(
            new_description=new_description,
            new_manaat=new_manaat,
            trigger=trigger,
            residuals=(
                Residual(
                    kind="refinement.incomplete",
                    description="Refinement based on counterexamples; needs further verification",
                ),
            ),
        )

    def _generate_cycle_explanations(
        self,
        rule_before: RuleCandidate,
        rule_after: RuleCandidate,
        verification: VerificationResult,
    ) -> Tuple[Explanation, ...]:
        """Generate explanations for this learning cycle."""
        explanations = []

        # Explain rule change
        if rule_before.description != rule_after.description:
            mod = rule_after.latest_modification
            if mod:
                explanations.append(
                    explain_modification(
                        mod,
                        learned=f"Pattern licenses multiple interpretations based on context",
                        confidence=0.75,
                    )
                )

        # Explain rank change
        if rule_before.rank != rule_after.rank:
            explanations.append(
                explain_rank_change(
                    before_rank=rule_before.rank,
                    after_rank=rule_after.rank,
                    trigger=f"{len(verification.counterexamples)} counterexample(s) found" if verification.counterexamples else "No counterexamples",
                    learned="Rule refined to handle counterexamples",
                )
            )

        return tuple(explanations)


# ===========================================================================
# Helpers
# ===========================================================================


def _extract_interpretation_from_description(description: str) -> str:
    """Extract interpretation from rule description."""
    description_lower = description.lower()
    if "agentive" in description_lower:
        return "agentive"
    elif "qualitative" in description_lower:
        return "qualitative"
    elif "patient" in description_lower:
        return "patient"
    else:
        return "unknown"


__all__ = [
    "LearningCycle",
    "GeneralLearner",
]
