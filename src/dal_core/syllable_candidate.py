"""
Syllable Candidate Layer (D1) - PR #30 + PR #32

Domain: SYLLABIC (D1)
Transition: Atom sequence → Syllable candidates
Purpose: Generate syllable structure candidates with boundaries

PR #30: Base syllable candidate generation
PR #32: Integrated D1 certification (Corr_D1 + Failure_D1 + RankPolicy_D1 + ProofObject_D1)

Implements:
- SyllableCandidate class following DalCandidateProtocol
- Syllable candidate generator (atom → syllable transitions)
- Syllable boundary detection
- Evidence-based syllable validation
- Integrated Corr_D1 validation in generation path
- D1FailureSet replacing generic residuals
- SyllableRankVector replacing simple confidence
- ProofObject_D1 for certification
"""

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4
import warnings

from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.syllables import (
    Syllable,
    SyllableType,
    handle_shadda,
    handle_tanwin,
    handle_sukun,
    handle_madd,
    is_long_vowel_sequence,
    validate_syllable_pattern
)
from dal_core.dal_algebra import (
    DalTransitionDomain,
    DalClaimScope,
    DalEvidence,
    DalCounterEvidence,
    DalTraceRef
)
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType

# PR #32: D1 certification imports
from dal_core.d1_correctness import validate_corr_d1, Corr_D1_Result, reverse_syllable_candidate
from dal_core.d1_failures import (
    D1FailureSet,
    D1Failure,
    make_missing_nucleus_failure,
    make_illegal_pattern_failure,
    make_atom_loss_failure,
    make_atom_order_violation_failure,
    make_trace_loss_failure,
    make_non_reversible_trace_failure
)
from dal_core.d1_rank_policy import SyllableRankVector, compute_syllable_rank
from dal_core.d1_proof import ProofObject_D1, create_proof


