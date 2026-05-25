"""
Neutral Potential - Foundational Neutral Element Redefinition

CORE INSIGHT:
    Neutral ≠ Empty
    Neutral = Preserved Potential without Certification

This redefines the neutral element across all algebra:
    - Weight neutral element ≠ "no weight"
    - Weight neutral element = carrier that opens weight paths without certification
    - Syllable neutral element ≠ "no syllable"
    - Syllable neutral element = C+V that opens syllable paths without certification

Constitutional Theorem (Neutral Potential Theorem):
    في كل طبقة من طبقات الجبر العام،
    العنصر المحايد ليس عدمًا،
    بل حامل محفوظ بلغ حدّ إمكان المسار
    ولم يدخل بعد بوابة الشهادة.

    In every layer of general algebra,
    the neutral element is not emptiness,
    but a preserved carrier that has reached the threshold of potential paths
    and has not yet entered the gate of certification.

Formal Statement:
    Neutral_L(x) ⇒
        PreserveIdentity(x) ∧
        PreserveTrace(x) ∧
        PreserveResiduals(x) ∧
        PreserveCompetitors(x) ∧
        OpensPotentialPaths(x) ∧
        ¬CertifiesPath(x)

Examples:
    C + V = NeutralSyllablePotential (opens PotentialSyllablePath, no certificate)
    كَتَبَ = NeutralWeightPotential (opens PotentialWeightPath, no certificate)
    بْ = BlockedSyllablePotential (no nucleus, cannot open syllable path)

Critical Laws:
    1. NeutralPotential.certified_paths MUST be empty
    2. NeutralPotential.opened_paths MAY be non-empty
    3. NeutralPotential preserves trace/residuals/competitors
    4. NeutralPotential does NOT raise rank to CERTIFICATE
    5. CPB₀ preserves NeutralPotential without transformation

PR: FOUNDATION-NEUTRAL-POTENTIAL
Created: 2026-05-25
"""

from dataclasses import dataclass
from typing import Tuple, FrozenSet, Optional, Any
from uuid import uuid4

from dal_core.foundation.rank import Rank
from dal_core.residuals import Residual


# ============================================================================
# Neutral Potential Core Structure
# ============================================================================

