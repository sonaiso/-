"""Minimal Dal Transition Signature.

PR #22: Licensed-transition contracts for ordered bounded dal sequences.

This module defines the MINIMAL signature for dal transitions, respecting
PR #21 governance: dal = ordered bounded sequence, not bag of features.

Out of scope:
- No analyzers
- No RelationCandidate
- No CaseEffectCandidate
- No Rank Algebra implementation
- No Residual Algebra implementation
- No refactoring existing classes to inherit from base classes
- No semantic interpretation
- No i'rab
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol, TypeVar, Generic, List, Tuple, Optional, Any, Set
from abc import abstractmethod


# =============================================================================
# DOMAIN ENUMS
# =============================================================================

class DalTransitionDomain(Enum):
    """Transition domains for dal analysis.

    Based on PR #21: Each domain operates on ordered bounded sequences,
    not bags of features.
    """
    GRAPHOPHONEMIC = auto()  # D0: رسم/صوت
    SYLLABIC = auto()         # D1: مقطع
    PRE_MORPH = auto()        # D2: ما قبل الصرف
    ORIGIN = auto()           # D3: أصل (root/frozen)
    TEMPLATE = auto()          # D4: وزن
    IDENTITY_AXIS = auto()    # D5: محور الهوية (lexical identity)
    DIRECTIONAL_ANALYSIS = auto()  # D6: تحليل اتجاهي (bidirectional scan)
    JUDGMENT = auto()         # D7: حكم (final categorization)


class DalClaimScope(Enum):
    """Scope of claims made during transitions.

    PR #21 governance: No claim without position.
    Every claim must be scoped to specific indices.
    """
    SINGLE_POSITION = auto()   # Claim about one position
    SPAN = auto()              # Claim about contiguous span
    ADJACENCY = auto()         # Claim about two adjacent positions
    FOLD = auto()              # Claim about folded units
    BOUNDARY = auto()          # Claim about boundary condition


# =============================================================================
# EVIDENCE & COUNTER-EVIDENCE
# =============================================================================

@dataclass(frozen=True)
class DalEvidence:
    """Evidence supporting a dal transition claim.

    PR #21 Invariant 5: No certificate without claim-scoped evidence.

    Evidence must specify:
    - Which positions it applies to (span)
    - What observation supports the claim
    - Source domain of observation
    """
    claim_scope: DalClaimScope
    span: Tuple[int, int]  # (start_index, end_index) - required by PR #21
    observation: str
    source_domain: DalTransitionDomain
    confidence: float = 1.0

    def __post_init__(self):
        """Validate evidence respects PR #21 governance."""
        if self.span[0] < 0 or self.span[1] < self.span[0]:
            raise ValueError(f"Invalid span {self.span}: violates ordered sequence")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence {self.confidence} must be in [0,1]")


@dataclass(frozen=True)
class DalCounterEvidence:
    """Evidence against a dal transition claim.

    PR #21: Counter-evidence must also be position-scoped.
    """
    claim_scope: DalClaimScope
    span: Tuple[int, int]
    blocking_observation: str
    source_domain: DalTransitionDomain
    severity: float = 1.0  # How strongly it blocks (0=weak, 1=absolute)


# =============================================================================
# POLICIES
# =============================================================================

class ShortcutPolicy(Enum):
    """Policy for direct cross-layer transitions.

    Based on repository memory: "Prohibited cross-layer promotions".

    PR #21: Direct promotions are forbidden unless explicitly licensed
    with lexicon/attestation or intermediate trace.
    """
    FORBIDDEN = auto()         # No direct jump allowed
    LEXICON_ATTESTED = auto()  # Allowed if in closed lexicon
    WITH_TRACE = auto()        # Allowed if trace path provided


class EvidenceRequirement(Enum):
    """How much evidence is required for a transition."""
    NONE = auto()              # No evidence needed (structural only)
    WEAK = auto()              # At least one piece of evidence
    STRONG = auto()            # Multiple converging evidence
    UNANIMOUS = auto()         # No counter-evidence allowed


class CandidateBudgetPolicy(Enum):
    """Policy for how many candidates a transition can emit."""
    UNIQUE = auto()            # Exactly one candidate
    BOUNDED = auto()           # Fixed upper limit
    UNBOUNDED = auto()         # No limit (use with caution)


# =============================================================================
# TRANSITION TRACE
# =============================================================================

@dataclass(frozen=True)
class DalTrace:
    """Transition trace for reverse recoverability.

    PR #21 Invariant 2: No fold without reverse trace.
    """
    source_domain: DalTransitionDomain
    target_domain: DalTransitionDomain
    operation: str
    input_spans: List[Tuple[int, int]]  # Which positions were consumed
    output_span: Tuple[int, int]        # What position was produced

    def is_reversible(self) -> bool:
        """Check if trace allows reverse operation."""
        return len(self.input_spans) > 0 and self.output_span[0] >= 0


# =============================================================================
# PROTOCOLS (STRUCTURAL TYPING)
# =============================================================================

T_Input = TypeVar('T_Input')
T_Output = TypeVar('T_Output')


class DalCandidateProtocol(Protocol):
    """Protocol for dal candidates.

    PR #21 Invariant 4: No candidate without boundaries.

    Every candidate must specify its span within parent sequence.
    """

    @property
    def span(self) -> Tuple[int, int]:
        """Span within parent sequence (required by PR #21)."""
        ...

    @property
    def claim_scope(self) -> DalClaimScope:
        """Scope of the claim this candidate makes."""
        ...