@dataclass
class SyllableCandidate:
    """
    Syllable Candidate (D1 Domain)

    Follows DalCandidateProtocol for typed transition algebra.

    Each candidate represents one possible syllabification of an atom sequence.
    Multiple candidates may exist for ambiguous sequences.

    PR #32 Updates:
    - failures: D1FailureSet (replaces residuals)
    - rank_vector: SyllableRankVector (replaces confidence)
    - proof: ProofObject_D1 (certification proof)
    - validate() method for integrated certification
    """
    # Required by DalCandidateProtocol
    candidate_id: str = field(default_factory=lambda: f"syl-{uuid4().hex[:8]}")
    domain: DalTransitionDomain = DalTransitionDomain.SYLLABIC
    evidence: List[DalEvidence] = field(default_factory=list)
    counter_evidence: List[DalCounterEvidence] = field(default_factory=list)

    # Syllable-specific fields
    syllable: Syllable = field(default_factory=lambda: Syllable(type=SyllableType.CV))
    source_atoms: List[ArabicAtom] = field(default_factory=list)
    span: tuple[int, int] = (0, 0)  # Position in source atom sequence

    # Transition metadata
    trace: Optional[DalTraceRef] = None

    # PR #32: New certification fields
    failures: D1FailureSet = field(default_factory=D1FailureSet)
    rank_vector: Optional[SyllableRankVector] = None
    proof: Optional[ProofObject_D1] = None

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

        # PR #32: Sync legacy residuals with failures for backward compatibility
        if self.residuals and not self.failures.failures:
            # If legacy residuals exist but no failures, keep residuals as primary
            pass
        elif self.failures.failures and not self.residuals:
            # If failures exist but no residuals, sync for backward compat
            self.residuals = self._convert_failures_to_residuals()

    def is_valid(self) -> bool:
        """Check if this candidate has no blocking issues.

        PR #32: Checks both proof certification and critical failures.

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

    def validate(self, original_atoms: List[ArabicAtom]) -> ProofObject_D1:
        """Run full D1 certification on this candidate.

        This integrates:
        - Corr_D1 validation
        - D1 failure detection
        - Rank vector computation
        - Proof object creation

        Args:
            original_atoms: Original atom sequence from D0

        Returns:
            ProofObject_D1 with certification result

        Side Effects:
            Updates self.failures, self.rank_vector, self.proof
        """
        # 1. Run Corr_D1 validation
        corr_result = validate_corr_d1(self, original_atoms)

        # 2. Convert Corr_D1 failures to D1FailureSet
        failure_set = self._convert_corr_to_failures(corr_result)

        # 3. Add failures from residuals (backward compat)
        for residual in self.residuals:
            if residual.is_blocker():
                # Add as critical failure
                failure_set.add(D1Failure(
                    failure_type=D1FailureType.TRACE_LOSS,  # Generic type
                    span=self.span,
                    message=residual.message,
                    severity=1.0,
                    context={'residual_type': str(residual.type)}
                ))

        # 4. Compute rank vector
        context = {
            'is_reversible_verified': self._verify_reversibility(original_atoms),
            'competing_candidate_count': 1  # Default, can be updated by set
        }
        rank_vector = compute_syllable_rank(self, context)

        # 5. Create proof object
        proof = create_proof(
            candidate_id=self.candidate_id,
            corr_result=corr_result,
            failure_set=failure_set,
            rank_vector=rank_vector,
            metadata={
                'domain': self.domain.value,
                'span': self.span,
                'syllable_type': self.syllable.type.value
            }
        )

        # 6. Update self
        self.failures = failure_set
        self.rank_vector = rank_vector
        self.proof = proof

        return proof

    def _convert_corr_to_failures(self, corr_result: Corr_D1_Result) -> D1FailureSet:
        """Convert Corr_D1 check results to D1 failures.

        Args:
            corr_result: Corr_D1 validation result

        Returns:
            D1FailureSet with typed failures
        """
        from dal_core.d1_failures import D1FailureType

        failure_set = D1FailureSet()

        for check in corr_result.failed_checks():
            # Map check name to failure type and create appropriate failure
            if check.name == "source_atoms_preserved":
                failure_set.add(make_atom_loss_failure(
                    span=self.span,
                    expected_count=check.evidence.get('expected_count', 0),
                    actual_count=check.evidence.get('actual_count', 0)
                ))
            elif check.name == "atom_order_preserved":
                failure_set.add(make_atom_order_violation_failure(
                    span=self.span,
                    position=check.evidence.get('position', 0)
                ))
            elif check.name == "no_atom_loss":
                failure_set.add(make_atom_loss_failure(
                    span=self.span,
                    expected_count=check.evidence.get('expected', 0),
                    actual_count=check.evidence.get('actual', 0)
                ))
            elif check.name == "nucleus_valid":
                failure_set.add(make_missing_nucleus_failure(
                    span=self.span,
                    onset_count=len(self.syllable.onset)
                ))
            elif check.name == "syllable_pattern_legal":
                failure_set.add(make_illegal_pattern_failure(
                    span=self.span,
                    attempted_pattern=check.evidence.get('type', 'UNKNOWN')
                ))
            elif check.name == "trace_exists" or check.name == "trace_actually_reversible":
                if not check.evidence.get('reversible', False):
                    failure_set.add(make_non_reversible_trace_failure(span=self.span))
                else:
                    failure_set.add(make_trace_loss_failure(span=self.span))
            else:
                # Generic failure for unknown check type
                failure_set.add(D1Failure(
                    failure_type=D1FailureType.TRACE_LOSS,
                    span=self.span,
                    message=check.reason,
                    severity=1.0,
                    context={'check_name': check.name}
                ))

        return failure_set

    def _verify_reversibility(self, original_atoms: List[ArabicAtom]) -> bool:
        """Actually verify reversibility (not just check flag).

        Args:
            original_atoms: Original atom sequence

        Returns:
            True if reverse operation succeeds and matches
        """
        try:
            reversed_atoms = reverse_syllable_candidate(self)
            start, end = self.span
            expected = original_atoms[start:end]
            return reversed_atoms == expected
        except Exception:
            return False

    def _convert_failures_to_residuals(self) -> List[Residual]:
        """Convert D1 failures to legacy residuals for backward compat.

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
class SyllableCandidateSet:
    """
    Set of syllable candidates for a word.

    Bounded candidate set (|candidates| < ∞).
    Preserves competitors for ambiguous syllabifications.
    """
    candidates: List[SyllableCandidate] = field(default_factory=list)
    source_atoms: List[ArabicAtom] = field(default_factory=list)
    global_residuals: List[Residual] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.candidates)

    def valid_candidates(self) -> List[SyllableCandidate]:
        """Return candidates without blockers."""
        return [c for c in self.candidates if c.is_valid()]

    def best_candidate(self) -> Optional[SyllableCandidate]:
        """Return highest confidence valid candidate, if any."""
        valid = self.valid_candidates()
        if not valid:
            return None
        return max(valid, key=lambda c: c.confidence)