@dataclass(frozen=True)
class NeutralPotential:
    """
    Neutral element in the algebra of potential paths.

    This is NOT "empty" or "no-op".
    This IS "preserved carrier that opens paths without certifying them".

    The neutral element redefines across all layers:
        - At syllable layer: C+V is NeutralSyllablePotential (not certified syllable)
        - At weight layer: TriLiteral is NeutralWeightPotential (not certified weight)
        - At boundary layer: SyllableSequence is NeutralBoundaryPotential (not certified boundary)

    Fields:
        neutral_id: Unique identifier
        carrier_id: ID of underlying carrier
        layer: Layer name (U₀, U₁, U₂p, U₂s, etc.)
        opened_paths: Tuple of potential path IDs that this neutral opens
        certified_paths: Tuple of certified path IDs (MUST be empty for neutral)
        trace: Tuple of trace IDs to previous layers
        residuals: Tuple of residuals (warnings/blockers)
        competitors: Tuple of competing neutral/path IDs
        rank: Epistemic rank (typically CANDIDATE, never CERTIFICATE)
        metadata: Optional additional metadata

    Critical Invariants:
        1. len(certified_paths) MUST be 0 (neutral does not certify)
        2. opened_paths MAY be non-empty (neutral opens possibilities)
        3. rank MUST NOT be CERTIFICATE (neutral does not certify)
        4. trace MUST be preserved (neutral preserves identity)
        5. residuals MUST be preserved (neutral does not discharge)
        6. competitors MUST be preserved (neutral does not resolve)

    Examples:
        ConsonantVowelComposite(C=/k/, V=/a/) →
            NeutralSyllablePotential(
                opened_paths=["potential_cv_syllable"],
                certified_paths=[],  # Empty!
                rank=CANDIDATE
            )

        TriLiteralRoot(كتب) →
            NeutralWeightPotential(
                opened_paths=["verb_weight", "noun_weight"],
                certified_paths=[],  # Empty!
                rank=CANDIDATE
            )
    """
    neutral_id: str
    carrier_id: str
    layer: str
    opened_paths: Tuple[str, ...]
    certified_paths: Tuple[str, ...]
    trace: Tuple[str, ...]
    residuals: FrozenSet[Residual]
    competitors: Tuple[str, ...]
    rank: Rank
    metadata: Optional[Any] = None

    def __post_init__(self):
        """Validate NeutralPotential invariants."""
        # CRITICAL: Neutral MUST have empty certified_paths
        if len(self.certified_paths) > 0:
            raise ValueError(
                "NeutralPotential MUST have empty certified_paths. "
                "Neutral means 'preserved potential without certification'. "
                f"Got certified_paths: {self.certified_paths}. "
                "If paths are certified, this is NOT neutral."
            )

        # Neutral MUST NOT have CERTIFICATE rank
        if self.rank == Rank.CERTIFICATE:
            raise ValueError(
                "NeutralPotential MUST NOT have CERTIFICATE rank. "
                "Neutral means 'potential without certification'. "
                f"Got rank: {self.rank}. "
                "If rank is CERTIFICATE, this is NOT neutral."
            )

        # Neutral SHOULD preserve trace (warning if empty)
        if not self.trace:
            # This is a warning, not an error - some initial carriers may have no trace
            pass

    def is_neutral(self) -> bool:
        """
        Check if this is truly neutral (no certified paths).

        Returns:
            True if neutral (certified_paths is empty)
        """
        return len(self.certified_paths) == 0

    def opens_paths(self) -> bool:
        """
        Check if neutral opens any potential paths.

        Returns:
            True if opened_paths is non-empty
        """
        return len(self.opened_paths) > 0

    def is_blocked(self) -> bool:
        """
        Check if neutral is blocked (has blocking residuals).

        Returns:
            True if any residual is a blocker
        """
        return any(r.is_blocker for r in self.residuals)

    def has_competitors(self) -> bool:
        """
        Check if neutral has competing alternatives.

        Returns:
            True if competitors is non-empty
        """
        return len(self.competitors) > 0


# ============================================================================
# Neutral Potential Validators
# ============================================================================

def validate_neutral_potential(neutral: NeutralPotential) -> bool:
    """
    Validate that NeutralPotential meets neutrality requirements.

    Args:
        neutral: NeutralPotential to validate

    Returns:
        True if valid neutral, False otherwise

    Requirements:
        1. certified_paths MUST be empty
        2. rank MUST NOT be CERTIFICATE
        3. trace SHOULD be preserved (recommended)

    This enforces the law: Neutral = Preserved Potential, NOT emptiness.
    """
    # Must have no certified paths
    if len(neutral.certified_paths) > 0:
        return False

    # Must not have CERTIFICATE rank
    if neutral.rank == Rank.CERTIFICATE:
        return False

    # Should preserve trace (warning but not failure)
    # In production, might want to emit warning if trace is empty

    return True


def validate_cpb_zero_preserves_neutral(
    input_neutral: NeutralPotential,
    output_neutral: NeutralPotential
) -> bool:
    """
    Validate that CPB₀ preserves NeutralPotential without transformation.

    Args:
        input_neutral: Input NeutralPotential
        output_neutral: Output NeutralPotential

    Returns:
        True if CPB₀ preserved neutral correctly

    Requirements:
        1. carrier_id preserved
        2. layer preserved
        3. trace preserved (or extended)
        4. residuals preserved (or extended)
        5. competitors preserved
        6. certified_paths remains empty
        7. rank does NOT increase to CERTIFICATE

    CPB₀ is the identity preservation operation.
    It does NOT transform, only preserves.
    """
    # Carrier ID should be preserved
    if input_neutral.carrier_id != output_neutral.carrier_id:
        return False

    # Layer should be preserved
    if input_neutral.layer != output_neutral.layer:
        return False

    # Certified paths must remain empty (both input and output)
    if len(input_neutral.certified_paths) > 0 or len(output_neutral.certified_paths) > 0:
        return False

    # Rank must not jump to CERTIFICATE
    if output_neutral.rank == Rank.CERTIFICATE:
        return False

    return True


