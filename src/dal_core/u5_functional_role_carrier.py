"""
U₅ Functional Role Carrier (حامل الأدوار الوظيفية)

Domain: U₅ = FunctionalRoleCarrier
Purpose: Assign functional role CANDIDATES after true lafẓ identification
Transition: U₄ (TrueSingularLafẓ) → U₅ (FunctionalRole) → U₆ (MabniClosedClass)

Critical Laws (Axioms):
    - Axiom 5.1: لا دور وظيفي قبل لفظ حقيقي (No functional role before true lafẓ)
    - Axiom 5.2: الدور ≠ الجذر (Role ≠ root)
    - Axiom 5.3: الدور ≠ الوزن (Role ≠ weight)
    - Axiom 5.4: الدور ≠ المعنى (Role ≠ meaning)
    - Axiom 5.5: الدور ≠ الحكم (Role ≠ hukm)
    - Axiom 5.6: الدور مرشح حتى يُحجب المنافسون (Role is candidate until competitors blocked)

Type System:
    FunctionalRole ≠ Root
    FunctionalRole ≠ Weight
    FunctionalRole ≠ Meaning
    FunctionalRole ≠ Hukm
    FunctionalRole ≠ Certificate (until evidence blocks competitors)

Architecture:
    U₄ (TrueLafẓLayerObject) → CPB₅ → U₅ (FunctionalRoleLayerObject) → CPB₆ → MabniClosedClass

Key Principle:
    U₅ reads U₄ surface potentials and opens functional role paths.
    U₅ does NOT certify roles; certification requires evidence-based competitor blocking.

Example Analysis:
    From U₄ units [وَ, بِ, كِتَاب, ـهِمْ]:
        - وَ → HARF_ATF_CANDIDATE (conjunction candidate)
        - بِ → HARF_JARR_CANDIDATE (preposition candidate)
        - كِتَاب → NOUN_CANDIDATE (may also be VERBAL_NOUN_CANDIDATE)
        - ـهِمْ → ATTACHED_PRONOUN_CANDIDATE (3mp genitive pronoun)

U₅ Output:
    Gives U₆:
        - Role candidates (verb, noun, particle, pronoun)
        - Downstream path hints
        - Residuals (ambiguities, deferred decisions)
        - Rank (zero → candidate → hypothesis → certificate)

U₅ Does NOT Give:
    - Root extraction (U₈)
    - Weight/pattern determination (U₉)
    - Meaning/semantic interpretation (U₁₅)
    - Final grammatical hukm (U₇+)

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
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
from dal_core.u4_true_singular_lafz_carrier import (
    TrueLafzLayerObject,
    TrueLafzUnit,
    TrueLafzUnitType,
    TerminalProfile,
    DefinitenessSurfacePotential,
    QuantitySurfacePotential,
    VerbSurfacePotential,
    DownstreamPathHints
)


# ============================================================================
# Role Type Taxonomy (Multi-Sorted Role Algebra)
# ============================================================================

class RoleSort(Enum):
    """
    Role sort categories for multi-sorted algebra.

    Each role belongs to exactly one sort, preventing category mixing.
    """
    CLOSED_CLASS = "closed_class"        # Particles, prepositions, etc.
    PRONOUN = "pronoun"                  # Personal, attached, detached
    VERB_CANDIDATE = "verb_candidate"    # Verb surface candidates
    NOUN_CANDIDATE = "noun_candidate"    # Noun surface candidates
    OPERATOR_CANDIDATE = "operator_candidate"  # Operator/operand patterns
    REFERENCE_CANDIDATE = "reference_candidate"  # Reference carriers
    QUANTITY_CANDIDATE = "quantity_candidate"    # Number/quantity patterns
    RESIDUAL = "residual"                # Unresolved, deferred


# ============================================================================
# Functional Role Candidates (Closed Class)
# ============================================================================

class ClosedClassRoleCandidate(Enum):
    """
    Closed-class functional role candidates.

    These are CANDIDATES, not certificates.
    Certification requires lexicon match + evidence.
    """
    HARF_JARR_CANDIDATE = "حرف جر محتمل"              # Preposition candidate
    HARF_ATF_CANDIDATE = "حرف عطف محتمل"              # Conjunction candidate
    HARF_NASB_CANDIDATE = "حرف نصب محتمل"             # Accusative particle candidate
    HARF_JAZM_CANDIDATE = "حرف جزم محتمل"             # Jussive particle candidate
    HARF_TAWKID_CANDIDATE = "حرف توكيد محتمل"         # Emphasis particle candidate
    HARF_NAFY_CANDIDATE = "حرف نفي محتمل"             # Negation candidate
    HARF_ISTIFHAM_CANDIDATE = "حرف استفهام محتمل"    # Interrogative candidate
    HARF_SHART_CANDIDATE = "حرف شرط محتمل"            # Conditional candidate
    HARF_NIDA_CANDIDATE = "حرف نداء محتمل"            # Vocative candidate
    PARTICLE_CANDIDATE = "أداة محتملة"                # Generic particle candidate


# ============================================================================
# Pronoun Role Candidates
# ============================================================================

class PronounRoleCandidate(Enum):
    """
    Pronoun role candidates.

    These are surface-based candidates, NOT resolved reference.
    """
    ATTACHED_PRONOUN_CANDIDATE = "ضمير متصل محتمل"
    DETACHED_PRONOUN_CANDIDATE = "ضمير منفصل محتمل"
    SUBJECT_PRONOUN_CANDIDATE = "ضمير رفع محتمل"
    OBJECT_PRONOUN_CANDIDATE = "ضمير نصب محتمل"
    POSSESSIVE_PRONOUN_CANDIDATE = "ضمير ملكية محتمل"
    GENITIVE_PRONOUN_CANDIDATE = "ضمير جر محتمل"


# ============================================================================
# Verb Role Candidates (Surface-Based)
# ============================================================================

class VerbRoleCandidate(Enum):
    """
    Verb surface role candidates.

    Based on U₄ verb surface potentials.
    These are NOT tense certificates.
    """
    PAST_VERB_SURFACE_CANDIDATE = "فعل ماض سطحي محتمل"
    PRESENT_VERB_SURFACE_CANDIDATE = "فعل مضارع سطحي محتمل"
    IMPERATIVE_VERB_SURFACE_CANDIDATE = "فعل أمر سطحي محتمل"
    VERBAL_NOUN_CANDIDATE = "مصدر محتمل"
    ACTIVE_PARTICIPLE_CANDIDATE = "اسم فاعل محتمل"
    PASSIVE_PARTICIPLE_CANDIDATE = "اسم مفعول محتمل"
    VERB_SURFACE_CANDIDATE = "مرشح فعلي سطحي"


# ============================================================================
# Noun Role Candidates (Surface-Based)
# ============================================================================

class NounRoleCandidate(Enum):
    """
    Noun surface role candidates.

    Based on U₄ surface hints (definiteness, quantity, terminal patterns).
    These are NOT semantic categories.
    """
    NOUN_SURFACE_CANDIDATE = "اسم سطحي محتمل"
    DEFINITE_NOUN_CANDIDATE = "اسم معرف سطحي محتمل"
    INDEFINITE_NOUN_CANDIDATE = "اسم نكرة سطحي محتمل"
    DUAL_NOUN_CANDIDATE = "مثنى سطحي محتمل"
    PLURAL_NOUN_CANDIDATE = "جمع سطحي محتمل"
    SINGULAR_NOUN_CANDIDATE = "مفرد سطحي محتمل"


# ============================================================================
# Operator/Operand Role Candidates
# ============================================================================

class OperatorRoleCandidate(Enum):
    """
    Operator/operand role candidates.

    These indicate potential operator-operand relationships.
    NOT grammatical case assignment.
    """
    OPERATOR_CANDIDATE = "عامل محتمل"
    OPERAND_CANDIDATE = "معمول محتمل"
    GOVERNOR_CANDIDATE = "حاكم محتمل"
    GOVERNED_CANDIDATE = "محكوم محتمل"


# ============================================================================
# Reference Role Candidates
# ============================================================================

class ReferenceRoleCandidate(Enum):
    """
    Reference carrier candidates.

    Based on U₄ definiteness and pronoun surface hints.
    NOT resolved reference (that's U₁₅).
    """
    REFERENCE_CARRIER_CANDIDATE = "حامل إحالة محتمل"
    DEFINITE_REFERENCE_CANDIDATE = "محدد بالإحالة محتمل"
    PRONOUN_REFERENCE_CANDIDATE = "إحالة ضميرية محتملة"


# ============================================================================
# Quantity Role Candidates
# ============================================================================

class QuantityRoleCandidate(Enum):
    """
    Quantity pattern candidates.

    Based on U₄ quantity surface hints.
    NOT counted reality (that's U₁₅).
    """
    NUMBER_WORD_CANDIDATE = "رقم لفظي محتمل"
    COUNTED_OBJECT_CANDIDATE = "معدود محتمل"
    DUAL_QUANTITY_CANDIDATE = "تثنية كمية محتملة"
    PLURAL_QUANTITY_CANDIDATE = "جمع كمي محتمل"


# ============================================================================
# Failure Types
# ============================================================================

class FunctionalRoleFailureType(Enum):
    """Failure types for functional role assignment."""
    NO_LAFZ_UNITS = "no_lafz_units"
    CONFLICTING_HINTS = "conflicting_hints"
    INSUFFICIENT_POTENTIALS = "insufficient_potentials"
    INVALID_INPUT_LAYER = "invalid_input_layer"


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class FunctionalRoleCandidate:
    """
    A single functional role candidate for a lafẓ unit.

    This represents a CANDIDATE role, not a certified role.
    Roles become certificates only when competitors are blocked by evidence.

    Forbidden fields:
        - root (that's U₈)
        - weight (that's U₉)
        - meaning (that's U₁₅)
        - hukm (that's U₇+)
    """
    uid: str
    role: Enum  # One of the role candidate enums above
    sort: RoleSort
    confidence: float  # [0.0, 1.0]
    evidence: Tuple[str, ...]  # Why this role candidate
    source_u4_unit_id: str  # Trace to U₄ lafẓ unit
    residuals: FrozenSet[Residual]
    rank: Rank

    def __post_init__(self):
        """Validate role candidate."""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")

        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("FunctionalRoleCandidate MUST NOT contain 'root' field (Axiom 5.2)")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("FunctionalRoleCandidate MUST NOT contain 'weight' field (Axiom 5.3)")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("FunctionalRoleCandidate MUST NOT contain 'meaning' field (Axiom 5.4)")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("FunctionalRoleCandidate MUST NOT contain 'hukm' field (Axiom 5.5)")


@dataclass(frozen=True)
class FunctionalRoleUnit:
    """
    U₅ functional role assignment for a lafẓ unit.

    Contains multiple competing role candidates.
    Candidates are NOT mutually exclusive until evidence blocks competitors.

    Example:
        بِ may simultaneously be:
            - HARF_JARR_CANDIDATE (preposition)
            - (Future layers may add: ROOT_RADICAL_CANDIDATE)
    """
    uid: str
    surface: str  # Orthographic surface from U₄
    source_lafz_unit_id: str  # Trace to U₄ lafẓ unit
    trace_4: Tuple[str, ...]  # Ordered trace to U₄
    role_candidates: Tuple[FunctionalRoleCandidate, ...]  # Competing candidates
    evidence: Tuple[str, ...]  # Evidence for role opening
    residuals: FrozenSet[Residual]
    rank: Rank


@dataclass(frozen=True)
class FunctionalRoleLayerObject:
    """
    U₅ layer object containing functional role candidates.

    Represents role candidacy based on U₄ surface potentials.
    """
    uid: str
    units: Tuple[FunctionalRoleUnit, ...]  # Role-assigned units
    source_lafz_layer_id: str  # Trace to U₄ layer
    trace_4: Tuple[str, ...]  # Ordered trace to U₄
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None


@dataclass(frozen=True)
class FunctionalRoleResult:
    """Result of functional role assignment."""
    success: bool
    layer_object: Optional[FunctionalRoleLayerObject]
    failure_type: Optional[FunctionalRoleFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₅ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB5:
    """
    CPB₅: Completeness Predicate and Proof Builder for FunctionalRole layer.

    Guards:
        - Role candidates identified
        - Lafẓ trace preserved
        - No forbidden fields (root, weight, meaning, hukm)
        - Allowed next gate: U₆ MabniClosedClass
    """

    @staticmethod
    def is_complete(layer_obj: FunctionalRoleLayerObject) -> bool:
        """Check if functional role layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_lafz_layer_id:
            return False

        # Check no forbidden fields in role candidates
        for unit in layer_obj.units:
            for candidate in unit.role_candidates:
                if (hasattr(candidate, 'root') or hasattr(candidate, 'weight') or
                    hasattr(candidate, 'meaning') or hasattr(candidate, 'hukm')):
                    return False

        return True

    @staticmethod
    def build_proof(layer_obj: FunctionalRoleLayerObject) -> ProofObject:
        """Build proof object for functional role layer."""
        return make_proof_object(
            claim="U₅ functional role candidates determined",
            scope="U5_FUNCTIONAL_ROLE",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"trace_preserved={bool(layer_obj.source_lafz_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"mabni_closed_class_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
            limitations=frozenset([
                "no_root_extraction",
                "no_weight_determination",
                "no_meaning_assignment",
                "no_hukm_judgment",
                "candidates_not_certificates",
            ]),
        )


# ============================================================================
# Role Candidate Builders (Using U₄ Potentials)
# ============================================================================

def _build_closed_class_candidates(
    lafz_unit: TrueLafzUnit
) -> List[FunctionalRoleCandidate]:
    """
    Build closed-class role candidates from lafẓ unit.

    Uses U₄ unit_type to determine if unit is likely a particle.

    Args:
        lafz_unit: U₄ lafẓ unit

    Returns:
        List of closed-class role candidates
    """
    candidates = []

    # Check if unit is a proclitic (likely particle)
    if lafz_unit.unit_type == TrueLafzUnitType.BOUND_PROCLITIC:
        surface = lafz_unit.surface

        # Determine likely particle type from surface
        if surface in ["بِ", "بِـ"]:
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=ClosedClassRoleCandidate.HARF_JARR_CANDIDATE,
                sort=RoleSort.CLOSED_CLASS,
                confidence=0.8,
                evidence=("surface_match_preposition", f"surface={surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))
        elif surface in ["لِ", "لِـ"]:
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=ClosedClassRoleCandidate.HARF_JARR_CANDIDATE,
                sort=RoleSort.CLOSED_CLASS,
                confidence=0.8,
                evidence=("surface_match_preposition", f"surface={surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))
        elif surface in ["وَ", "فَ"]:
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=ClosedClassRoleCandidate.HARF_ATF_CANDIDATE,
                sort=RoleSort.CLOSED_CLASS,
                confidence=0.9,
                evidence=("surface_match_conjunction", f"surface={surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))
        else:
            # Generic particle candidate
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=ClosedClassRoleCandidate.PARTICLE_CANDIDATE,
                sort=RoleSort.CLOSED_CLASS,
                confidence=0.5,
                evidence=("bound_proclitic_type",),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset([make_warning("particle_type_unresolved", "Particle type needs lexicon match")]),
                rank=Rank.CANDIDATE
            ))

    return candidates


def _build_pronoun_candidates(
    lafz_unit: TrueLafzUnit
) -> List[FunctionalRoleCandidate]:
    """
    Build pronoun role candidates from lafẓ unit.

    Uses U₄ unit_type to determine if unit is a pronoun.

    Args:
        lafz_unit: U₄ lafẓ unit

    Returns:
        List of pronoun role candidates
    """
    candidates = []

    # Check if unit is attached pronoun
    if lafz_unit.unit_type == TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE:
        candidates.append(FunctionalRoleCandidate(
            uid=str(uuid4()),
            role=PronounRoleCandidate.ATTACHED_PRONOUN_CANDIDATE,
            sort=RoleSort.PRONOUN,
            confidence=0.9,
            evidence=("u4_attached_pronoun_type",),
            source_u4_unit_id=lafz_unit.uid,
            residuals=frozenset(),
            rank=Rank.CANDIDATE
        ))

        # Also add more specific pronoun types based on surface
        surface = lafz_unit.surface
        if "هِمْ" in surface or "هُمْ" in surface:
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=PronounRoleCandidate.GENITIVE_PRONOUN_CANDIDATE,
                sort=RoleSort.PRONOUN,
                confidence=0.7,
                evidence=("surface_pattern_3mp_genitive", f"surface={surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset([make_warning("genitive_vs_possessive", "Needs context to disambiguate")]),
                rank=Rank.CANDIDATE
            ))

    return candidates


def _build_verb_candidates(
    lafz_unit: TrueLafzUnit,
    verb_potential: Optional[VerbSurfacePotential]
) -> List[FunctionalRoleCandidate]:
    """
    Build verb role candidates from U₄ verb surface potential.

    Args:
        lafz_unit: U₄ lafẓ unit
        verb_potential: U₄ verb surface potential

    Returns:
        List of verb role candidates
    """
    candidates = []

    if not verb_potential:
        return candidates

    # Check if verb hint is possible
    if verb_potential.verb_surface_hint == "possible":
        # General verb candidate
        candidates.append(FunctionalRoleCandidate(
            uid=str(uuid4()),
            role=VerbRoleCandidate.VERB_SURFACE_CANDIDATE,
            sort=RoleSort.VERB_CANDIDATE,
            confidence=0.6,
            evidence=("u4_verb_surface_hint_possible",),
            source_u4_unit_id=lafz_unit.uid,
            residuals=frozenset(),
            rank=Rank.CANDIDATE
        ))

        # Past verb candidate
        if verb_potential.past_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=VerbRoleCandidate.PAST_VERB_SURFACE_CANDIDATE,
                sort=RoleSort.VERB_CANDIDATE,
                confidence=0.7,
                evidence=("u4_past_surface_hint_possible",),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

        # Present verb candidate
        if verb_potential.present_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=VerbRoleCandidate.PRESENT_VERB_SURFACE_CANDIDATE,
                sort=RoleSort.VERB_CANDIDATE,
                confidence=0.7,
                evidence=("u4_present_surface_hint_possible", f"has_prefix={verb_potential.has_present_prefix_surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

        # Imperative candidate
        if verb_potential.imperative_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=VerbRoleCandidate.IMPERATIVE_VERB_SURFACE_CANDIDATE,
                sort=RoleSort.VERB_CANDIDATE,
                confidence=0.5,
                evidence=("u4_imperative_surface_hint_possible",),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset([make_warning("imperative_needs_context", "Imperative requires context")]),
                rank=Rank.CANDIDATE
            ))

    return candidates


def _build_noun_candidates(
    lafz_unit: TrueLafzUnit,
    definiteness_potential: Optional[DefinitenessSurfacePotential],
    quantity_potential: Optional[QuantitySurfacePotential],
    verb_potential: Optional[VerbSurfacePotential]
) -> List[FunctionalRoleCandidate]:
    """
    Build noun role candidates from U₄ surface potentials.

    Args:
        lafz_unit: U₄ lafẓ unit
        definiteness_potential: U₄ definiteness surface potential
        quantity_potential: U₄ quantity surface potential
        verb_potential: U₄ verb surface potential

    Returns:
        List of noun role candidates
    """
    candidates = []

    # Only assign noun candidates to core units
    if lafz_unit.unit_type != TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE:
        return candidates

    # Check if verb hint is NOT likely (if unlikely or unresolved, consider noun)
    verb_unlikely = not verb_potential or verb_potential.verb_surface_hint != "possible"

    if verb_unlikely:
        # General noun candidate
        candidates.append(FunctionalRoleCandidate(
            uid=str(uuid4()),
            role=NounRoleCandidate.NOUN_SURFACE_CANDIDATE,
            sort=RoleSort.NOUN_CANDIDATE,
            confidence=0.6,
            evidence=("core_candidate", "verb_unlikely"),
            source_u4_unit_id=lafz_unit.uid,
            residuals=frozenset(),
            rank=Rank.CANDIDATE
        ))

    # Definiteness-based candidates
    if definiteness_potential:
        if definiteness_potential.definite_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=NounRoleCandidate.DEFINITE_NOUN_CANDIDATE,
                sort=RoleSort.NOUN_CANDIDATE,
                confidence=0.7,
                evidence=("u4_definite_surface_hint_possible", f"has_al={definiteness_potential.has_al_surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

        if definiteness_potential.indefinite_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=NounRoleCandidate.INDEFINITE_NOUN_CANDIDATE,
                sort=RoleSort.NOUN_CANDIDATE,
                confidence=0.7,
                evidence=("u4_indefinite_surface_hint_possible", f"has_tanwin={definiteness_potential.has_tanwin_surface}"),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

    # Quantity-based candidates
    if quantity_potential:
        if quantity_potential.dual_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=NounRoleCandidate.DUAL_NOUN_CANDIDATE,
                sort=RoleSort.NOUN_CANDIDATE,
                confidence=0.8,
                evidence=("u4_dual_surface_hint_possible",),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

        if quantity_potential.plural_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=NounRoleCandidate.PLURAL_NOUN_CANDIDATE,
                sort=RoleSort.NOUN_CANDIDATE,
                confidence=0.8,
                evidence=("u4_plural_surface_hint_possible",),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

        if quantity_potential.singular_surface_hint == "possible":
            candidates.append(FunctionalRoleCandidate(
                uid=str(uuid4()),
                role=NounRoleCandidate.SINGULAR_NOUN_CANDIDATE,
                sort=RoleSort.NOUN_CANDIDATE,
                confidence=0.6,
                evidence=("u4_singular_surface_hint_possible",),
                source_u4_unit_id=lafz_unit.uid,
                residuals=frozenset(),
                rank=Rank.CANDIDATE
            ))

    return candidates


# ============================================================================
# Functional Role Operations
# ============================================================================

def functional_role_5(lafz_layer: TrueLafzLayerObject) -> FunctionalRoleResult:
    """
    Assign functional role candidates from U₄ true lafẓ layer.

    Critical Examples:
        كَتَبَ → PAST_VERB_SURFACE_CANDIDATE + NOUN_SURFACE_CANDIDATE
        بِكِتَابٍ → بِ (HARF_JARR_CANDIDATE) + كِتَابٍ (INDEFINITE_NOUN_CANDIDATE)
        وَبِكِتَابِهِمْ → وَ (HARF_ATF_CANDIDATE) + بِ (HARF_JARR_CANDIDATE) +
                        كِتَابِ (DEFINITE_NOUN_CANDIDATE) + ـهِمْ (ATTACHED_PRONOUN_CANDIDATE)

    Args:
        lafz_layer: U₄ layer object with lafẓ eligibility units

    Returns:
        FunctionalRoleResult with role candidates

    Forbidden:
        - Direct jump to Root (U₈)
        - Direct jump to Weight (U₉)
        - Direct jump to Meaning (U₁₅)
        - Direct jump to Hukm (U₇+)
    """
    # Validate input
    if not lafz_layer.units:
        return FunctionalRoleResult(
            success=False,
            layer_object=None,
            failure_type=FunctionalRoleFailureType.NO_LAFZ_UNITS,
            message="No lafẓ units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot assign functional roles without lafẓ units")])
        )

    # Build functional role units
    role_units = []
    all_residuals = []

    for lafz_unit in lafz_layer.units:
        # Collect all role candidates for this unit
        all_candidates = []

        # 1. Closed-class candidates (particles)
        all_candidates.extend(_build_closed_class_candidates(lafz_unit))

        # 2. Pronoun candidates
        all_candidates.extend(_build_pronoun_candidates(lafz_unit))

        # 3. Verb candidates (from U₄ verb potential)
        all_candidates.extend(_build_verb_candidates(
            lafz_unit,
            lafz_unit.verb_surface_potential
        ))

        # 4. Noun candidates (from U₄ definiteness + quantity potentials)
        all_candidates.extend(_build_noun_candidates(
            lafz_unit,
            lafz_unit.definiteness_surface_potential,
            lafz_unit.quantity_surface_potential,
            lafz_unit.verb_surface_potential
        ))

        # Build evidence
        evidence_items = [
            f"u4_unit_type={lafz_unit.unit_type.value}",
            f"candidates_count={len(all_candidates)}",
        ]

        # Create FunctionalRoleUnit
        role_unit = FunctionalRoleUnit(
            uid=str(uuid4()),
            surface=lafz_unit.surface,
            source_lafz_unit_id=lafz_unit.uid,
            trace_4=(lafz_layer.uid,),
            role_candidates=tuple(all_candidates),
            evidence=tuple(evidence_items),
            residuals=lafz_unit.residuals,  # Preserve residuals from U₄
            rank=lafz_unit.rank
        )
        role_units.append(role_unit)
        all_residuals.extend(list(lafz_unit.residuals))

    # Build layer object
    layer_obj = FunctionalRoleLayerObject(
        uid=str(uuid4()),
        units=tuple(role_units),
        source_lafz_layer_id=lafz_layer.uid,
        trace_4=(lafz_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=lafz_layer.rank,  # Inherit rank from U₄
        proof=None
    )

    # Build proof
    proof = CPB5.build_proof(layer_obj)
    layer_obj = FunctionalRoleLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_lafz_layer_id=layer_obj.source_lafz_layer_id,
        trace_4=layer_obj.trace_4,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return FunctionalRoleResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"Functional role candidates assigned: {len(role_units)} units processed",
        residuals=layer_obj.residuals
    )


# ============================================================================
# Backward Compatibility Exports
# ============================================================================

# Export enums for backward compatibility
__all__ = [
    # Core types
    'RoleSort',
    'ClosedClassRoleCandidate',
    'PronounRoleCandidate',
    'VerbRoleCandidate',
    'NounRoleCandidate',
    'OperatorRoleCandidate',
    'ReferenceRoleCandidate',
    'QuantityRoleCandidate',

    # Structures
    'FunctionalRoleCandidate',
    'FunctionalRoleUnit',
    'FunctionalRoleLayerObject',
    'FunctionalRoleResult',

    # Failures
    'FunctionalRoleFailureType',

    # CPB
    'CPB5',

    # Operations
    'functional_role_5',
]
