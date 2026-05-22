"""Origin: Extract invariant patterns from positive examples.

Core Principle:
    الأصل هو المثال الموجب الذي نستخرج منه القاعدة.
    "The origin is the positive example from which we extract the rule."

Central Law:
    لا قاعدة بلا أصل.
    "No rule without origin."

Architecture:
    An **Origin** is a positive example that:
    1. Exhibits a pattern we want to generalize
    2. Is verified (in lexicon/corpus) or attested
    3. Carries evidence of the pattern
    4. May have residuals (e.g., ambiguity, context-dependence)

    An **OriginSet** is a collection of origins that:
    1. Share a common invariant pattern
    2. Are sufficient in number (≥3 recommended)
    3. Are non-conflicting (or conflicts are explained)
    4. Form the basis for rule extraction

Example (فاعل Pattern):
    Origins:
        كاتب (writer) → exhibits agentive reading
        زارع (farmer) → exhibits agentive reading
        عامل (worker) → exhibits agentive reading

    Invariant extracted:
        Pattern: فاعل (fa'il)
        Feature: Agentive interpretation
        Evidence: All three examples show agent of action

    Rule candidate:
        "وزن فاعل يرشح علاقة فاعلية"
        "فاعل pattern licenses agentive relation"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, Mapping, Any

from fvafk.algebra import Evidence, Residual, Rank, Trace


# ===========================================================================
# Origin
# ===========================================================================


@dataclass(frozen=True)
class Origin:
    """A positive example from which a rule is extracted.

    An origin is NOT just a surface form; it is a **governed example**
    that carries evidence, residuals, and rank just like any Result.

    Attributes:
        surface: The surface form (e.g., "كاتب").
        pattern: The morphological pattern (e.g., "فاعل").
        root: The root letters (e.g., ("ك", "ت", "ب")).
        interpretation: The semantic interpretation observed (e.g., "agentive").
        evidence: Supporting evidence for this interpretation.
        residuals: Unresolved aspects (e.g., context-dependent).
        rank: Epistemic rank of this origin (LICENSED, CERTIFIED, etc.).
        metadata: Additional contextual information.

    Example:
        >>> origin = Origin(
        ...     surface="كاتب",
        ...     pattern="فاعل",
        ...     root=("ك", "ت", "ب"),
        ...     interpretation="agentive",
        ...     evidence=(Evidence(kind="lexicon.attested", source="Wehr", detail="writer"),),
        ...     rank=Rank.LICENSED,
        ... )
        >>> origin.surface
        'كاتب'
        >>> origin.pattern
        'فاعل'
    """

    surface: str
    pattern: str
    root: Tuple[str, ...] | None = None
    interpretation: str = ""
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    rank: Rank = Rank.CANDIDATE
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.surface:
            raise ValueError("Origin.surface must be non-empty")
        if not self.pattern:
            raise ValueError("Origin.pattern must be non-empty")

    @property
    def is_verified(self) -> bool:
        """Check if origin is verified (has evidence with LICENSED+ rank)."""
        return self.rank in (Rank.LICENSED, Rank.CERTIFIED) and bool(self.evidence)

    @property
    def has_conflicts(self) -> bool:
        """Check if origin has conflicting interpretations (multiple residuals)."""
        return len(self.residuals) > 1

    def to_trace(self) -> Trace:
        """Convert origin to a Trace for provenance tracking."""
        return Trace(
            operation=f"origin_extraction:{self.surface}",
            source_span=(0, len(self.surface)),
            metadata={
                "pattern": self.pattern,
                "root": self.root,
                "interpretation": self.interpretation,
                "rank": self.rank.name,
            },
        )


# ===========================================================================
# OriginSet
# ===========================================================================


@dataclass(frozen=True)
class OriginSet:
    """A collection of origins that share a common pattern.

    An OriginSet is the foundation for rule extraction. It must:
    1. Contain sufficient examples (≥3 recommended)
    2. Share a common invariant pattern
    3. Have evidence supporting the pattern
    4. Track any conflicts or residuals

    Attributes:
        origins: The positive examples.
        shared_pattern: The pattern common to all origins (e.g., "فاعل").
        shared_feature: The feature/interpretation shared (e.g., "agentive").
        evidence: Evidence supporting the shared pattern.
        residuals: Unresolved aspects across the set.
        rank: Epistemic rank of the origin set.

    Example:
        >>> origin1 = Origin(surface="كاتب", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin2 = Origin(surface="زارع", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin3 = Origin(surface="عامل", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin_set = OriginSet(
        ...     origins=(origin1, origin2, origin3),
        ...     shared_pattern="فاعل",
        ...     shared_feature="agentive",
        ...     rank=Rank.LICENSED,
        ... )
        >>> len(origin_set.origins)
        3
        >>> origin_set.shared_pattern
        'فاعل'
    """

    origins: Tuple[Origin, ...]
    shared_pattern: str = ""
    shared_feature: str = ""
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    rank: Rank = Rank.CANDIDATE

    def __post_init__(self) -> None:
        if not self.origins:
            raise ValueError("OriginSet.origins must be non-empty")
        if len(self.origins) < 2:
            raise ValueError("OriginSet requires at least 2 origins")

    @property
    def is_sufficient(self) -> bool:
        """Check if origin set has sufficient examples (≥3)."""
        return len(self.origins) >= 3

    @property
    def is_consistent(self) -> bool:
        """Check if all origins share the same pattern and interpretation."""
        if not self.origins:
            return False
        patterns = {o.pattern for o in self.origins}
        interpretations = {o.interpretation for o in self.origins}
        return len(patterns) == 1 and len(interpretations) == 1

    @property
    def is_verified(self) -> bool:
        """Check if all origins are verified."""
        return all(o.is_verified for o in self.origins)

    @property
    def min_rank(self) -> Rank:
        """Get minimum rank across all origins."""
        if not self.origins:
            return Rank.UNRESOLVED
        return min(o.rank for o in self.origins)

    def to_trace(self) -> Trace:
        """Convert origin set to a Trace for provenance tracking."""
        return Trace(
            operation="origin_set_construction",
            source_span=(0, len(self.origins)),
            parents=tuple(o.to_trace().trace_id for o in self.origins),
            metadata={
                "shared_pattern": self.shared_pattern,
                "shared_feature": self.shared_feature,
                "count": len(self.origins),
                "rank": self.rank.name,
            },
        )


# ===========================================================================
# Origin Extraction
# ===========================================================================


def extract_origin(
    surface: str,
    pattern: str,
    root: Tuple[str, ...] | None = None,
    interpretation: str = "",
    evidence: Tuple[Evidence, ...] = (),
    residuals: Tuple[Residual, ...] = (),
    rank: Rank = Rank.CANDIDATE,
) -> Origin:
    """Extract an origin from a positive example.

    This is a convenience constructor that validates the inputs and
    creates an Origin with proper defaults.

    Args:
        surface: Surface form (e.g., "كاتب").
        pattern: Morphological pattern (e.g., "فاعل").
        root: Root letters (optional).
        interpretation: Semantic interpretation (e.g., "agentive").
        evidence: Supporting evidence.
        residuals: Unresolved aspects.
        rank: Epistemic rank.

    Returns:
        Origin instance.

    Raises:
        ValueError: If surface or pattern is empty.

    Example:
        >>> origin = extract_origin(
        ...     surface="كاتب",
        ...     pattern="فاعل",
        ...     root=("ك", "ت", "ب"),
        ...     interpretation="agentive",
        ...     rank=Rank.LICENSED,
        ... )
        >>> origin.surface
        'كاتب'
    """
    return Origin(
        surface=surface,
        pattern=pattern,
        root=root,
        interpretation=interpretation,
        evidence=evidence,
        residuals=residuals,
        rank=rank,
    )


def make_origin_set(
    origins: Tuple[Origin, ...],
    shared_pattern: str = "",
    shared_feature: str = "",
    evidence: Tuple[Evidence, ...] = (),
    residuals: Tuple[Residual, ...] = (),
) -> OriginSet:
    """Create an OriginSet from a collection of origins.

    This function:
    1. Validates that all origins share the same pattern
    2. Extracts the shared pattern/feature if not provided
    3. Determines the rank based on minimum origin rank
    4. Validates consistency

    Args:
        origins: Collection of Origin instances.
        shared_pattern: The shared pattern (auto-detected if empty).
        shared_feature: The shared feature (auto-detected if empty).
        evidence: Additional evidence for the set.
        residuals: Residuals at the set level.

    Returns:
        OriginSet instance.

    Raises:
        ValueError: If origins is empty or inconsistent.

    Example:
        >>> origin1 = Origin(surface="كاتب", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin2 = Origin(surface="زارع", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin_set = make_origin_set(origins=(origin1, origin2))
        >>> origin_set.shared_pattern
        'فاعل'
    """
    if not origins:
        raise ValueError("origins must be non-empty")

    # Auto-detect shared pattern if not provided
    if not shared_pattern:
        patterns = {o.pattern for o in origins}
        if len(patterns) == 1:
            shared_pattern = next(iter(patterns))
        else:
            raise ValueError(f"Origins have inconsistent patterns: {patterns}")

    # Auto-detect shared feature if not provided
    if not shared_feature:
        interpretations = {o.interpretation for o in origins if o.interpretation}
        if len(interpretations) == 1:
            shared_feature = next(iter(interpretations))

    # Determine rank: minimum rank across origins
    ranks = [o.rank for o in origins]
    set_rank = min(ranks) if ranks else Rank.CANDIDATE

    return OriginSet(
        origins=origins,
        shared_pattern=shared_pattern,
        shared_feature=shared_feature,
        evidence=evidence,
        residuals=residuals,
        rank=set_rank,
    )


__all__ = [
    "Origin",
    "OriginSet",
    "extract_origin",
    "make_origin_set",
]
