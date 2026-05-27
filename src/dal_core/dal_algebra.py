"""Minimal Dal Transition Signature.

PR #23: Lightweight runtime foundation for dal candidate layers.

This module implements the minimal licensed-transition signature
for future dal candidate layers. It does NOT implement full Dal Algebra.

Obeys PR #21 (Ordered Dal Form Governance):
- A dal form is an ordered bounded sequence, not a bag of features.
- No claim without position.
- No fold without reverse trace.
- No adjacency without direction.
- No candidate without boundaries.
- No certificate without claim-scoped evidence.

Obeys PR #22 (Project Algebra Architecture Map):
- 𝔾 = successful typed objects.
- Failure ∉ 𝔾.
- Transitions return CandidateSet[𝔾] or AlgebraicFailure.
- No algebra may claim outputs of later algebra.

PR #1C (Hybrid Failure Semantics):
- Construction invariant violation → Exception (ValueError, TypeError)
- Algebraic operation failure → AlgebraicFailure value
- Preserves algebraic closure while maintaining construction safety
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol, List, Any, Optional, Set, TypeVar, Generic, Tuple, Mapping
from abc import abstractmethod
from types import MappingProxyType


# ============================================================================
# Domain and Scope Enums
# ============================================================================


class DalTransitionDomain(Enum):
    """8-layer transition domain architecture (D0-D7).

    This is a partial transition network (شبكة انتقالات جزئية),
    not a single pipeline. Different words follow different paths.
    """
    GRAPHOPHONEMIC = auto()      # D0: رسم/صوت - Carrier → Atom
    SYLLABIC = auto()            # D1: مقطع - Atom → Syllable
    PRE_MORPH = auto()           # D2: ما قبل الصرف - Pre-morphological classification
    ORIGIN = auto()              # D3: أصل - Root/frozen/functional classification
    TEMPLATE = auto()            # D4: وزن - Pattern matching
    IDENTITY_AXIS = auto()       # D5: محور الهوية - Ism/Fi'l/Harf classification
    DIRECTIONAL_ANALYSIS = auto() # D6: تحليل اتجاهي - Bidirectional form analysis
    JUDGMENT = auto()            # D7: حكم صرفي - Morphological judgment


class DalClaimScope(Enum):
    """Scope of claim for dal certificate.

    No global certificate. All certificates are claim-scoped.
    """
    CARRIER_VALID = auto()           # Unicode carrier is valid Arabic
    ATOM_SEQUENCE_VALID = auto()     # Atom sequence is well-formed
    SYLLABLE_STRUCTURE_VALID = auto() # Syllable structure is valid
    ORIGIN_CLASSIFIED = auto()       # Origin is classified (root/frozen/functional)
    TEMPLATE_MATCHED = auto()        # Template pattern matched
    IDENTITY_DETERMINED = auto()     # Identity axis determined (Ism/Fi'l/Harf)
    FORM_ANALYZED = auto()           # Form analysis complete
    JUDGMENT_ISSUED = auto()         # Morphological judgment issued
    # Composition claims (dal-murakkab)
    FRAME_STRUCTURE_VALID = auto()   # Sentence frame structure valid
    CASE_SIGNS_OBSERVED = auto()     # Surface case signs observed
    OPERATOR_TRIGGERED = auto()      # Operator trigger potential identified
    # FORBIDDEN: meaning, murad, hukm claims


class EvidenceRequirement(Enum):
    """Evidence requirement for transition."""
    NONE = auto()              # No evidence required (structural only)
    LEXICON_LOOKUP = auto()    # Requires lexicon attestation
    CONTEXT = auto()           # Requires context evidence
    ATTESTATION = auto()       # Requires explicit attestation
    TRACE = auto()             # Requires transformation trace


class ShortcutPolicy(Enum):
    """Policy for allowing shortcuts across layers."""
    FORBIDDEN = auto()         # No shortcuts allowed
    CLOSED_CLASS_ONLY = auto() # Only for closed-class items (particles, etc.)
    WITH_ATTESTATION = auto()  # Allowed with explicit attestation
    ALLOWED = auto()           # Shortcuts allowed


class CandidateBudgetPolicy(Enum):
    """Policy for candidate set size."""
    UNBOUNDED = auto()         # No limit (dangerous, use with caution)
    SMALL = auto()             # ≤ 10 candidates
    MEDIUM = auto()            # ≤ 100 candidates
    LARGE = auto()             # ≤ 1000 candidates
    CUSTOM = auto()            # Custom limit specified in contract


# ============================================================================
# Evidence and Trace Models
# ============================================================================


@dataclass(frozen=True)
class DalEvidence:
    """Evidence for dal transition or claim.

    Certificate must be claim-scoped, not global.
    Evidence must include span (position in ordered sequence).
    """
    source: str                    # Evidence source (lexicon, rule, observation)
    claim_scope: DalClaimScope     # Scope of this evidence
    span: tuple[int, int]          # Position span in ordered sequence (start, end)
    confidence: float = 1.0        # Confidence [0.0, 1.0]
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate evidence invariants."""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")
        if self.span[0] > self.span[1]:
            raise ValueError(f"Invalid span: start > end ({self.span})")
        if self.span[0] < 0:
            raise ValueError(f"Invalid span: negative start ({self.span})")


