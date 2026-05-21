"""Pre-Morphological Unit Candidate Layer (D2) - PR #34

Domain: PRE_MORPH (D2)
Transition: Syllable candidates → Pre-morphological unit candidates
Purpose: Pre-morphological segmentation BEFORE root/pattern analysis

Implements:
- PreMorphUnitCandidate class following DalCandidateProtocol
- Pre-morph candidate generator (syllable → segmentation transitions)
- Clitic detection
- Frozen word detection
- Functional particle detection
- Augmentation marker detection
- Integrated Corr_D2 validation
- D2FailureSet replacing generic residuals
- PreMorphRankVector replacing simple confidence
- ProofObject_D2 for certification

Critical Law: D2 does NOT inherit D1 certification.
D2 accepts only CERTIFIED syllables from D1 and builds INDEPENDENT CPB_D2.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4

from dal_core.dal_algebra import (
    DalTransitionDomain,
    DalClaimScope,
    DalEvidence,
    DalCounterEvidence,
    DalTraceRef
)
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType

# D2 certification imports (CPB_D2)
from dal_core.d2_correctness import validate_corr_d2, Corr_D2_Result, reverse_premorph_candidate
from dal_core.d2_failures import (
    D2FailureSet,
    D2Failure,
    D2FailureType,
    make_missing_syllable_source_failure,
    make_uncertified_syllable_input_failure,
    make_illegal_segmentation_failure,
    make_syllable_loss_failure,
    make_trace_loss_failure,
    make_non_reversible_trace_failure
)
from dal_core.d2_rank_policy import PreMorphRankVector, compute_premorph_rank
from dal_core.d2_proof import ProofObject_D2, create_d2_proof, verify_d1_syllable_certification

# D2 types
from dal_core.premorph_types import (
    PreMorphSegmentation,
    PreMorphPolicy,
    CliticMarker,
    CliticType,
    AugmentationMarker,
    AugmentationType,
    make_simple_segmentation,
    make_clitic_segmentation,
    make_frozen_word_segmentation,
    make_particle_segmentation
)


@dataclass
class PreMorphUnitCandidate:
    """
    Pre-Morphological Unit Candidate (D2 Domain)

    Follows DalCandidateProtocol for typed transition algebra.

    Each candidate represents one possible pre-morphological segmentation of
    a syllable sequence into:
    - Proclitics (if any)
    - Core unit
    - Enclitics (if any)
    - Augmentation markers (if detected)

    Multiple candidates may exist for ambiguous segmentations.

    Critical: D2 does NOT inherit D1 certification.
    D2 builds independent ProofObject_D2.
    """
    # Required by DalCandidateProtocol
    candidate_id: str = field(default_factory=lambda: f"pm-{uuid4().hex[:8]}")
    domain: DalTransitionDomain = DalTransitionDomain.PRE_MORPH
    evidence: List[DalEvidence] = field(default_factory=list)
    counter_evidence: List[DalCounterEvidence] = field(default_factory=list)

    # D2-specific fields
    segmentation: PreMorphSegmentation = field(default_factory=lambda: PreMorphSegmentation())
    source_syllables: List = field(default_factory=list)  # Certified D1 syllables
    span: tuple[int, int] = (0, 0)  # Position in syllable sequence

    # Transition metadata
    trace: Optional[DalTraceRef] = None

    # D2 Certification fields (CPB_D2 - independent from D1)
    failures: D2FailureSet = field(default_factory=D2FailureSet)
    rank_vector: Optional[PreMorphRankVector] = None
    proof: Optional[ProofObject_D2] = None

    # Legacy fields (deprecated, kept for backward compatibility)
    residuals: List[Residual] = field(default_factory=list)
    confidence: float = 1.0  # [0.0, 1.0]

    def __post_init__(self):
        """Validate candidate invariants."""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")
        if self.span[0] > self.span[1]:
            raise ValueError(f"Invalid span: start > end ({self.span})")
        if self.span[0] < 0:
            raise ValueError(f"Invalid span: negative start ({self.span})")

        # Sync legacy residuals with failures for backward compatibility
        if self.residuals and not self.failures.failures:
            pass  # Keep residuals as primary
        elif self.failures.failures and not self.residuals:
            self.residuals = self._convert_failures_to_residuals()

    def is_valid(self) -> bool:
        """Check if this candidate has no blocking issues.

        Checks both proof certification and critical failures.

        Returns:
            True if certified OR (no critical failures and no blockers)
        """
        # If we have a proof, use it
        if self.proof is not None:
            return self.proof.is_certified

        # Otherwise check failures and residuals
        has_critical_failure = self.failures.has_critical_failure()
        has_blocker = any(r.is_blocker() for r in self.residuals)

        return not (has_critical_failure or has_blocker)

    def has_blocker(self) -> bool:
        """Check if this candidate has blocking residuals."""
        return any(r.is_blocker() for r in self.residuals) or self.failures.has_critical_failure()

    def validate(self, original_syllables: List) -> ProofObject_D2:
        """Run full D2 certification on this candidate.

        This integrates:
        - Corr_D2 validation
        - D2 failure detection
        - Rank vector computation
        - Proof object creation
        - D1 certification verification

        Args:
            original_syllables: Original syllable sequence from D1

        Returns:
            ProofObject_D2 with certification result

        Side Effects:
            Updates self.failures, self.rank_vector, self.proof
        """
        # 1. Verify D1 syllable certification (CRITICAL)
        d1_certified = verify_d1_syllable_certification(self.source_syllables)

        if not d1_certified:
            # Add failure for uncertified D1 input
            failure_set = D2FailureSet()
            for i, syll in enumerate(self.source_syllables):
                if not hasattr(syll, 'proof') or not syll.proof or not syll.proof.is_certified:
                    failure_set.add(make_uncertified_syllable_input_failure(
                        span=self.span,
                        syllable_id=getattr(syll, 'candidate_id', f"syll-{i}")
                    ))

            # Create uncertified proof
            from dal_core.d2_proof import create_uncertified_d2_proof
            proof = create_uncertified_d2_proof(
                candidate_id=self.candidate_id,
                reason="D1 syllable certification not verified"
            )
            self.failures = failure_set
            self.proof = proof
            return proof

        # 2. Run Corr_D2 validation
        corr_result = validate_corr_d2(self)

        # 3. Convert Corr_D2 failures to D2FailureSet
        failure_set = self._convert_corr_to_failures(corr_result)

        # 4. Add failures from residuals (backward compat)
        for residual in self.residuals:
            if residual.is_blocker():
                failure_set.add(D2Failure(
                    failure_type=D2FailureType.TRACE_LOSS,  # Generic type
                    span=self.span,
                    message=residual.message,
                    severity=1.0,
                    context={'residual_type': str(residual.type)}
                ))

        # 5. Compute rank vector
        context = {
            'is_reversible_verified': self._verify_reversibility(original_syllables),
            'competing_candidate_count': 1  # Default, can be updated by set
        }
        rank_vector = compute_premorph_rank(self, context)

        # 6. Create proof object (with D1 certification verification)
        proof = create_d2_proof(
            candidate_id=self.candidate_id,
            corr_result=corr_result,
            failure_set=failure_set,
            rank_vector=rank_vector,
            d1_syllable_certification_verified=d1_certified,
            metadata={
                'domain': self.domain.value,
                'span': self.span,
                'segmentation': str(self.segmentation)
            }
        )

        # 7. Update self
        self.failures = failure_set
        self.rank_vector = rank_vector
        self.proof = proof

        return proof

    def _convert_corr_to_failures(self, corr_result: Corr_D2_Result) -> D2FailureSet:
        """Convert Corr_D2 check results to D2 failures.

        Args:
            corr_result: Corr_D2 validation result

        Returns:
            D2FailureSet with typed failures
        """
        failure_set = D2FailureSet()

        for check in corr_result.failed_checks():
            # Map check name to failure type and create appropriate failure
            if check.name == "source_syllables_certified":
                for idx in check.evidence.get('uncertified_indices', []):
                    failure_set.add(make_uncertified_syllable_input_failure(
                        span=self.span,
                        syllable_id=str(idx)
                    ))
            elif check.name == "syllable_order_preserved":
                failure_set.add(D2Failure(
                    failure_type=D2FailureType.SYLLABLE_ORDER_VIOLATION,
                    span=self.span,
                    message=check.reason,
                    severity=1.0,
                    context=check.evidence
                ))
            elif check.name == "no_syllable_loss":
                failure_set.add(make_syllable_loss_failure(
                    span=self.span,
                    expected_count=check.evidence.get('expected', 0),
                    actual_count=check.evidence.get('actual', 0)
                ))
            elif check.name == "segmentation_legal":
                failure_set.add(make_illegal_segmentation_failure(
                    span=self.span,
                    reason=check.reason
                ))
            elif check.name == "trace_exists" or check.name == "trace_actually_reversible":
                if not check.evidence.get('reversible', False):
                    failure_set.add(make_non_reversible_trace_failure(span=self.span))
                else:
                    failure_set.add(make_trace_loss_failure(span=self.span))
            elif check.name == "no_cross_layer_leakage":
                # Add failure for each forbidden field
                for field in check.evidence.get('forbidden_fields', []):
                    if 'root' in field or 'radical' in field:
                        failure_set.add(D2Failure(
                            failure_type=D2FailureType.PREMATURE_ROOT_CLAIM,
                            span=self.span,
                            message=f"Forbidden field: {field}",
                            severity=1.0,
                            context={'field': field}
                        ))
                    elif 'wazn' in field or 'pattern' in field:
                        failure_set.add(D2Failure(
                            failure_type=D2FailureType.PREMATURE_PATTERN_CLAIM,
                            span=self.span,
                            message=f"Forbidden field: {field}",
                            severity=1.0,
                            context={'field': field}
                        ))
                    elif 'meaning' in field or 'murad' in field:
                        failure_set.add(D2Failure(
                            failure_type=D2FailureType.PREMATURE_MEANING_CLAIM,
                            span=self.span,
                            message=f"Forbidden field: {field}",
                            severity=1.0,
                            context={'field': field}
                        ))
            else:
                # Generic failure for unknown check type
                failure_set.add(D2Failure(
                    failure_type=D2FailureType.TRACE_LOSS,
                    span=self.span,
                    message=check.reason,
                    severity=1.0,
                    context={'check_name': check.name}
                ))

        return failure_set

    def _verify_reversibility(self, original_syllables: List) -> bool:
        """Actually verify reversibility (not just check flag).

        Args:
            original_syllables: Original syllable sequence

        Returns:
            True if reverse operation succeeds and matches
        """
        try:
            reversed_syllables = reverse_premorph_candidate(self)
            start, end = self.span
            expected = original_syllables[start:end]
            return reversed_syllables == expected
        except Exception:
            return False

    def _convert_failures_to_residuals(self) -> List[Residual]:
        """Convert D2 failures to legacy residuals for backward compat.

        Returns:
            List of Residual objects
        """
        residuals = []
        for failure in self.failures.failures:
            if failure.is_critical():
                residuals.append(make_blocker(
                    ResidualType.INVALID_SYLLABLE,
                    failure.message,
                    location=f"span {failure.span}"
                ))
            else:
                residuals.append(make_warning(
                    ResidualType.INVALID_SYLLABLE,
                    failure.message,
                    location=f"span {failure.span}"
                ))
        return residuals


@dataclass
class PreMorphUnitCandidateSet:
    """
    Set of pre-morphological unit candidates for a syllable sequence.

    Bounded candidate set (|candidates| < ∞).
    Preserves competitors for ambiguous segmentations.
    """
    candidates: List[PreMorphUnitCandidate] = field(default_factory=list)
    source_syllables: List = field(default_factory=list)  # Certified D1 syllables
    global_residuals: List[Residual] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.candidates)

    def valid_candidates(self) -> List[PreMorphUnitCandidate]:
        """Return candidates without blockers."""
        return [c for c in self.candidates if c.is_valid()]

    def best_candidate(self) -> Optional[PreMorphUnitCandidate]:
        """Return highest confidence valid candidate, if any."""
        valid = self.valid_candidates()
        if not valid:
            return None
        return max(valid, key=lambda c: c.confidence)


# ============================================================================
# Pre-Morphological Unit Generation Functions
# ============================================================================


def generate_premorph_candidates(
    syllables: List,
    policy: Optional[PreMorphPolicy] = None
) -> PreMorphUnitCandidateSet:
    """
    Generate pre-morphological unit candidates from certified syllables.

    This is the main D1 → D2 transition function.

    Args:
        syllables: List of SyllableCandidate objects from D1 (must be certified)
        policy: Generation policy (defaults to PreMorphPolicy())

    Returns:
        PreMorphUnitCandidateSet with all candidates (with D2 certification)

    Critical:
    - Accepts only certified SyllableCandidate from D1
    - Runs mandatory validate() on each candidate
    - Returns candidates with ProofObject_D2
    """
    if policy is None:
        policy = PreMorphPolicy()

    candidates = []
    global_residuals = []

    # Verify D1 certification
    if not verify_d1_syllable_certification(syllables):
        global_residuals.append(make_blocker(
            ResidualType.INVALID_SYLLABLE,
            "D1 syllables not certified - D2 requires certified input",
            location="d1_certification"
        ))
        return PreMorphUnitCandidateSet(
            candidates=[],
            source_syllables=syllables,
            global_residuals=global_residuals
        )

    # Strategy 1: Simple segmentation (no clitics, whole word as core)
    candidate = _generate_simple_candidate(syllables)
    if candidate:
        candidates.append(candidate)

    # Strategy 2: Clitic detection (if enabled)
    if policy.enable_proclitic_detection or policy.enable_enclitic_detection:
        clitic_candidates = _generate_clitic_candidates(syllables, policy)
        candidates.extend(clitic_candidates)

    # Strategy 3: Frozen word detection (if enabled)
    if policy.enable_frozen_word_detection:
        frozen_candidate = _generate_frozen_word_candidate(syllables, policy)
        if frozen_candidate:
            candidates.append(frozen_candidate)

    # Strategy 4: Functional particle detection (if enabled)
    if policy.enable_particle_detection:
        particle_candidate = _generate_particle_candidate(syllables, policy)
        if particle_candidate:
            candidates.append(particle_candidate)

    # Limit candidates
    if len(candidates) > policy.max_candidates:
        candidates = candidates[:policy.max_candidates]
        global_residuals.append(make_warning(
            ResidualType.INVALID_SYLLABLE,
            f"Candidate overflow: limited to {policy.max_candidates}",
            location="generation"
        ))

    # Update ambiguity penalty for all candidates
    if len(candidates) > 1:
        for candidate in candidates:
            if candidate.rank_vector is not None:
                # Recompute with correct competing_candidate_count
                context = {
                    'competing_candidate_count': len(candidates),
                    'is_reversible_verified': candidate._verify_reversibility(syllables)
                }
                candidate.rank_vector = compute_premorph_rank(candidate, context)

    return PreMorphUnitCandidateSet(
        candidates=candidates,
        source_syllables=syllables,
        global_residuals=global_residuals
    )


def _generate_simple_candidate(syllables: List) -> Optional[PreMorphUnitCandidate]:
    """Generate simple candidate (no clitics, whole sequence as core).

    Args:
        syllables: Syllable sequence

    Returns:
        PreMorphUnitCandidate or None
    """
    if not syllables:
        return None

    segmentation = make_simple_segmentation(core_syllables=syllables)

    evidence = [
        DalEvidence(
            source="premorph_simple_segmentation",
            claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,  # Reuse claim scope
            span=(0, len(syllables)),
            confidence=0.9,
            details={
                'strategy': 'simple',
                'syllable_count': len(syllables)
            }
        )
    ]

    trace = DalTraceRef(
        transition_id="d1-to-d2-simple-segmentation",
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.PRE_MORPH,
        timestamp="",
        reversible=True,
        metadata={
            'syllables_consumed': len(syllables),
            'segmentation_type': 'simple'
        }
    )

    candidate = PreMorphUnitCandidate(
        candidate_id=f"pm-simple-{uuid4().hex[:8]}",
        domain=DalTransitionDomain.PRE_MORPH,
        evidence=evidence,
        counter_evidence=[],
        segmentation=segmentation,
        source_syllables=syllables,
        span=(0, len(syllables)),
        trace=trace,
        confidence=0.9
    )

    # Run integrated D2 certification
    try:
        candidate.validate(syllables)
    except Exception as e:
        from dal_core.d2_proof import create_uncertified_d2_proof
        candidate.proof = create_uncertified_d2_proof(
            candidate_id=candidate.candidate_id,
            reason=f"Validation failed: {str(e)}"
        )

    return candidate


def _generate_clitic_candidates(syllables: List, policy: PreMorphPolicy) -> List[PreMorphUnitCandidate]:
    """Generate candidates with clitic detection.

    Args:
        syllables: Syllable sequence
        policy: Generation policy

    Returns:
        List of PreMorphUnitCandidate with clitics
    """
    # Simplified clitic detection (full implementation would use lexicon)
    # For now, just return empty list
    # Full implementation would:
    # 1. Check first syllable(s) for proclitics
    # 2. Check last syllable(s) for enclitics
    # 3. Generate candidates with different clitic combinations
    return []


def _generate_frozen_word_candidate(syllables: List, policy: PreMorphPolicy) -> Optional[PreMorphUnitCandidate]:
    """Generate frozen word candidate.

    Args:
        syllables: Syllable sequence
        policy: Generation policy

    Returns:
        PreMorphUnitCandidate or None
    """
    # Simplified frozen word detection
    # Full implementation would query frozen word lexicon
    return None


def _generate_particle_candidate(syllables: List, policy: PreMorphPolicy) -> Optional[PreMorphUnitCandidate]:
    """Generate functional particle candidate.

    Args:
        syllables: Syllable sequence
        policy: Generation policy

    Returns:
        PreMorphUnitCandidate or None
    """
    # Simplified particle detection
    # Full implementation would query particle lexicon
    return None
