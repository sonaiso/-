"""
U₇-C Clause Surface Agreement Contract Carrier (حامل عقد تعاقدات الجملة السطحية)

Domain: U₇-C = ClauseSurfaceAgreementCarrier
Purpose: Protect clause-level surface agreement contracts before root extraction
Transition: U₇-B (WordSurfaceGuard) → U₇-C (ClauseSurfaceAgreement) → U₈ (RootStemCandidate)

Critical Laws (Axioms):
    - Axiom 7C.1: العلامة لا تُفهم إلا في تعاقد (Marker understood only in contract)
    - Axiom 7C.2: التعاقد ≠ الإعراب (Agreement ≠ i'rab judgment)
    - Axiom 7C.3: التعاقد ≠ الوظيفة (Agreement ≠ function assignment)
    - Axiom 7C.4: الحافة السطحية ≠ الحكم النحوي (Surface edge ≠ grammatical judgment)
    - Axiom 7C.5: لا حكم قبل العلاقات (No judgment before relations)
    - Axiom 7C.6: جمع التكسير يحتاج عقدًا متعدد الأبعاد (Broken plural needs multi-dimensional contract)

Type System:
    ClauseSurfaceAgreement ≠ FinalI'rab
    ClauseSurfaceAgreement ≠ GrammaticalFunction
    ClauseSurfaceAgreement ≠ SemanticInterpretation
    ClauseSurfaceAgreement ≠ ResolvedReference
    AgreementEdge ≠ SyntacticRelation
    SurfaceContract ≠ Hukm

Architecture:
    U₇-B (WordSurfaceGuard) → CPB₇C → U₇-C (ClauseSurfaceAgreement) → CPB₈ → U₈ (RootStem)

Key Principle:
    U₇-C protects clause-level agreement contracts from being consumed by root/weight extraction.
    U₇-C observes agreement patterns, NOT assigns grammatical function.
    U₇-C elevates or confirms U₇-B permissions based on agreement evidence.

Separation from U₇-B:
    U₇-B answers: "ما العلامات داخل هذه الكلمة؟" (What markers within this word?)
    U₇-C answers: "ما التعاقدات بين الكلمات؟" (What contracts between words?)

Example Analysis:
    الكتبُ كثيرةٌ

    U₇-B sees:
        الكتب → broken_plural_hint=possible, root_input_permission=DEFERRED
        كثيرة → feminine_marker_hint=possible, root_input_permission=ALLOWED

    U₇-C sees EDGE:
        الكتب ↔ كثيرة
        → non_rational_plural_feminine_singular_agreement = possible
        → broken_plural_rationality_hint = non_rational_possible
        → Agreement evidence strengthens singular_candidate_path

    But U₇-C does NOT:
        - Extract root from "الكتب"
        - Assign mubtada'/khabar status
        - Certify i'rab
        - Resolve semantic gender

U₇-C Output:
    Gives U₈:
        - Agreement surface candidates
        - Rationality surface hints
        - Gender surface contracts
        - Broken plural guard nodes
        - Permission elevations/confirmations
        - residuals (ambiguities)
        - rank (zero → candidate → hypothesis)

U₇-C Does NOT Give:
    - Root extraction (U₈)
    - Weight determination (U₉)
    - I'rab final judgment (U₇+)
    - Grammatical function assignment (mubtada', khabar, fā'il, maf'ūl)
    - Semantic interpretation (U₁₅)

PR: U7C-CLAUSE-SURFACE-AGREEMENT
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.residuals import Residual, ResidualType, make_blocker, make_warning
from dal_core.foundation import (
    Rank,
    RankVector,
    ProofObject,
    make_proof_object,
    ResidualSet,
    merge_residuals,
    has_blocking_residuals
)
from dal_core.u7b_inflectional_surface_contract_carrier import (
    InflectionalSurfaceContractLayerObject,
    InflectionalSurfaceContractUnit,
    MarkerHint,
    RootInputPermission,
)


# ============================================================================
# Type System - Agreement Classification
# ============================================================================

class AgreementHint(Enum):
    """
    Agreement hint values (NOT judgments).

    These are surface agreement observations/hints, not grammatical judgments.
    """
    POSSIBLE = "possible"              # ممكن
    UNLIKELY = "unlikely"              # غير محتمل
    UNRESOLVED = "unresolved"          # غير محسوم
    AMBIGUOUS = "ambiguous"            # ملتبس
    CONFLICTING = "conflicting"        # متعارض


class RationalityHint(Enum):
    """
    Rationality surface hints (عاقلية).

    NOT definitive classification, only surface hints.
    """
    HUMAN_POSSIBLE = "human_possible"           # محتمل إنسان
    NON_RATIONAL_POSSIBLE = "non_rational_possible"  # محتمل غير عاقل
    RATIONAL_POSSIBLE = "rational_possible"     # محتمل عاقل
    UNRESOLVED = "unresolved"                   # غير محسوم
    AMBIGUOUS = "ambiguous"                     # ملتبس


class GenderSurfaceHint(Enum):
    """
    Gender surface hints (جنس).

    Covers multiple types of feminine/masculine.
    """
    MASCULINE_POSSIBLE = "masculine_possible"
    FEMININE_POSSIBLE = "feminine_possible"
    REAL_FEMININE_HINT = "real_feminine_hint"       # تأنيث حقيقي (ة/ات markers)
    SEMANTIC_FEMININE_HINT = "semantic_feminine_hint"  # تأنيث معنوي (no marker)
    GRAMMATICAL_FEMININE_HINT = "grammatical_feminine_hint"  # تأنيث نحوي (agreement-based)
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"


class NumberSurfaceHint(Enum):
    """
    Number surface hints (عدد).
    """
    SINGULAR_POSSIBLE = "singular_possible"
    DUAL_POSSIBLE = "dual_possible"
    PLURAL_POSSIBLE = "plural_possible"
    BROKEN_PLURAL_POSSIBLE = "broken_plural_possible"
    SOUND_PLURAL_POSSIBLE = "sound_plural_possible"
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"


class AgreementEdgeType(Enum):
    """
    Types of agreement edges between words.
    """
    NOUN_ADJECTIVE = "noun_adjective"           # اسم - صفة
    VERB_SUBJECT = "verb_subject"               # فعل - فاعل
    MUBTADA_KHABAR = "mubtada_khabar"          # مبتدأ - خبر
    NA3T_MAN3UT = "na3t_man3ut"                # نعت - منعوت
    BROKEN_PLURAL_ADJECTIVE = "broken_plural_adjective"  # جمع تكسير - صفة
    UNRESOLVED = "unresolved"


class TransitivityHint(Enum):
    """
    Transitivity surface potential hints (NOT judgments).
    """
    INTRANSITIVE_HINT = "intransitive_hint"
    TRANSITIVE_ONE_OBJECT_HINT = "transitive_one_object_hint"
    TRANSITIVE_TWO_OBJECTS_HINT = "transitive_two_objects_hint"
    PREPOSITIONAL_OBJECT_HINT = "prepositional_object_hint"
    UNRESOLVED = "unresolved"


class WeakRadicalRisk(Enum):
    """
    Weak radical surface risk hints.
    """
    INITIAL_WEAK_RISK = "initial_weak_risk"     # فاء معتلة
    MEDIAL_WEAK_RISK = "medial_weak_risk"       # عين معتلة
    FINAL_WEAK_RISK = "final_weak_risk"         # لام معتلة
    HAMZATED_RISK = "hamzated_risk"             # مهموز
    DOUBLED_RISK = "doubled_risk"               # مضعّف
    HOLLOW_RISK = "hollow_risk"                 # أجوف
    DEFECTIVE_RISK = "defective_risk"           # ناقص
    NO_RISK = "no_risk"
    UNRESOLVED = "unresolved"


# ============================================================================
# Broken Plural Surface Guard Node (Multi-Dimensional)
# ============================================================================

@dataclass(frozen=True)
class BrokenPluralGuardNode:
    """
    Multi-dimensional broken plural protection node.

    This is NOT a simple pattern match - it combines 10+ dimensions
    that cannot be safely reduced to root_input before comprehensive analysis.

    Critical Law: جمع التكسير لا يدخل U₈ إلا بترخيص متعدد الأبعاد
                  Broken plural SHALL NOT enter U₈ without multi-dimensional licensing
    """
    uid: str
    surface: str  # Original broken plural surface

    # Pattern dimension
    broken_pattern_hint: str  # فِعال، فُعُول، مَفَاعِل، etc. (or empty if unresolved)

    # Singular recovery dimension
    singular_candidate_path: Optional[str]  # Probable singular (requires lexicon)
    singular_requires_lexicon: bool  # Does singular-plural link require lexical attestation?

    # Derivational status dimension
    singular_jamid_potential: MarkerHint  # Is singular frozen/primitive (جامد)?
    singular_mushtaq_potential: MarkerHint  # Is singular derived (مشتق)?

    # Ontic type dimension
    entity_noun_potential: MarkerHint  # اسم ذات (concrete entity)
    adjective_potential: MarkerHint  # صفة (quality/attribute)

    # Adjective source dimension (if adjective)
    adjective_source_hint: Optional[str]  # اسم فاعل، صفة مشبهة، etc.

    # Gender contracts dimension
    gender_surface_hint: GenderSurfaceHint
    real_feminine_hint: MarkerHint
    semantic_feminine_hint: MarkerHint
    grammatical_feminine_agreement_hint: MarkerHint

    # Rationality dimension
    rationality_surface_hint: RationalityHint

    # Agreement behavior dimension
    agreement_edges: Tuple[str, ...]  # UIDs of agreement edges involving this plural

    # Transitivity path dimension (if verb-derived)
    transitivity_path_hint: TransitivityHint

    # Root weakness dimension
    weak_radical_risk: WeakRadicalRisk

    # Lexical evidence dimension
    lexical_attestation_required: bool

    # Permission dimension
    root_input_permission: RootInputPermission  # CRITICAL: Usually DEFERRED

    # Residuals
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]


@dataclass(frozen=True)
class TransitivitySurfacePotential:
    """
    Transitivity surface potential (NOT judgment).

    Represents surface hints about verb transitivity before syntactic analysis.
    """
    uid: str
    surface_word: str

    intransitive_path_hint: MarkerHint
    transitive_one_object_hint: MarkerHint
    transitive_two_objects_hint: MarkerHint
    prepositional_object_hint: MarkerHint
    passive_blocks_agent_hint: MarkerHint

    residuals: FrozenSet[Residual]


@dataclass(frozen=True)
class WeakRadicalRiskVector:
    """
    Weak radical surface risk vector.

    Warns U₈ about potential root weakness before extraction.
    """
    uid: str
    surface_word: str

    initial_weak_risk: MarkerHint  # فاء
    medial_weak_risk: MarkerHint  # عين
    final_weak_risk: MarkerHint  # لام
    hamzated_risk: MarkerHint
    doubled_risk: MarkerHint
    hollow_surface_risk: MarkerHint
    defective_surface_risk: MarkerHint

    residuals: FrozenSet[Residual]


# ============================================================================
# Agreement Edge Structures
# ============================================================================

@dataclass(frozen=True)
class AgreementSurfaceEdge:
    """
    Represents a surface agreement contract between two words.

    This is NOT a syntactic relation - it's a surface agreement observation.
    """
    uid: str
    edge_type: AgreementEdgeType

    # Source and target units from U₇-B
    source_unit_id: str  # First word in agreement
    target_unit_id: str  # Second word in agreement

    # Agreement dimensions
    number_agreement_hint: AgreementHint
    gender_agreement_hint: AgreementHint
    rationality_agreement_hint: AgreementHint

    # Specific agreement patterns
    broken_plural_feminine_singular_hint: MarkerHint  # جمع تكسير يعامل معاملة مفرد مؤنث
    non_rational_plural_feminine_agreement_hint: MarkerHint

    # Evidence and ambiguities
    residuals: FrozenSet[Residual]
    rank: Rank


@dataclass(frozen=True)
class AgreementSurfaceCandidate:
    """
    A candidate agreement pattern in the clause.

    Represents a potential agreement contract (NOT certified relation).
    """
    uid: str
    agreement_edge: AgreementSurfaceEdge

    # Evidence supporting this agreement
    number_evidence: Optional[str] = None
    gender_evidence: Optional[str] = None
    rationality_evidence: Optional[str] = None

    # Permission effects
    elevates_permission: bool = False  # Does this agreement elevate a DEFERRED permission?
    confirms_permission: bool = False  # Does this agreement confirm an ALLOWED permission?

    residuals: FrozenSet[Residual]
    rank: Rank


# ============================================================================
# Failure Types
# ============================================================================

class ClauseSurfaceAgreementFailureType(Enum):
    """Failure types for clause surface agreement determination."""
    NO_U7B_UNITS = "no_u7b_units"
    INVALID_INPUT_LAYER = "invalid_input_layer"
    TRACE_LOSS = "trace_loss"
    CONFLICTING_AGREEMENTS = "conflicting_agreements"


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class ClauseSurfaceAgreementUnit:
    """
    U₇-C clause surface agreement unit.

    This represents CLAUSE-LEVEL AGREEMENT PROTECTION, NOT grammatical analysis.
    Observes agreement patterns, does NOT assign grammatical function.

    Forbidden fields (CRITICAL - these cause ValueError):
        - root (that's U₈)
        - stem (that's U₈)
        - weight (that's U₉)
        - pattern (that's U₉)
        - meaning (that's U₁₅)
        - hukm (that's U₇+)
        - fa3il (that's syntactic analysis)
        - maf3ul (that's syntactic analysis)
        - mubtada (that's syntactic analysis)
        - khabar (that's syntactic analysis)
        - final_irab (that's U₇+)
        - resolved_reference (that's U₁₅)
    """
    uid: str
    surface: str  # Original orthographic surface from U₇-B
    source_u7b_unit_id: str  # Trace to U₇-B unit
    source_u7b_trace: Tuple[str, ...]  # Ordered trace to U₇-B

    # Core from U₇-B (carried forward)
    protected_core: str  # From U₇-B
    root_input: str  # From U₇-B
    root_input_permission: RootInputPermission  # May be elevated by U₇-C

    # Broken plural guard (if applicable)
    broken_plural_guard: Optional[BrokenPluralGuardNode] = None

    # Surface potential hints
    transitivity_potential: Optional[TransitivitySurfacePotential] = None
    weak_radical_risk_vector: Optional[WeakRadicalRiskVector] = None

    # Agreement edges this unit participates in
    agreement_edges: Tuple[str, ...] = ()  # UIDs of AgreementSurfaceEdge

    # Rationality and gender hints (may be elevated from U₇-B based on agreement)
    rationality_surface_hint: RationalityHint = RationalityHint.UNRESOLVED
    gender_surface_hint: GenderSurfaceHint = GenderSurfaceHint.UNRESOLVED
    number_surface_hint: NumberSurfaceHint = NumberSurfaceHint.UNRESOLVED

    # Permission elevation tracking
    permission_elevated_by_agreement: bool = False  # Was permission elevated by U₇-C?
    permission_elevation_evidence: Optional[str] = None  # Evidence for elevation

    # Evidence and ambiguities
    residuals: FrozenSet[Residual] = frozenset()
    rank: Rank = Rank.ZERO
    trace: Tuple[str, ...] = ()  # Full ordered trace from U₀

    def __post_init__(self):
        """Validate clause surface agreement unit - CRITICAL constitutional checks."""
        # FORBIDDEN FIELDS - These MUST NOT exist
        forbidden_fields = [
            'root', 'root_certificate',
            'stem', 'stem_certificate',
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab', 'i3rab_final',
            'fa3il', 'maf3ul', 'mubtada', 'khabar',
            'resolved_reference'
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"ClauseSurfaceAgreementUnit MUST NOT contain '{field}' field "
                    f"(Axiom 7C.1-7C.6 violation)"
                )

        # CRITICAL: Verify architectural separation
        if not hasattr(self, 'surface'):
            raise ValueError("ClauseSurfaceAgreementUnit MUST contain 'surface' field")
        if not hasattr(self, 'protected_core'):
            raise ValueError("ClauseSurfaceAgreementUnit MUST contain 'protected_core' field")
        if not hasattr(self, 'root_input'):
            raise ValueError("ClauseSurfaceAgreementUnit MUST contain 'root_input' field")


@dataclass(frozen=True)
class ClauseSurfaceAgreementLayerObject:
    """
    U₇-C layer object containing clause surface agreement contracts.

    Provides agreement observations and permission elevations for U₈.
    """
    uid: str
    units: Tuple[ClauseSurfaceAgreementUnit, ...]  # Agreement units
    agreement_edges: Tuple[AgreementSurfaceEdge, ...]  # All agreement edges
    agreement_candidates: Tuple[AgreementSurfaceCandidate, ...]  # Agreement candidates
    broken_plural_guards: Tuple[BrokenPluralGuardNode, ...]  # All broken plural guards

    source_u7b_layer_id: str  # Trace to U₇-B layer
    trace_7b: Tuple[str, ...]  # Ordered trace to U₇-B
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None

    def __post_init__(self):
        """Validate clause surface agreement layer object."""
        if len(self.units) == 0:
            raise ValueError("ClauseSurfaceAgreementLayerObject must contain at least one unit")

        # Verify all agreement edges reference valid unit IDs
        unit_ids = frozenset(u.uid for u in self.units)
        for edge in self.agreement_edges:
            if edge.source_unit_id not in unit_ids:
                raise ValueError(f"Agreement edge references non-existent source unit: {edge.source_unit_id}")
            if edge.target_unit_id not in unit_ids:
                raise ValueError(f"Agreement edge references non-existent target unit: {edge.target_unit_id}")


# ============================================================================
# CPB Identity Guardian (Constitutional Law Enforcement)
# ============================================================================

def verify_no_premature_judgment(unit: ClauseSurfaceAgreementUnit) -> None:
    """
    CPB Identity Guardian: Verify no premature grammatical judgment.

    Constitutional Law: Agreement observation ≠ Grammatical judgment
    """
    # This is enforced by __post_init__ checks
    # Additional runtime verification can go here
    pass


# ============================================================================
# Agreement Detection Functions (Placeholder for Phase 4)
# ============================================================================

def detect_noun_adjective_agreement(
    units: Tuple[ClauseSurfaceAgreementUnit, ...]
) -> Tuple[AgreementSurfaceEdge, ...]:
    """
    Detect noun-adjective agreement patterns.

    Returns agreement edges (NOT syntactic relations).
    """
    # Placeholder for Phase 4 implementation
    return ()


def detect_verb_subject_agreement(
    units: Tuple[ClauseSurfaceAgreementUnit, ...]
) -> Tuple[AgreementSurfaceEdge, ...]:
    """
    Detect verb-subject agreement patterns.

    Returns agreement edges (NOT syntactic relations).
    """
    # Placeholder for Phase 4 implementation
    return ()


def detect_broken_plural_feminine_singular_agreement(
    units: Tuple[ClauseSurfaceAgreementUnit, ...]
) -> Tuple[AgreementSurfaceEdge, ...]:
    """
    Detect broken plural treating as feminine singular in agreement.

    الكتب كثيرة → broken plural + feminine singular adjective
    """
    # Placeholder for Phase 4 implementation
    return ()


# ============================================================================
# Transition Function (U₇-B → U₇-C)
# ============================================================================

def transition_u7b_to_u7c(
    u7b_layer: InflectionalSurfaceContractLayerObject
) -> ClauseSurfaceAgreementLayerObject:
    """
    Transition from U₇-B (WordSurfaceGuard) to U₇-C (ClauseSurfaceAgreement).

    This is the minimal transition function for Phase 2.
    Full implementation will be in Phase 4.
    """
    # Phase 2: Minimal pass-through with structure creation
    u7c_units = []

    for u7b_unit in u7b_layer.units:
        u7c_unit = ClauseSurfaceAgreementUnit(
            uid=str(uuid4()),
            surface=u7b_unit.surface,
            source_u7b_unit_id=u7b_unit.uid,
            source_u7b_trace=u7b_unit.trace,
            protected_core=u7b_unit.protected_core,
            root_input=u7b_unit.root_input,
            root_input_permission=u7b_unit.root_input_permission,
            broken_plural_guard=None,  # Will be implemented in Phase 3
            transitivity_potential=None,  # Will be implemented in Phase 5
            weak_radical_risk_vector=None,  # Will be implemented in Phase 5
            agreement_edges=(),  # Will be detected in Phase 4
            rationality_surface_hint=RationalityHint.UNRESOLVED,
            gender_surface_hint=GenderSurfaceHint.UNRESOLVED,
            number_surface_hint=NumberSurfaceHint.UNRESOLVED,
            permission_elevated_by_agreement=False,
            permission_elevation_evidence=None,
            residuals=u7b_unit.residuals,
            rank=u7b_unit.rank,
            trace=u7b_unit.trace,
        )
        u7c_units.append(u7c_unit)

    # Phase 2: No agreement detection yet
    agreement_edges = ()  # Will be implemented in Phase 4
    agreement_candidates = ()  # Will be implemented in Phase 4
    broken_plural_guards = ()  # Will be implemented in Phase 3

    layer = ClauseSurfaceAgreementLayerObject(
        uid=str(uuid4()),
        units=tuple(u7c_units),
        agreement_edges=agreement_edges,
        agreement_candidates=agreement_candidates,
        broken_plural_guards=broken_plural_guards,
        source_u7b_layer_id=u7b_layer.uid,
        trace_7b=u7b_layer.trace_7a,
        residuals=u7b_layer.residuals,
        rank=u7b_layer.rank,
        proof=None,
    )

    return layer
