"""
Relation Candidate Boundary Types (أنواع حدود النسبة المرشحة)

PR #140: Constitutional boundary types for relation algebra.

This module implements ONLY boundary types (carriers), NOT relation algorithms.

Constitutional Laws:
    1. No relation candidate may produce meaning, hukm, or reality
    2. No single relation closes ifadah alone
    3. RelationNetworkCandidate is a carrier, NOT a closure engine
    4. Every relation MUST preserve anchor_id and trace
    5. Every relation MUST carry residual audit
    6. Every relation MUST declare relation_type and rank

Forbidden Outputs:
    ❌ meaning, final_meaning, contextual_meaning
    ❌ hukm, judgment
    ❌ reality, waqiʿ
    ❌ ifadah (single relations do NOT close ifadah)

Permitted Outputs:
    ✅ RelationCandidate instances with preserved identities
    ✅ RelationNetworkCandidate as relation carrier
    ✅ Residuals for unresolved aspects
    ✅ Rank (CANDIDATE/HYPOTHESIS/STRONG_HYPOTHESIS, never CERTIFICATE for relations)

Architecture Position:
    WordformCandidate
        → RelationCandidate (single edge)
        → RelationCandidateSet (multiple edges)
        → RelationNetworkCandidate (network structure)
        → [future: RelationClosureGate]
        → [future: Ifadah_Dal]

Reference:
    docs/RELATION_ALGORITHMS_APPENDIX.md
    docs/ARABIC_ALGEBRA_ALGORITHM_CONSTITUTION.md

Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, FrozenSet

from dal_core.foundation import Rank, ResidualSet


# ============================================================================
# Core Relation Type Classification
# ============================================================================

class RelationType(Enum):
    """
    Four core relation types.

    Three major semantic-syntactic relations:
        PREDICATIVE: Predication/Carrying (حمل - ḥaml)
        INCLUSION: Embedding/Containment (تضمين - taḍmīn)
        RESTRICTIVE: Restriction/Narrowing (تقييد - taqyīd)

    One closure/support relation:
        REFERENCE: Referential linking (إحالة - iḥāla)

    Constitutional Distinction:
        The three major relations are primary semantic-syntactic operations.
        Reference is a closure/support operation necessary for network completion.

        All four are RelationType programmatically, but reference has distinct
        constitutional status as a closure edge, not a primary semantic relation.
    """
    PREDICATIVE = auto()   # النسبة الإسنادية - Predication
    INCLUSION = auto()     # النسبة التضمينية - Inclusion
    RESTRICTIVE = auto()   # النسبة التقييدية - Restriction
    REFERENCE = auto()     # النسبة الإحالية - Reference (closure edge)


class InclusionType(Enum):
    """Types of inclusion relation."""
    GENUS_SPECIES = auto()       # جنس/نوع
    PART_WHOLE = auto()          # جزء/كل
    ATTRIBUTE = auto()           # صفة داخلة
    FIELD_ELEMENT = auto()       # مجال/عنصر
    LEXICAL_ENTAILMENT = auto()  # تضمين معجمي
    CONCEPTUAL_ENTAILMENT = auto()  # لزوم مفهومي
    FUNCTIONAL = auto()          # وظيفي


class RestrictionType(Enum):
    """Types of restrictive relation."""
    ATTRIBUTIVE = auto()         # وصفية
    POSSESSIVE = auto()          # إضافية
    ADVERBIAL = auto()           # ظرفية
    CIRCUMSTANTIAL = auto()      # حالية
    SPECIFICATIVE = auto()       # تمييزية
    PREPOSITIONAL = auto()       # جرية/حرفية
    CONDITIONAL = auto()         # شرطية
    PURPOSIVE = auto()           # غائية
    CAUSAL = auto()              # سببية
    NUMERICAL = auto()           # عددية
    EXCEPTIVE = auto()           # استثنائية
    EXCLUSIVE = auto()           # حصرية
    RELATIVE = auto()            # موصولية
    REFERENTIAL = auto()         # إحالية


class ReferenceType(Enum):
    """Types of reference relation."""
    DEMONSTRATIVE = auto()       # إشارية (هذا، ذلك)
    RELATIVE = auto()            # موصولية (الذي، التي)
    PRONOMINAL = auto()          # ضميرية (هو، هي)
    DEFINITE_ARTICLE = auto()    # تعريفية (ال)


# ============================================================================
# Base RelationCandidate
# ============================================================================

@dataclass(frozen=True)
class RelationCandidate:
    """
    Base relation candidate (نسبة مرشحة).

    Constitutional Laws:
        - MUST preserve anchor_id
        - MUST carry trace
        - MUST carry residual_audit
        - MUST have rank
        - MUST declare relation_type
        - FORBIDDEN: produce meaning, hukm, reality, ifadah

    Fields:
        anchor_id: Preserved anchor identity
        related_id: Related term identity
        relation_type: Type of relation (PREDICATIVE/INCLUSION/RESTRICTIVE/REFERENCE)
        trace: Operational trace (origin of this relation)
        residuals: Residual audit (unresolved issues)
        rank: Epistemic rank (CANDIDATE/HYPOTHESIS/STRONG_HYPOTHESIS)
        forbidden_outputs: Metadata listing forbidden operations

    Forbidden Methods (MUST NOT exist):
        - to_hukm()
        - to_reality()
        - to_final_meaning()
        - to_ifadah()
        - close_ifadah()
        - emit_hukm()
        - emit_reality()
    """
    anchor_id: str
    related_id: str
    relation_type: RelationType
    trace: Tuple[str, ...]
    residuals: ResidualSet
    rank: Rank

    @property
    def forbidden_outputs(self) -> Tuple[str, ...]:
        """Metadata listing forbidden operations."""
        return ("meaning", "hukm", "reality", "ifadah")

    def __post_init__(self):
        """
        Validate relation candidate invariants.

        Uses ValueError for validation (NOT assert).
        """
        # Validate anchor_id
        if not self.anchor_id:
            raise ValueError("RelationCandidate requires non-empty anchor_id")
        if not isinstance(self.anchor_id, str):
            raise TypeError(f"anchor_id must be str, got {type(self.anchor_id)}")

        # Validate related_id
        if not self.related_id:
            raise ValueError("RelationCandidate requires non-empty related_id")
        if not isinstance(self.related_id, str):
            raise TypeError(f"related_id must be str, got {type(self.related_id)}")

        # Validate relation_type
        if not isinstance(self.relation_type, RelationType):
            raise TypeError(f"relation_type must be RelationType, got {type(self.relation_type)}")

        # Validate trace
        if not isinstance(self.trace, tuple):
            raise TypeError(f"trace must be tuple, got {type(self.trace)}")
        if not self.trace:
            raise ValueError("RelationCandidate requires non-empty trace")

        # Validate residuals
        if not isinstance(self.residuals, ResidualSet):
            raise TypeError(f"residuals must be ResidualSet, got {type(self.residuals)}")

        # Validate rank
        if not isinstance(self.rank, Rank):
            raise TypeError(f"rank must be Rank, got {type(self.rank)}")

        # Constitutional guard: Relations MUST NOT be CERTIFICATE rank
        if self.rank == Rank.CERTIFICATE:
            raise ValueError(
                "RelationCandidate cannot have CERTIFICATE rank. "
                "Relations are hypotheses, not certificates."
            )


# ============================================================================
# Predicative Relation (النسبة الإسنادية)
# ============================================================================

@dataclass(frozen=True)
class PredicativeRelationCandidate(RelationCandidate):
    """
    Predicative relation candidate (النسبة الإسنادية).

    Links a predicate to an anchor/subject.

    Examples:
        زيد قائم (Zayd [is] standing)
        الكتاب جديد (The book [is] new)

    Fields:
        predicate_id: Identity of the predicate
        agreement_trace: Optional trace of agreement checking

    Constitutional Laws:
        - Does NOT mean anchor actually has the predicate in reality
        - Only establishes dal predicative structure
        - Cannot close ifadah alone
        - Cannot produce hukm or reality
    """
    predicate_id: str
    agreement_trace: Optional[Tuple[str, ...]] = None

    def __post_init__(self):
        """Validate predicative relation invariants."""
        # Call parent validation
        super().__post_init__()

        # Verify relation_type is PREDICATIVE
        if self.relation_type != RelationType.PREDICATIVE:
            raise ValueError(
                f"PredicativeRelationCandidate requires relation_type=PREDICATIVE, "
                f"got {self.relation_type}"
            )

        # Validate predicate_id
        if not self.predicate_id:
            raise ValueError("PredicativeRelationCandidate requires non-empty predicate_id")
        if not isinstance(self.predicate_id, str):
            raise TypeError(f"predicate_id must be str, got {type(self.predicate_id)}")


# ============================================================================
# Inclusion Relation (النسبة التضمينية)
# ============================================================================

@dataclass(frozen=True)
class InclusionRelationCandidate(RelationCandidate):
    """
    Inclusion relation candidate (النسبة التضمينية).

    One term within the domain of another (genus-species, part-whole, etc.).

    Examples:
        الإنسان حيوان (Human [is] animal)
        السقف من البيت (Ceiling [is part] of house)

    Fields:
        container_id: Identity of the containing term
        inclusion_type: Type of inclusion (genus-species, part-whole, etc.)

    Constitutional Laws:
        - Does NOT establish reality/existence
        - Only establishes dal inclusion structure
        - Cannot close ifadah alone
        - Cannot produce hukm or reality
    """
    container_id: str
    inclusion_type: InclusionType

    def __post_init__(self):
        """Validate inclusion relation invariants."""
        # Call parent validation
        super().__post_init__()

        # Verify relation_type is INCLUSION
        if self.relation_type != RelationType.INCLUSION:
            raise ValueError(
                f"InclusionRelationCandidate requires relation_type=INCLUSION, "
                f"got {self.relation_type}"
            )

        # Validate container_id
        if not self.container_id:
            raise ValueError("InclusionRelationCandidate requires non-empty container_id")
        if not isinstance(self.container_id, str):
            raise TypeError(f"container_id must be str, got {type(self.container_id)}")

        # Validate inclusion_type
        if not isinstance(self.inclusion_type, InclusionType):
            raise TypeError(f"inclusion_type must be InclusionType, got {type(self.inclusion_type)}")


# ============================================================================
# Restrictive Relation (النسبة التقييدية)
# ============================================================================

@dataclass(frozen=True)
class RestrictiveRelationCandidate(RelationCandidate):
    """
    Restrictive relation candidate (النسبة التقييدية).

    Narrows the domain of anchor without creating final judgment.

    Examples:
        رجل كريم (generous man) - attribute restriction
        جاء زيد صباحًا (Zayd came in-morning) - temporal restriction
        كتاب الطالب (book of-student) - possessive restriction

    Fields:
        base_id: Identity of the restricted base
        restrictor_id: Identity of the restrictor
        restriction_type: Type of restriction (attributive, temporal, etc.)

    Constitutional Laws:
        - Restriction narrows domain but does NOT create the base
        - Cannot close ifadah alone
        - Cannot produce hukm or reality
    """
    base_id: str
    restrictor_id: str
    restriction_type: RestrictionType

    def __post_init__(self):
        """Validate restrictive relation invariants."""
        # Call parent validation
        super().__post_init__()

        # Verify relation_type is RESTRICTIVE
        if self.relation_type != RelationType.RESTRICTIVE:
            raise ValueError(
                f"RestrictiveRelationCandidate requires relation_type=RESTRICTIVE, "
                f"got {self.relation_type}"
            )

        # Validate base_id
        if not self.base_id:
            raise ValueError("RestrictiveRelationCandidate requires non-empty base_id")
        if not isinstance(self.base_id, str):
            raise TypeError(f"base_id must be str, got {type(self.base_id)}")

        # Validate restrictor_id
        if not self.restrictor_id:
            raise ValueError("RestrictiveRelationCandidate requires non-empty restrictor_id")
        if not isinstance(self.restrictor_id, str):
            raise TypeError(f"restrictor_id must be str, got {type(self.restrictor_id)}")

        # Validate restriction_type
        if not isinstance(self.restriction_type, RestrictionType):
            raise TypeError(
                f"restriction_type must be RestrictionType, got {type(self.restriction_type)}"
            )


# ============================================================================
# Reference Relation (النسبة الإحالية)
# ============================================================================

@dataclass(frozen=True)
class ReferenceRelationCandidate(RelationCandidate):
    """
    Reference relation candidate (النسبة الإحالية).

    Referential linking necessary for network closure.

    Examples:
        هذا رجل (this [is-a] man) - demonstrative reference
        الذي جاء كريم (who came [is] generous) - relative reference
        هو قائم (he [is] standing) - pronominal reference

    Fields:
        referent_id: Identity of the referent
        reference_type: Type of reference (demonstrative, relative, pronominal)

    Constitutional Status:
        Reference is a CLOSURE/SUPPORT relation, not a primary semantic relation.
        Many ifadah structures cannot close without reference edges.

    Constitutional Laws:
        - Does NOT establish reality
        - Necessary for closure but insufficient alone
        - Cannot close ifadah alone
        - Cannot produce hukm or reality
    """
    referent_id: str
    reference_type: ReferenceType

    def __post_init__(self):
        """Validate reference relation invariants."""
        # Call parent validation
        super().__post_init__()

        # Verify relation_type is REFERENCE
        if self.relation_type != RelationType.REFERENCE:
            raise ValueError(
                f"ReferenceRelationCandidate requires relation_type=REFERENCE, "
                f"got {self.relation_type}"
            )

        # Validate referent_id
        if not self.referent_id:
            raise ValueError("ReferenceRelationCandidate requires non-empty referent_id")
        if not isinstance(self.referent_id, str):
            raise TypeError(f"referent_id must be str, got {type(self.referent_id)}")

        # Validate reference_type
        if not isinstance(self.reference_type, ReferenceType):
            raise TypeError(f"reference_type must be ReferenceType, got {type(self.reference_type)}")


# ============================================================================
# Relation Network Carrier
# ============================================================================

@dataclass(frozen=True)
class RelationNetworkCandidate:
    """
    Relation network carrier (حامل شبكة النسب).

    Constitutional Law:
        RelationNetworkCandidate is a CARRIER, NOT a closure engine.
        It holds relation edges but does NOT close ifadah itself.

        Future closure will be performed by:
            - RelationClosureGate
            - IfadahDalClosureGate

    Single relations CANNOT close ifadah:
        ❌ PredicativeRelationCandidate alone ≠ Ifadah_Dal
        ❌ InclusionRelationCandidate alone ≠ Ifadah_Dal
        ❌ RestrictiveRelationCandidate alone ≠ Ifadah_Dal
        ❌ ReferenceRelationCandidate alone ≠ Ifadah_Dal

    Network may enable closure with all conditions:
        ✅ Terms known or estimated
        ✅ Relations classified
        ✅ Edges non-conflicting
        ✅ Reference stable
        ✅ No blocking residuals
        ✅ Sufficient rank

    Fields:
        relations: Tuple of relation candidates (immutable)
        network_rank: Overall network rank
        closure_residuals: Network-level residuals
        closure_eligible: Whether network meets basic closure preconditions

    Forbidden Methods (MUST NOT exist in PR #140):
        - close_ifadah()
        - to_ifadah()
        - emit_ifadah()
    """
    relations: Tuple[RelationCandidate, ...]
    network_rank: Rank
    closure_residuals: ResidualSet
    closure_eligible: bool = False

    def __post_init__(self):
        """
        Validate relation network invariants.

        Uses ValueError for validation (NOT assert).
        """
        # Validate relations
        if not isinstance(self.relations, tuple):
            raise TypeError(f"relations must be tuple, got {type(self.relations)}")
        if not self.relations:
            raise ValueError("RelationNetworkCandidate requires non-empty relations")

        # Verify all items are RelationCandidate instances
        for i, rel in enumerate(self.relations):
            if not isinstance(rel, RelationCandidate):
                raise TypeError(
                    f"relations[{i}] must be RelationCandidate, got {type(rel)}"
                )

        # Validate network_rank
        if not isinstance(self.network_rank, Rank):
            raise TypeError(f"network_rank must be Rank, got {type(self.network_rank)}")

        # Validate closure_residuals
        if not isinstance(self.closure_residuals, ResidualSet):
            raise TypeError(
                f"closure_residuals must be ResidualSet, got {type(self.closure_residuals)}"
            )

        # Validate closure_eligible
        if not isinstance(self.closure_eligible, bool):
            raise TypeError(f"closure_eligible must be bool, got {type(self.closure_eligible)}")