@dataclass(frozen=True)
class DalCounterEvidence:
    """Counter-evidence against a transition or claim."""
    source: str                    # Counter-evidence source
    claim_scope: DalClaimScope     # Scope of counter-evidence
    span: tuple[int, int]          # Position span
    severity: float = 1.0          # Severity [0.0, 1.0]
    reason: str = ""               # Why this is counter-evidence

    def __post_init__(self):
        """Validate counter-evidence invariants."""
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError(f"Severity must be in [0.0, 1.0], got {self.severity}")
        if self.span[0] > self.span[1]:
            raise ValueError(f"Invalid span: start > end ({self.span})")
        if self.span[0] < 0:
            raise ValueError(f"Invalid span: negative start ({self.span})")


@dataclass(frozen=True)
class DalTraceRef:
    """Reference to transformation trace.

    Enables reverse trace (fold with reversibility).
    """
    transition_id: str             # Which transition produced this
    source_domain: DalTransitionDomain
    target_domain: DalTransitionDomain
    timestamp: str                 # When transition occurred
    reversible: bool = False       # Can this be reversed?
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Algebraic Failure Model (PR-1C)
# ============================================================================


@dataclass(frozen=True)
class AlgebraicFailure:
    """Algebraic operation failure value.

    PR #1C: Hybrid Failure Semantics

    Represents failure of an algebraic operation (NOT construction failure).
    Construction failures should raise ValueError/TypeError in __post_init__.

    This is a VALUE in the algebra, not an exception.
    It enables algebraic composability while preserving failure information.

    Examples of when to use AlgebraicFailure:
    - Gate not satisfied
    - Evidence insufficient
    - Rank not licensed
    - Residual blocking operation
    - Domain boundary violation during operation
    - Forbidden path attempted
    - Minimal sufficiency not met

    Examples of when to raise Exception instead:
    - Invalid field values in __post_init__ (e.g., negative probability)
    - Missing required structural fields
    - Invalid enum combinations
    - Type mismatches
    - Attempt to forge ApprovedTransitionContext

    Mathematical Type:
        Opₑ : A → Success[B] ∪ AlgebraicFailure

    where A is valid input (construction already validated).

    Immutability:
        All fields are truly immutable. Lists/dicts passed to constructor
        are converted to tuple/MappingProxyType in __post_init__.
    """
    reason: str                           # Human-readable failure reason
    gate: Optional[str] = None            # Which gate was not satisfied
    evidence_gap: Optional[str] = None    # What evidence was missing
    rank_issue: Optional[str] = None      # Rank-related problem
    residual_block: Optional[str] = None  # Blocking residual description
    domain_violation: Optional[str] = None  # Domain boundary crossed
    forbidden_path: Optional[str] = None  # Forbidden transition attempted
    counter_evidence: Tuple[DalCounterEvidence, ...] = ()
    trace: Tuple[DalTraceRef, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate failure invariants and enforce true immutability.

        Note: Even failure values must have valid construction.
        This method coerces mutable inputs to immutable types.
        """
        if not self.reason:
            raise ValueError("AlgebraicFailure must have non-empty reason")
        if not isinstance(self.reason, str):
            raise TypeError(f"AlgebraicFailure.reason must be str, got {type(self.reason)}")

        # Coerce counter_evidence to tuple if list/sequence provided
        if not isinstance(self.counter_evidence, tuple):
            object.__setattr__(self, "counter_evidence", tuple(self.counter_evidence))

        # Coerce trace to tuple if list/sequence provided
        if not isinstance(self.trace, tuple):
            object.__setattr__(self, "trace", tuple(self.trace))

        # Coerce metadata to MappingProxyType if dict provided
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


# ============================================================================
# Transition Contract
# ============================================================================


@dataclass(frozen=True)
class DalTransitionContract:
    """Contract for a dal transition.

    Specifies source domain, target domain, input/output types,
    claim scope, evidence requirements, and policies.

    Critical: No global certificate. Certificate is claim-scoped.
    """
    contract_id: str
    source_domain: DalTransitionDomain
    target_domain: DalTransitionDomain
    input_type: type               # Expected input type
    output_type: type              # Expected output type
    claim_scope: DalClaimScope     # Scope of certificate

    # Requirements
    evidence_requirement: EvidenceRequirement = EvidenceRequirement.NONE
    lexicon_requirement: bool = False
    context_requirement: bool = False

    # Policies
    shortcut_policy: ShortcutPolicy = ShortcutPolicy.FORBIDDEN
    candidate_budget_policy: CandidateBudgetPolicy = CandidateBudgetPolicy.SMALL
    candidate_budget_limit: Optional[int] = None

    # Forbidden outputs (to prevent semantic leakage)
    forbidden_output_types: Set[type] = field(default_factory=set)

    # Flags
    allows_unresolved: bool = False  # Can transition produce unresolved candidates?
    hypothesis_only: bool = False    # Is this hypothesis-only (not certified)?

    def __post_init__(self):
        """Validate contract invariants."""
        # Source and target must be different (no identity transition)
        if self.source_domain == self.target_domain:
            raise ValueError(
                f"Source and target domain must differ: {self.source_domain}"
            )

        # Custom budget policy must specify limit
        if (self.candidate_budget_policy == CandidateBudgetPolicy.CUSTOM
                and self.candidate_budget_limit is None):
            raise ValueError("CUSTOM budget policy requires candidate_budget_limit")


# ============================================================================
# Protocols (duck-typed interfaces)
# ============================================================================

T = TypeVar('T')


class DalCandidateProtocol(Protocol):
    """Protocol for dal candidate objects.

    Protocols do not force existing classes to inherit.
    They provide duck-typed interfaces.
    """

    @property
    @abstractmethod
    def candidate_id(self) -> str:
        """Unique candidate identifier."""
        ...

    @property
    @abstractmethod
    def domain(self) -> DalTransitionDomain:
        """Domain of this candidate."""
        ...

    @property
    @abstractmethod
    def evidence(self) -> List[DalEvidence]:
        """Supporting evidence."""
        ...

    @property
    @abstractmethod
    def counter_evidence(self) -> List[DalCounterEvidence]:
        """Counter-evidence."""
        ...


class DalCandidateSetProtocol(Protocol, Generic[T]):
    """Protocol for dal candidate sets.

    CandidateSet must be:
    - Bounded (finite candidates)
    - Evidence-bearing
    - Trace-preserving
    - Competitor-preserving
    """

    @property
    @abstractmethod
    def claim_scope(self) -> DalClaimScope:
        """Scope of claim for this candidate set."""
        ...

    @property
    @abstractmethod
    def candidates(self) -> List[T]:
        """List of candidates (must be finite)."""
        ...

    @property
    @abstractmethod
    def evidence(self) -> List[DalEvidence]:
        """Evidence for this candidate set."""
        ...

    @property
    @abstractmethod
    def counter_evidence(self) -> List[DalCounterEvidence]:
        """Counter-evidence."""
        ...

    @property
    @abstractmethod
    def trace(self) -> List[DalTraceRef]:
        """Transformation trace."""
        ...

    def is_empty(self) -> bool:
        """Check if candidate set is empty."""
        return len(self.candidates) == 0

    def size(self) -> int:
        """Number of candidates."""
        return len(self.candidates)


class DalTransitionProtocol(Protocol, Generic[T]):
    """Protocol for dal transitions.

    PR #1C: Hybrid Failure Semantics

    Transition: 𝔾ᵢ × Aux → CandidateSet[𝔾ⱼ] ∪ AlgebraicFailure

    Returns either:
    - CandidateSet[T]: Successful operation with candidates
    - AlgebraicFailure: Operation failed (gate not satisfied, evidence insufficient, etc.)

    Raises Exception ONLY for construction/invariant violations, NOT for operation failures.
    """

    @property
    @abstractmethod
    def contract(self) -> DalTransitionContract:
        """Transition contract."""
        ...

    @abstractmethod
    def apply(self, input_obj: Any, **aux) -> DalCandidateSetProtocol[T] | AlgebraicFailure:
        """Apply transition to input with auxiliary data.

        Args:
            input_obj: Input object (must be valid/constructed)
            **aux: Auxiliary data for transition

        Returns:
            CandidateSet[T] if operation succeeds, AlgebraicFailure if operation fails.

        Raises:
            ValueError: If input_obj has invalid construction/invariants
            TypeError: If input_obj has wrong type

        Note:
            Construction failures raise exceptions.
            Algebraic operation failures return AlgebraicFailure.
        """
        ...


# ============================================================================
# Validation Helpers
# ============================================================================


def validate_transition_contract(contract: DalTransitionContract) -> None:
    """Validate transition contract.

    Raises ValueError if contract is invalid.
    """
    # Already validated in __post_init__, but can add extra checks
    if contract.contract_id == "":
        raise ValueError("Contract ID cannot be empty")

    # Verify no forbidden cross-layer promotions
    _check_no_direct_promotion(contract.source_domain, contract.target_domain,
                               contract.shortcut_policy)


def _check_no_direct_promotion(
    source: DalTransitionDomain,
    target: DalTransitionDomain,
    shortcut_policy: ShortcutPolicy
) -> None:
    """Check that direct cross-layer promotion is not allowed.

    Prohibited promotions without intermediate contract:
    - GRAPHOPHONEMIC → TEMPLATE (رسم/صوت → وزن)
    - SYLLABIC → ORIGIN (مقطع → أصل)
    - Surface pattern → Deep pattern jumps
    - Frozen word → Root extraction (جامد → جذر) without classification
    - Built unit → Morphological pattern (مبني → وزن صرفي)
    """
    forbidden_direct_jumps = [
        (DalTransitionDomain.GRAPHOPHONEMIC, DalTransitionDomain.TEMPLATE),
        (DalTransitionDomain.GRAPHOPHONEMIC, DalTransitionDomain.ORIGIN),
        (DalTransitionDomain.GRAPHOPHONEMIC, DalTransitionDomain.IDENTITY_AXIS),
        (DalTransitionDomain.SYLLABIC, DalTransitionDomain.TEMPLATE),
        (DalTransitionDomain.SYLLABIC, DalTransitionDomain.ORIGIN),
        (DalTransitionDomain.PRE_MORPH, DalTransitionDomain.IDENTITY_AXIS),
    ]

    if (source, target) in forbidden_direct_jumps:
        if shortcut_policy == ShortcutPolicy.FORBIDDEN:
            raise ValueError(
                f"Direct promotion from {source.name} to {target.name} is forbidden "
                f"without intermediate transition or explicit shortcut policy"
            )


def validate_candidate_set_shape(candidate_set: DalCandidateSetProtocol) -> None:
    """Validate candidate set shape.

    Rules:
    1. CandidateSet may be empty only explicitly.
    2. CandidateSet rejects None candidates.
    3. CandidateSet must not be unbounded without budget policy.

    Raises ValueError if validation fails.
    """
    # Rule 2: No None candidates
    if any(c is None for c in candidate_set.candidates):
        raise ValueError("CandidateSet contains None candidates")

    # Can add budget enforcement here if needed
    # For now, rely on contract enforcement at transition level


def ensure_no_forbidden_outputs(
    obj: Any,
    forbidden_outputs: Set[type]
) -> None:
    """Ensure object does not contain forbidden output types.

    This prevents semantic leakage in dal-only layers.
    Forbidden outputs typically include:
    - Meaning types
    - Murad types
    - Hukm types
    - Semantic relation types (before wadh' boundary)

    Raises ValueError if forbidden output detected.
    """
    if not forbidden_outputs:
        return

    obj_type = type(obj)
    if obj_type in forbidden_outputs:
        raise ValueError(
            f"Forbidden output type detected: {obj_type.__name__}"
        )

    # Check if object has forbidden fields
    if hasattr(obj, '__dict__'):
        for field_name, field_value in obj.__dict__.items():
            if field_value is not None:
                field_type = type(field_value)
                if field_type in forbidden_outputs:
                    raise ValueError(
                        f"Forbidden output type in field '{field_name}': "
                        f"{field_type.__name__}"
                    )


def validate_no_direct_promotion(
    source_domain: DalTransitionDomain,
    target_domain: DalTransitionDomain,
    has_trace: bool = False,
    has_shortcut: bool = False,
    has_attestation: bool = False
) -> None:
    """Validate that direct promotion is rejected without trace/shortcut.

    Direct promotion is rejected unless:
    - Intermediate trace exists, or
    - Closed-class lexicon shortcut exists, or
    - Explicit attestation exists.

    Raises ValueError if direct promotion without justification.
    """
    # Define layer distances
    domain_order = [
        DalTransitionDomain.GRAPHOPHONEMIC,
        DalTransitionDomain.SYLLABIC,
        DalTransitionDomain.PRE_MORPH,
        DalTransitionDomain.ORIGIN,
        DalTransitionDomain.TEMPLATE,
        DalTransitionDomain.IDENTITY_AXIS,
        DalTransitionDomain.DIRECTIONAL_ANALYSIS,
        DalTransitionDomain.JUDGMENT,
    ]

    try:
        source_idx = domain_order.index(source_domain)
        target_idx = domain_order.index(target_domain)
    except ValueError:
        # Unknown domain, skip validation
        return

    # Direct promotion (skipping layers) requires justification
    layer_skip = abs(target_idx - source_idx)

    if layer_skip > 1:
        # This is a direct promotion (skipping layers)
        if not (has_trace or has_shortcut or has_attestation):
            raise ValueError(
                f"Direct promotion from {source_domain.name} to {target_domain.name} "
                f"(skipping {layer_skip - 1} layers) requires trace, shortcut, or attestation"
            )


# ============================================================================
# Mufrad-axes specific prohibition (PR-G / §5.1 of the mufrad-axes plan)
# ============================================================================
#
# The plan explicitly bans deriving the BINAA/I'RAB judgment from the
# SYLLABIC layer. Syllable count is descriptive (D1); BINAA is judicial
# (D5/D7). NO amount of trace or shortcut justifies this promotion —
# it is forbidden by construction.

FORBIDDEN_AXIS_PROMOTIONS: frozenset[tuple[str, str]] = frozenset({
    # (source_domain.name, target_axis_name)
    ("SYLLABIC", "BINAA_JUDGMENT"),
    ("SYLLABIC", "ISHTIQAQ_JUDGMENT"),
})
"""Promotions that are forbidden regardless of trace/shortcut/attestation.

Each entry is ``(source_domain, target_axis_name)``. ``target_axis_name``
is the *judicial* axis (not a domain), and corresponds to the axes
defined in ``dal_core.mufrad_axes``. These are categorical bans, not
heuristic warnings: any code path proposing such a promotion is broken
by definition and must be rewritten.
"""


def assert_axis_promotion_allowed(
    source_domain: DalTransitionDomain, target_axis_name: str
) -> None:
    """Hard-fail if a forbidden axis promotion is attempted.

    Use this from any code that derives a mufrad axis judgment from a
    lower domain. The function raises ``ValueError`` immediately for
    any pair listed in :data:`FORBIDDEN_AXIS_PROMOTIONS`.

    This is the runtime counterpart to :func:`validate_no_direct_promotion`
    — but unlike that function, no escape hatches exist. The plan §5.1
    requires: "عدد المقاطع لا يحكم بالبناء/الإعراب".
    """
    pair = (source_domain.name, target_axis_name)
    if pair in FORBIDDEN_AXIS_PROMOTIONS:
        raise ValueError(
            f"Forbidden axis promotion: {source_domain.name} → "
            f"{target_axis_name}. "
            f"Per the mufrad-axes plan §5.1, syllable count is "
            f"descriptive and may not drive judicial axes. See "
            f"docs/MUFRAD_AXES.md and dal_core.mufrad_axes."
        )


# ============================================================================
# Module exports
# ============================================================================

__all__ = [
    # Enums
    "DalTransitionDomain",
    "DalClaimScope",
    "EvidenceRequirement",
    "ShortcutPolicy",
    "CandidateBudgetPolicy",
    # Evidence and trace
    "DalEvidence",
    "DalCounterEvidence",
    "DalTraceRef",
    # Algebraic Failure (PR-1C)
    "AlgebraicFailure",
    # Contracts and protocols
    "DalTransitionContract",
    "DalCandidateProtocol",
    "DalCandidateSetProtocol",
    "DalTransitionProtocol",
    # Validation
    "validate_transition_contract",
    "validate_candidate_set_shape",
    "ensure_no_forbidden_outputs",
    "validate_no_direct_promotion",
    "FORBIDDEN_AXIS_PROMOTIONS",
    "assert_axis_promotion_allowed",
]