class DalCandidateSetProtocol(Protocol[T_Output]):
    """Protocol for candidate sets.

    PR #21: Candidate sets must preserve ordering and trace.
    """

    @property
    def candidates(self) -> List[T_Output]:
        """Ordered list of candidates (preserves sequence order)."""
        ...

    @property
    def domain(self) -> DalTransitionDomain:
        """Which domain these candidates belong to."""
        ...

    def is_empty(self) -> bool:
        """Check if candidate set is empty (allowed explicitly)."""
        ...


class DalTransitionContract(Protocol[T_Input, T_Output]):
    """Contract for licensed dal transitions.

    PR #21 compliance:
    - Input must be ordered bounded sequence
    - Output preserves boundaries and trace
    - Evidence must be claim-scoped
    """

    @property
    def source_domain(self) -> DalTransitionDomain:
        """Source domain of transition."""
        ...

    @property
    def target_domain(self) -> DalTransitionDomain:
        """Target domain of transition."""
        ...

    @property
    def shortcut_policy(self) -> ShortcutPolicy:
        """Whether this transition shortcuts layers."""
        ...

    @property
    def evidence_requirement(self) -> EvidenceRequirement:
        """How much evidence is required."""
        ...

    @abstractmethod
    def apply(
        self,
        input_unit: T_Input,
        evidence: List[DalEvidence],
    ) -> DalCandidateSetProtocol[T_Output]:
        """Apply transition to produce candidates.

        Args:
            input_unit: Ordered bounded sequence (PR #21)
            evidence: Claim-scoped evidence list (PR #21 Invariant 5)

        Returns:
            Candidate set with boundaries and trace
        """
        ...


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_transition_contract(
    contract: Any,
    require_domain: bool = True,
    require_policy: bool = True,
) -> List[str]:
    """Validate transition contract compliance.

    Returns:
        List of validation errors (empty if valid)
    """
    errors: List[str] = []

    if require_domain:
        if not hasattr(contract, 'source_domain'):
            errors.append("Missing source_domain")
        if not hasattr(contract, 'target_domain'):
            errors.append("Missing target_domain")

    if require_policy:
        if not hasattr(contract, 'shortcut_policy'):
            errors.append("Missing shortcut_policy")
        if not hasattr(contract, 'evidence_requirement'):
            errors.append("Missing evidence_requirement")

    if not hasattr(contract, 'apply'):
        errors.append("Missing apply method")

    return errors


def validate_candidate_set_shape(
    candidate_set: Any,
    allow_empty: bool = True,
    require_boundaries: bool = True,
) -> List[str]:
    """Validate candidate set structure.

    PR #21 Invariant 4: Candidates must have boundaries.

    Returns:
        List of validation errors (empty if valid)
    """
    errors: List[str] = []

    if not hasattr(candidate_set, 'candidates'):
        errors.append("Missing candidates property")
        return errors

    candidates = candidate_set.candidates

    if not allow_empty and len(candidates) == 0:
        errors.append("Empty candidate set not allowed")

    if require_boundaries:
        for i, cand in enumerate(candidates):
            if not hasattr(cand, 'span'):
                errors.append(f"Candidate {i} missing span (violates PR #21)")
            elif not isinstance(cand.span, tuple) or len(cand.span) != 2:
                errors.append(f"Candidate {i} has invalid span format")

    return errors


def validate_no_direct_promotion(
    source_domain: DalTransitionDomain,
    target_domain: DalTransitionDomain,
    shortcut_policy: ShortcutPolicy,
    lexicon_attested: bool = False,
    trace_provided: bool = False,
) -> List[str]:
    """Validate no prohibited cross-layer promotions.

    Based on repository memory: "Prohibited cross-layer promotions"
    - رسم/صوت → وزن (grapheme/phoneme to pattern): FORBIDDEN
    - مقطع → أصل (syllable to root): FORBIDDEN
    - وزن ظاهر → وزن عميق (surface to deep pattern): FORBIDDEN
    - جامد → جذر (frozen to root): FORBIDDEN
    - مبني → وزن صرفي (built to morph pattern): FORBIDDEN

    Each layer jump requires intermediate contract.

    Returns:
        List of violations (empty if valid)
    """
    violations: List[str] = []

    # Calculate layer distance
    layer_distance = abs(target_domain.value - source_domain.value)

    # Direct cross-layer jump (distance > 1)
    if layer_distance > 1:
        if shortcut_policy == ShortcutPolicy.FORBIDDEN:
            violations.append(
                f"Direct promotion from {source_domain.name} to {target_domain.name} "
                f"forbidden (layer distance {layer_distance})"
            )
        elif shortcut_policy == ShortcutPolicy.LEXICON_ATTESTED:
            if not lexicon_attested:
                violations.append(
                    f"Shortcut {source_domain.name} → {target_domain.name} "
                    f"requires lexicon attestation"
                )
        elif shortcut_policy == ShortcutPolicy.WITH_TRACE:
            if not trace_provided:
                violations.append(
                    f"Shortcut {source_domain.name} → {target_domain.name} "
                    f"requires intermediate trace"
                )

    return violations


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Domain enums
    'DalTransitionDomain',
    'DalClaimScope',
    # Evidence
    'DalEvidence',
    'DalCounterEvidence',
    # Policies
    'ShortcutPolicy',
    'EvidenceRequirement',
    'CandidateBudgetPolicy',
    # Trace
    'DalTrace',
    # Protocols
    'DalCandidateProtocol',
    'DalCandidateSetProtocol',
    'DalTransitionContract',
    # Validation
    'validate_transition_contract',
    'validate_candidate_set_shape',
    'validate_no_direct_promotion',
]