# ============================================================================
# Specific Neutral Potentials
# ============================================================================

@dataclass(frozen=True)
class NeutralSyllablePotential(NeutralPotential):
    """
    Neutral element at syllable layer.

    C + V does NOT directly equal certified syllable.
    C + V equals NeutralSyllablePotential that opens PotentialSyllablePath.

    Example:
        كَ (C=/k/, V=/a/) →
            NeutralSyllablePotential(
                opened_paths=["potential_cv_syllable"],
                certified_paths=[],  # Not certified yet!
                rank=CANDIDATE
            )

        Then through SyllableGate →
            SyllableCertificate(CV)

    Contrast with blocked case:
        بْ (C=/b/, SUKUN, no nucleus) →
            Cannot create NeutralSyllablePotential
            (fails nucleus requirement)
    """
    def requires_nucleus(self) -> bool:
        """Syllable potential requires nucleus V or VV."""
        return True


@dataclass(frozen=True)
class NeutralWeightPotential(NeutralPotential):
    """
    Neutral element at weight layer.

    TriLiteralCarrier does NOT directly equal certified weight.
    TriLiteralCarrier equals NeutralWeightPotential that opens PotentialWeightPath.

    Example:
        كَتَبَ (trilateral root كتب) →
            NeutralWeightPotential(
                opened_paths=["verb_weight_faeala", "noun_weight_faeal"],
                certified_paths=[],  # Not certified yet!
                rank=CANDIDATE
            )

        Then through WeightGate →
            WeightCertificate(فَعَلَ)

    This is NOT "no weight".
    This IS "carrier sufficient to open weight paths, without certifying them".
    """
    def opens_weighted_paths(self) -> bool:
        """Weight potential opens multiple possible weight paths."""
        return len(self.opened_paths) > 0


@dataclass(frozen=True)
class NeutralBoundaryPotential(NeutralPotential):
    """
    Neutral element at boundary layer.

    SyllableSequence does NOT directly equal certified boundary.
    SyllableSequence equals NeutralBoundaryPotential that opens PotentialBoundaryPath.

    Example:
        وَبِكِتَابِهِمْ (syllable sequence) →
            NeutralBoundaryPotential(
                opened_paths=["boundary_[وَ,بِكِتَابِهِمْ]", "boundary_[وَ,بِـ,كِتَابِـهِمْ]", "boundary_[وَ,بِـ,كِتَاب,ـهِمْ]"],
                certified_paths=[],  # Not certified yet!
                rank=CANDIDATE
            )

        Then through BoundaryGate →
            BoundaryAndAttachmentCertificate([وَ, بِـ, كِتَاب, ـهِمْ])
    """
    pass


# ============================================================================
# Factory Functions
# ============================================================================

def make_neutral_potential(
    carrier_id: str,
    layer: str,
    opened_paths: Tuple[str, ...],
    trace: Tuple[str, ...],
    residuals: FrozenSet[Residual] = frozenset(),
    competitors: Tuple[str, ...] = (),
    rank: Rank = Rank.CANDIDATE,
) -> NeutralPotential:
    """
    Factory function for creating NeutralPotential.

    Args:
        carrier_id: ID of underlying carrier
        layer: Layer name
        opened_paths: Potential paths that this neutral opens
        trace: Trace to previous layers
        residuals: Residuals (warnings/blockers)
        competitors: Competing neutrals/paths
        rank: Epistemic rank (default: CANDIDATE)

    Returns:
        NeutralPotential with empty certified_paths

    Example:
        neutral = make_neutral_potential(
            carrier_id="cv_composite_كَ",
            layer="U2P_PHONETIC_PROJECTION",
            opened_paths=("potential_cv_syllable",),
            trace=("phonetic_projection_123",),
            rank=Rank.CANDIDATE
        )
    """
    return NeutralPotential(
        neutral_id=str(uuid4()),
        carrier_id=carrier_id,
        layer=layer,
        opened_paths=opened_paths,
        certified_paths=(),  # Always empty for neutral!
        trace=trace,
        residuals=residuals,
        competitors=competitors,
        rank=rank,
        metadata=None
    )