def detect_syllable_boundaries(atoms: List[ArabicAtom]) -> List[tuple[int, int]]:
    """
    Detect syllable boundaries in atom sequence.

    Returns: List of (start, end) spans for each syllable.

    Arabic syllable patterns:
    - CV: consonant + short vowel
    - CVC: consonant + short vowel + consonant
    - CVV: consonant + long vowel
    - CVVC: consonant + long vowel + consonant
    - CVCC: consonant + short vowel + consonant + consonant
    """
    boundaries = []
    i = 0

    while i < len(atoms):
        # Skip non-structural atoms (marks, spaces, etc.)
        if atoms[i].kind in {AtomKind.SPACE, AtomKind.PUNCT}:
            i += 1
            continue

        # Syllable must start with consonant (onset)
        if atoms[i].kind != AtomKind.LETTER:
            # Invalid: syllable without onset
            # Skip and continue
            i += 1
            continue

        start = i
        onset_end = i + 1  # Single consonant onset

        # Check for nucleus (required)
        nucleus_start = onset_end
        nucleus_end = nucleus_start

        # Look for vowel
        if nucleus_start < len(atoms):
            # Check for long vowel sequence (CV + madd letter)
            if is_long_vowel_sequence(atoms, nucleus_start):
                nucleus_end = nucleus_start + 2  # vowel + letter
            elif atoms[nucleus_start].kind == AtomKind.VOWEL:
                nucleus_end = nucleus_start + 1
            elif atoms[nucleus_start].kind == AtomKind.SUKUN:
                # Sukun as nucleus (rare, word-final only)
                nucleus_end = nucleus_start + 1

        # Check for coda (optional)
        coda_start = nucleus_end
        coda_end = coda_start

        if coda_start < len(atoms):
            # Single consonant coda
            if atoms[coda_start].kind == AtomKind.LETTER:
                coda_end = coda_start + 1

                # Check for double consonant coda (CVCC)
                if coda_end < len(atoms) and atoms[coda_end].kind == AtomKind.LETTER:
                    # Check if next is also coda or starts new syllable
                    # For now, treat as single coda
                    pass

        # Create boundary
        end = max(nucleus_end, coda_end, onset_end)
        if end > start:
            boundaries.append((start, end))

        i = end

    return boundaries


def classify_syllable_type(
    onset: List[ArabicAtom],
    nucleus: List[ArabicAtom],
    coda: List[ArabicAtom]
) -> SyllableType:
    """
    Classify syllable based on structure.

    Returns: SyllableType enum value
    """
    has_long_nucleus = len(nucleus) > 1
    has_coda = len(coda) > 0
    has_double_coda = len(coda) > 1

    if has_double_coda:
        return SyllableType.CVCC
    elif has_long_nucleus and has_coda:
        return SyllableType.CVVC
    elif has_long_nucleus and not has_coda:
        return SyllableType.CVV
    elif not has_long_nucleus and has_coda:
        return SyllableType.CVC
    else:
        return SyllableType.CV


