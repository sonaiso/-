"""
Relation Algebra Core (نواة جبر العلاقات)

Constitutional Foundation:
    This module defines the algebraic foundation for composition.
    It is NOT an execution layer.
    It is the specification that composition layers MUST obey.

Critical Law:
    لا U₁₁ قبل RelationAlgebraCore.
    No U₁₁ before RelationAlgebraCore.

Purpose:
    Define relations as ALGEBRAIC OPERATIONS not labels.
    Each relation preserves identity while adding load/restriction/containment.

Forbidden Outputs from Relations:
    ❌ SEMANTIC_IDENTITY
    ❌ IFADAH_IDENTITY
    ❌ HUKM_IDENTITY
    ❌ FUNCTIONAL_RELATION_IDENTITY (final role)

Permitted Outputs:
    ✅ RelationCandidate with preserved identities
    ✅ Residuals for unresolved aspects
    ✅ Rank.CANDIDATE (never CERTIFIED)

Architecture Position:
    AlgebraicDecisionCore
        └── RelationAlgebraCore (this module)
              ├── Identity Carriers (Entity, Transformation, Function)
              ├── Relation Invariants
              └── Relation Operations (ISNAD, TADMIN, TAQYID, WASF, IDAFAH)

Reference:
    docs/APPENDIX_0_PRE_RELATION_ALGEBRA.md

PR: RELATION-ALGEBRA-CORE
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, FrozenSet, Optional, Protocol
from abc import ABC, abstractmethod

from dal_core.identity_registry import IdentityType
from dal_core.foundation import Rank, ResidualSet


# ============================================================================
# Supporting Type Definitions
# ============================================================================

class RelationType(Enum):
    """
    Five core relation types.

    CRITICAL: These are NOT standalone labels.
    Each must have a corresponding RelationOperation implementation.
    """
    ISNAD = auto()      # الإسناد - Predication
    TADMIN = auto()     # التضمين - Embedding/Containment
    TAQYID = auto()     # التقييد - Restriction/Modification
    WASF = auto()       # الوصف - Description/Attribution
    IDAFAH = auto()     # الإضافة - Attachment/Possession


class OnticType(Enum):
    """Ontic classification (what kind of being)."""
    SUBSTANCE = auto()  # جوهر (independent existence)
    ACCIDENT = auto()   # عرض (dependent existence)


class GenusType(Enum):
    """Genus vs individual."""
    GENUS = auto()      # كلي (universal)
    INDIVIDUAL = auto() # جزئي (particular)


class ReferenceStatus(Enum):
    """Reference determination status."""
    DEFINITE = auto()       # معرفة
    INDEFINITE = auto()     # نكرة
    UNRESOLVED = auto()     # غير محسوم


class StabilityType(Enum):
    """Entity stability."""
    STABLE = auto()         # ثابت
    TRANSIENT = auto()      # عارض
    UNRESOLVED = auto()     # غير محسوم


class TransformationType(Enum):
    """Transformation classification."""
    EVENT = auto()          # حدث
    ATTRIBUTE = auto()      # صفة
    STATE = auto()          # حال


class ScopeType(Enum):
    """Function word scope."""
    LOCAL = auto()          # محلي
    CLAUSE = auto()         # جملي
    SENTENCE = auto()       # نصي


# ============================================================================
# A. Identity Carriers (المحفوظات)
# ============================================================================

@dataclass(frozen=True)
class EntityAnchor:
    """
    Stable entity anchor (الجامد - jāmid)

    Constitutional Law:
        Entity identity MUST be preserved through composition.
        Relations add load but NEVER replace entity identity.

    Represents:
        الجامد - Stable entities that can bear transformations

    Attributes:
        identity: IdentityType from IdentityRegistry
        ontic_type: جوهر (substance) or عرض (accident)
        genus_or_individual: كلي (genus) or جزئي (individual)
        reference_status: معرفة/نكرة or unresolved
        preserved_invariant: What must NOT change
        stability: ثابت (stable) or عارض (transient)
        verified_bearability: Can this entity bear predication?
        trace: Origin trace from U₀→U₁₀
    """
    identity: IdentityType
    ontic_type: OnticType
    genus_or_individual: GenusType
    reference_status: ReferenceStatus
    preserved_invariant: str
    stability: StabilityType
    verified_bearability: bool
    trace: Tuple[str, ...]


@dataclass(frozen=True)
class TransformationAnchor:
    """
    Transformation anchor (المشتق - mushtaq)

    Constitutional Law:
        Transformation MUST trace back to root/pattern from U₈/U₉.
        No transformations without morphological evidence.

    Represents:
        المشتق - Derived forms with event/attribute semantics

    Attributes:
        identity: IdentityType from IdentityRegistry
        origin_root_id: str from U₈ RootStemCandidate
        pattern_id: str from U₉ WeightCandidate
        event_or_attribute: حدث (event) or صفة (attribute) or حال (state)
        bearability_requirements: What entities can bear this?
        valency_requirements: Argument structure if event
        trace: Origin trace from U₀→U₁₀
    """
    identity: IdentityType
    origin_root_id: str  # from U₈
    pattern_id: str  # from U₉
    event_or_attribute: TransformationType
    bearability_requirements: FrozenSet[str]
    valency_requirements: Optional[str]  # Simplified for now
    trace: Tuple[str, ...]


@dataclass(frozen=True)
class FunctionAnchor:
    """
    Function anchor (المبني - mabnī)

    Constitutional Law:
        Function words are locked (مبني).
        They require scope/anchor/join specifications.

    Represents:
        المبني - Frozen function words with scope requirements

    Attributes:
        identity: IdentityType (CLOSED_CLASS_IDENTITY)
        locked_form: str (frozen surface)
        scope_type: محلي/جملي/نصي (local/clause/sentence)
        attachment_requirements: What it must attach to
        trace: Origin trace from U₀→U₁₀
    """
    identity: IdentityType
    locked_form: str
    scope_type: ScopeType
    attachment_requirements: FrozenSet[str]
    trace: Tuple[str, ...]


# Union type for all anchors
Anchor = EntityAnchor | TransformationAnchor | FunctionAnchor


# ============================================================================
# B. Relation Invariants (ثوابت العلاقة)
# ============================================================================

@dataclass(frozen=True)
class RelationIdentityInvariant:
    """
    What a relation operation MUST preserve and what it MAY change.

    Constitutional Law:
        Every relation MUST declare:
        1. Input identities (preserved)
        2. Output identities (preserved or extended)
        3. Invariants (what cannot change)
        4. Permitted shifts (what may change under license)
        5. Blocked collapses (forbidden identity mergers)
        6. Residuals (unresolved aspects)

    Attributes:
        relation_type: ISNAD, TADMIN, TAQYID, WASF, or IDAFAH
        input_identities: Tuple of input identity types
        output_identities: Tuple of output identity types (must include inputs)
        preserved_invariants: What CANNOT change
        permitted_shifts: What MAY change under license
        blocked_collapses: Forbidden identity absorptions
        residuals: Unresolved aspects requiring evidence
        rank: Rank (CANDIDATE not CERTIFIED)
        evidence: Evidence trace
    """
    relation_type: RelationType
    input_identities: Tuple[IdentityType, ...]
    output_identities: Tuple[IdentityType, ...]
    preserved_invariants: FrozenSet[str]
    permitted_shifts: FrozenSet[str]
    blocked_collapses: FrozenSet[Tuple[IdentityType, IdentityType]]
    residuals: ResidualSet
    rank: Rank
    evidence: Tuple[str, ...]

    def __post_init__(self):
        """Validate invariant consistency."""
        # All input identities must be in output identities
        for input_id in self.input_identities:
            if input_id not in self.output_identities:
                raise ValueError(
                    f"Identity collapse detected: {input_id} not in outputs. "
                    f"Relations must preserve input identities."
                )


# ============================================================================
# C. Relation Result
# ============================================================================

@dataclass(frozen=True)
class RelationResult:
    """
    Result of applying a relation operation.

    Constitutional Law:
        Result MUST preserve input identities.
        Result MUST NOT emit forbidden outputs.

    Forbidden Outputs:
        ❌ SEMANTIC_IDENTITY
        ❌ IFADAH_IDENTITY
        ❌ HUKM_IDENTITY
        ❌ FUNCTIONAL_RELATION_IDENTITY (final role)

    Attributes:
        preserved_identities: Input identities (must all be present)
        added_loads: What was added (predication/restriction/etc.)
        residuals: Unresolved aspects
        rank: Always CANDIDATE
        evidence: Evidence trace
    """
    preserved_identities: FrozenSet[IdentityType]
    added_loads: FrozenSet[str]
    residuals: ResidualSet
    rank: Rank
    evidence: Tuple[str, ...]

    def __post_init__(self):
        """Validate result does not violate constitutional law."""
        # Must be CANDIDATE
        if self.rank != Rank.CANDIDATE:
            raise ValueError(
                f"Relations can only produce CANDIDATE rank, got {self.rank}"
            )

        # Check for forbidden outputs
        forbidden = {
            IdentityType.SEMANTIC_IDENTITY,
            IdentityType.HUKM_IDENTITY,
        }
        # Note: FUNCTIONAL_RELATION_IDENTITY might exist in registry
        # Check if attribute exists before adding
        if hasattr(IdentityType, 'IFADAH_IDENTITY'):
            forbidden.add(IdentityType.IFADAH_IDENTITY)
        if hasattr(IdentityType, 'FUNCTIONAL_RELATION_IDENTITY'):
            forbidden.add(IdentityType.FUNCTIONAL_RELATION_IDENTITY)

        violations = self.preserved_identities & forbidden
        if violations:
            raise ValueError(
                f"Forbidden identity outputs detected: {violations}. "
                f"Relations must NOT emit semantic/ifadah/hukm identities."
            )


# ============================================================================
# D. Relation Operation Protocol
# ============================================================================

class RelationOperation(Protocol):
    """
    Base protocol for all relation operations.

    Constitutional Law:
        Relations are OPERATIONS not labels.
        Each operation must:
        1. Preserve input identities
        2. Add load/restriction/containment
        3. Return residuals
        4. Never emit semantic/ifadah/hukm

    Methods:
        apply: Apply the relation operation
        get_invariant: Get what this relation preserves/licenses/blocks
    """

    def apply(self,
              inputs: Tuple[Anchor, ...],
              context: Optional['CompositionContext'] = None) -> RelationResult:
        """
        Apply relation operation preserving identities.

        Args:
            inputs: Tuple of anchors (Entity, Transformation, Function)
            context: Optional composition context

        Returns:
            RelationResult with preserved identities and residuals

        Raises:
            ValueError: If inputs violate relation requirements
        """
        ...

    def get_invariant(self) -> RelationIdentityInvariant:
        """
        Get the invariant specification for this relation.

        Returns:
            RelationIdentityInvariant declaring what is preserved/licensed/blocked
        """
        ...


# ============================================================================
# E. Five Core Relation Operations (Stub Implementations)
# ============================================================================

class IsnadOperation:
    """
    الإسناد - Predication Operation

    Definition:
        Attribution of transformation/state to entity while preserving entity identity.

    Preserves:
        - Entity identity (المسند إليه)
        - Transformation trace (المسند)

    Licenses:
        - Addition of predication load on entity

    Blocks:
        - Collapse of entity into transformation
        - Direct meaning production
        - Direct semantic identity output

    Example:
        الرجل كاتب
        Entity: الرجل (preserved)
        Transformation: كاتب (preserved)
        Relation: ISNAD adds predication load

    Constitutional Tests:
        - test_isnad_preserves_entity_identity
        - test_isnad_preserves_transformation_trace
        - test_isnad_requires_bearability
        - test_isnad_does_not_emit_semantic_identity
    """

    def apply(self,
              inputs: Tuple[Anchor, ...],
              context: Optional['CompositionContext'] = None) -> RelationResult:
        """Apply ISNAD operation preserving both identities."""
        if len(inputs) != 2:
            raise ValueError("ISNAD requires exactly 2 inputs: entity + transformation")

        entity, transformation = inputs

        if not isinstance(entity, EntityAnchor):
            raise ValueError("First input must be EntityAnchor")
        if not isinstance(transformation, TransformationAnchor):
            raise ValueError("Second input must be TransformationAnchor")

        # Verify bearability
        if not entity.verified_bearability:
            raise ValueError(
                f"Entity {entity.identity} cannot bear predication. "
                f"Bearability must be verified before ISNAD."
            )

        # Preserve both identities
        preserved = frozenset({entity.identity, transformation.identity})

        # Add predication load
        added = frozenset({'predication_load'})

        # Create residuals (scope, agreement, etc. unresolved)
        residuals = ResidualSet(residuals=frozenset())

        return RelationResult(
            preserved_identities=preserved,
            added_loads=added,
            residuals=residuals,
            rank=Rank.CANDIDATE,
            evidence=('isnad_applied',)
        )

    def get_invariant(self) -> RelationIdentityInvariant:
        """Get ISNAD invariant specification."""
        return RelationIdentityInvariant(
            relation_type=RelationType.ISNAD,
            input_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            output_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            preserved_invariants=frozenset({'entity_stability', 'transformation_trace'}),
            permitted_shifts=frozenset({'predication_load_addition'}),
            blocked_collapses=frozenset({
                (IdentityType.FORM_IDENTITY, IdentityType.SEMANTIC_IDENTITY),
            }),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('isnad_invariant',)
        )


class TadminOperation:
    """
    التضمين - Embedding/Containment Operation

    Definition:
        Relation between container and contained preserving BOTH identities.

    Preserves:
        - Container identity
        - Contained identity

    Blocks:
        - Identity absorption

    Constitutional Tests:
        - test_tadmin_preserves_container_identity
        - test_tadmin_preserves_contained_identity
        - test_tadmin_rejects_identity_absorption
    """

    def apply(self,
              inputs: Tuple[Anchor, ...],
              context: Optional['CompositionContext'] = None) -> RelationResult:
        """Apply TADMIN operation preserving both identities."""
        if len(inputs) != 2:
            raise ValueError("TADMIN requires exactly 2 inputs: container + contained")

        container, contained = inputs

        # Preserve both identities
        preserved = frozenset({container.identity, contained.identity})

        # Add containment load
        added = frozenset({'containment_load'})

        return RelationResult(
            preserved_identities=preserved,
            added_loads=added,
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('tadmin_applied',)
        )

    def get_invariant(self) -> RelationIdentityInvariant:
        """Get TADMIN invariant specification."""
        return RelationIdentityInvariant(
            relation_type=RelationType.TADMIN,
            input_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            output_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            preserved_invariants=frozenset({'container_identity', 'contained_identity'}),
            permitted_shifts=frozenset({'containment_addition'}),
            blocked_collapses=frozenset({
                (IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            }),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('tadmin_invariant',)
        )


class TaqyidOperation:
    """
    التقييد - Restriction/Modification Operation

    Preserves:
        - Base identity
        - Restrictor trace

    Licenses:
        - Domain narrowing

    Constitutional Tests:
        - test_taqyid_preserves_base_identity
        - test_taqyid_restricts_scope_without_collapsing_base
        - test_taqyid_preserves_restrictor_trace
    """

    def apply(self,
              inputs: Tuple[Anchor, ...],
              context: Optional['CompositionContext'] = None) -> RelationResult:
        """Apply TAQYID operation preserving base identity."""
        if len(inputs) != 2:
            raise ValueError("TAQYID requires exactly 2 inputs: base + restrictor")

        base, restrictor = inputs

        # Preserve both identities
        preserved = frozenset({base.identity, restrictor.identity})

        # Add restriction load
        added = frozenset({'restriction_load'})

        return RelationResult(
            preserved_identities=preserved,
            added_loads=added,
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('taqyid_applied',)
        )

    def get_invariant(self) -> RelationIdentityInvariant:
        """Get TAQYID invariant specification."""
        return RelationIdentityInvariant(
            relation_type=RelationType.TAQYID,
            input_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            output_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            preserved_invariants=frozenset({'base_identity', 'restrictor_trace'}),
            permitted_shifts=frozenset({'scope_restriction'}),
            blocked_collapses=frozenset({
                (IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            }),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('taqyid_invariant',)
        )


class WasfOperation:
    """
    الوصف - Description/Attribution Operation

    Preserves:
        - Described entity identity (الموصوف)
        - Descriptor trace (الصفة)

    Constitutional Tests:
        - test_wasf_preserves_mawsuf_identity
    """

    def apply(self,
              inputs: Tuple[Anchor, ...],
              context: Optional['CompositionContext'] = None) -> RelationResult:
        """Apply WASF operation preserving described entity."""
        if len(inputs) != 2:
            raise ValueError("WASF requires exactly 2 inputs: mawsuf + sifat")

        mawsuf, sifat = inputs

        # Preserve both identities
        preserved = frozenset({mawsuf.identity, sifat.identity})

        # Add description load
        added = frozenset({'description_load'})

        return RelationResult(
            preserved_identities=preserved,
            added_loads=added,
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('wasf_applied',)
        )

    def get_invariant(self) -> RelationIdentityInvariant:
        """Get WASF invariant specification."""
        return RelationIdentityInvariant(
            relation_type=RelationType.WASF,
            input_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            output_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            preserved_invariants=frozenset({'mawsuf_identity', 'sifat_trace'}),
            permitted_shifts=frozenset({'description_addition'}),
            blocked_collapses=frozenset(),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('wasf_invariant',)
        )


class IdafahOperation:
    """
    الإضافة - Attachment/Possession Operation

    Preserves:
        - Attached entity (المضاف)
        - Attachment target (المضاف إليه)

    Blocks:
        - Forced ownership interpretation

    Constitutional Tests:
        - test_idafah_preserves_both_identities_without_forcing_ownership
    """

    def apply(self,
              inputs: Tuple[Anchor, ...],
              context: Optional['CompositionContext'] = None) -> RelationResult:
        """Apply IDAFAH operation preserving both identities."""
        if len(inputs) != 2:
            raise ValueError("IDAFAH requires exactly 2 inputs: mudaf + mudaf_ilayh")

        mudaf, mudaf_ilayh = inputs

        # Preserve both identities
        preserved = frozenset({mudaf.identity, mudaf_ilayh.identity})

        # Add attachment load
        added = frozenset({'attachment_load'})

        return RelationResult(
            preserved_identities=preserved,
            added_loads=added,
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('idafah_applied',)
        )

    def get_invariant(self) -> RelationIdentityInvariant:
        """Get IDAFAH invariant specification."""
        return RelationIdentityInvariant(
            relation_type=RelationType.IDAFAH,
            input_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            output_identities=(IdentityType.FORM_IDENTITY, IdentityType.FORM_IDENTITY),
            preserved_invariants=frozenset({'mudaf_identity', 'mudaf_ilayh_identity'}),
            permitted_shifts=frozenset({'attachment_addition'}),
            blocked_collapses=frozenset(),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
            evidence=('idafah_invariant',)
        )


# ============================================================================
# F. Registry of Operations
# ============================================================================

RELATION_OPERATIONS = {
    RelationType.ISNAD: IsnadOperation(),
    RelationType.TADMIN: TadminOperation(),
    RelationType.TAQYID: TaqyidOperation(),
    RelationType.WASF: WasfOperation(),
    RelationType.IDAFAH: IdafahOperation(),
}


def get_relation_operation(relation_type: RelationType) -> RelationOperation:
    """Get the operation implementation for a relation type."""
    return RELATION_OPERATIONS[relation_type]