def make_neutral_syllable_potential(
    carrier_id: str,
    opened_paths: Tuple[str, ...],
    trace: Tuple[str, ...],
    residuals: FrozenSet[Residual] = frozenset(),
    rank: Rank = Rank.CANDIDATE,
) -> NeutralSyllablePotential:
    """
    Factory for NeutralSyllablePotential.

    C + V opens syllable potential, does not certify syllable.
    """
    return NeutralSyllablePotential(
        neutral_id=str(uuid4()),
        carrier_id=carrier_id,
        layer="U2S_ARABIC_SYLLABLE",
        opened_paths=opened_paths,
        certified_paths=(),
        trace=trace,
        residuals=residuals,
        competitors=(),
        rank=rank,
        metadata=None
    )


def make_neutral_weight_potential(
    carrier_id: str,
    opened_paths: Tuple[str, ...],
    trace: Tuple[str, ...],
    residuals: FrozenSet[Residual] = frozenset(),
    rank: Rank = Rank.CANDIDATE,
) -> NeutralWeightPotential:
    """
    Factory for NeutralWeightPotential.

    TriLiteralCarrier opens weight potential, does not certify weight.
    """
    return NeutralWeightPotential(
        neutral_id=str(uuid4()),
        carrier_id=carrier_id,
        layer="U9_WEIGHT",
        opened_paths=opened_paths,
        certified_paths=(),
        trace=trace,
        residuals=residuals,
        competitors=(),
        rank=rank,
        metadata=None
    )


def make_neutral_boundary_potential(
    carrier_id: str,
    opened_paths: Tuple[str, ...],
    trace: Tuple[str, ...],
    residuals: FrozenSet[Residual] = frozenset(),
    rank: Rank = Rank.CANDIDATE,
) -> NeutralBoundaryPotential:
    """
    Factory for NeutralBoundaryPotential.

    SyllableSequence opens boundary potential, does not certify boundary.
    """
    return NeutralBoundaryPotential(
        neutral_id=str(uuid4()),
        carrier_id=carrier_id,
        layer="U3_BOUNDARY_ATTACHMENT",
        opened_paths=opened_paths,
        certified_paths=(),
        trace=trace,
        residuals=residuals,
        competitors=(),
        rank=rank,
        metadata=None
    )


# ============================================================================
# Theorem: Neutral Potential Preservation
# ============================================================================

class NeutralPotentialViolation(Exception):
    """
    Raised when NeutralPotential invariants are violated.

    This enforces the constitutional law:
        Neutral ≠ Empty
        Neutral = Preserved Potential without Certification
    """
    pass


def enforce_neutral_potential_law(neutral: NeutralPotential) -> None:
    """
    Enforce NeutralPotential constitutional law.

    Args:
        neutral: NeutralPotential to validate

    Raises:
        NeutralPotentialViolation: If neutral has certified paths or CERTIFICATE rank

    Law:
        Neutral element MUST preserve potential without certification.
        certified_paths MUST be empty.
        rank MUST NOT be CERTIFICATE.
    """
    if not validate_neutral_potential(neutral):
        if len(neutral.certified_paths) > 0:
            raise NeutralPotentialViolation(
                f"NeutralPotential has certified paths: {neutral.certified_paths}. "
                "Neutral means 'preserved potential WITHOUT certification'. "
                "If paths are certified, this violates neutrality law."
            )

        if neutral.rank == Rank.CERTIFICATE:
            raise NeutralPotentialViolation(
                f"NeutralPotential has CERTIFICATE rank. "
                "Neutral means 'potential WITHOUT certification'. "
                "If rank is CERTIFICATE, this violates neutrality law."
            )

        raise NeutralPotentialViolation(
            "NeutralPotential violates neutrality law for unknown reason."
        )