def generate_syllable_candidate(
    atoms: List[ArabicAtom],
    span: tuple[int, int],
    candidate_id: Optional[str] = None
) -> SyllableCandidate:
    """
    Generate a single syllable candidate from atom sequence.

    PR #32: Now includes integrated D1 certification.

    Args:
        atoms: Full atom sequence
        span: (start, end) indices for this syllable
        candidate_id: Optional explicit ID

    Returns:
        SyllableCandidate with integrated certification (failures, rank_vector, proof)
    """
    start, end = span
    syllable_atoms = atoms[start:end]

    # Separate onset, nucleus, coda
    onset = []
    nucleus = []
    coda = []
    residuals = []

    i = 0
    # Extract onset (consonant)
    while i < len(syllable_atoms) and syllable_atoms[i].kind == AtomKind.LETTER:
        onset.append(syllable_atoms[i])
        i += 1
        break  # Single consonant onset for now

    # Extract nucleus (vowel or long vowel)
    if i < len(syllable_atoms):
        if is_long_vowel_sequence(syllable_atoms, i):
            nucleus = [syllable_atoms[i], syllable_atoms[i + 1]]
            i += 2
        elif syllable_atoms[i].kind in {AtomKind.VOWEL, AtomKind.SUKUN}:
            nucleus.append(syllable_atoms[i])
            i += 1

    # Extract coda (consonant(s))
    while i < len(syllable_atoms) and syllable_atoms[i].kind == AtomKind.LETTER:
        coda.append(syllable_atoms[i])
        i += 1

    # Handle special atoms (shadda, tanwin)
    for atom in syllable_atoms:
        if atom.kind == AtomKind.SUKUN:
            sukun_residuals = handle_sukun(atom, 'coda' if coda else 'onset')
            residuals.extend(sukun_residuals)

    # Classify syllable type
    syll_type = classify_syllable_type(onset, nucleus, coda)

    # Create syllable
    syllable = Syllable(
        type=syll_type,
        onset=onset,
        nucleus=nucleus,
        coda=coda,
        trace={
            'span': span,
            'atom_count': len(syllable_atoms),
            'method': 'boundary_detection'
        }
    )

    # Validate syllable
    validation_residuals = validate_syllable_pattern(syllable)
    residuals.extend(validation_residuals)

    # Create evidence
    evidence = [
        DalEvidence(
            source="syllable_boundary_detection",
            claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
            span=span,
            confidence=0.9,
            details={
                'type': syll_type.value,
                'onset_count': len(onset),
                'nucleus_count': len(nucleus),
                'coda_count': len(coda)
            }
        )
    ]

    # Create trace
    trace = DalTraceRef(
        transition_id="d0-to-d1-syllabification",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        timestamp="",  # Would be filled by orchestrator
        reversible=True,
        metadata={
            'atoms_consumed': len(syllable_atoms),
            'syllable_type': syll_type.value
        }
    )

    # Legacy confidence (will be replaced by rank)
    confidence = 0.9 if not validation_residuals else 0.5

    # Create candidate (without certification yet)
    candidate = SyllableCandidate(
        candidate_id=candidate_id or f"syl-{uuid4().hex[:8]}",
        domain=DalTransitionDomain.SYLLABIC,
        evidence=evidence,
        counter_evidence=[],
        syllable=syllable,
        source_atoms=syllable_atoms,
        span=span,
        trace=trace,
        residuals=residuals,
        confidence=confidence
    )

    # PR #32: Run integrated D1 certification
    try:
        candidate.validate(atoms)
    except Exception as e:
        # If validation fails, create uncertified proof
        from dal_core.d1_proof import create_uncertified_proof
        candidate.proof = create_uncertified_proof(
            candidate_id=candidate.candidate_id,
            reason=f"Validation failed: {str(e)}"
        )

    return candidate


def generate_syllable_candidates(atoms: List[ArabicAtom]) -> SyllableCandidateSet:
    """
    Generate syllable candidates for entire atom sequence.

    This is the main D0 → D1 transition function.

    PR #32: Now includes integrated D1 certification for all candidates.

    Args:
        atoms: Atom sequence from D0 (GRAPHOPHONEMIC domain)

    Returns: SyllableCandidateSet with all candidates (with certification)
    """
    candidates = []
    global_residuals = []

    # Detect boundaries
    boundaries = detect_syllable_boundaries(atoms)

    if not boundaries:
        # No syllables detected - add warning
        global_residuals.append(make_warning(
            ResidualType.INVALID_SYLLABLE,
            "No syllable boundaries detected in atom sequence",
            location="syllabification"
        ))
        return SyllableCandidateSet(
            candidates=[],
            source_atoms=atoms,
            global_residuals=global_residuals
        )

    # Generate candidate for each boundary
    for i, span in enumerate(boundaries):
        candidate = generate_syllable_candidate(
            atoms=atoms,
            span=span,
            candidate_id=f"syl-{i:03d}"
        )
        candidates.append(candidate)

    # PR #32: Update ambiguity penalty for all candidates
    if len(candidates) > 1:
        for candidate in candidates:
            if candidate.rank_vector is not None:
                # Recompute with correct competing_candidate_count
                context = {
                    'competing_candidate_count': len(candidates),
                    'is_reversible_verified': candidate._verify_reversibility(atoms)
                }
                candidate.rank_vector = compute_syllable_rank(candidate, context)

    return SyllableCandidateSet(
        candidates=candidates,
        source_atoms=atoms,
        global_residuals=global_residuals
    )


# Convenience function for single-word syllabification
def syllabify_word(atoms: List[ArabicAtom]) -> List[SyllableCandidate]:
    """
    Syllabify a word (atom sequence) into syllable candidates.

    Returns: List of valid syllable candidates
    """
    candidate_set = generate_syllable_candidates(atoms)
    return candidate_set.valid_candidates()
