"""
U₆ Mabni Closed Class Carrier (حامل المبنيات والأدوات المغلقة)

Domain: U₆ = MabniClosedClassCarrier
Purpose: Identify closed-class mabni candidates WITHOUT semantic or syntactic judgment
Transition: U₅ (FunctionalRole) → U₆ (MabniClosedClass) → U₇ (PreWeightContract)

Critical Laws (Axioms):
    - Axiom 6.1: لا مغلق قبل دور وظيفي (No closed-class before functional role)
    - Axiom 6.2: المبني ≠ المعنى (Mabni ≠ meaning)
    - Axiom 6.3: المبني ≠ الحكم (Mabni ≠ hukm)
    - Axiom 6.4: المبني ≠ الجذر (Mabni ≠ root)
    - Axiom 6.5: المبني ≠ الوزن (Mabni ≠ weight)
    - Axiom 6.6: إثبات الأداة ≠ تحليل الإحالة (Tool identity ≠ reference resolution)

Type System:
    MabniClosedClass ≠ Root
    MabniClosedClass ≠ Weight
    MabniClosedClass ≠ Meaning
    MabniClosedClass ≠ Hukm
    MabniClosedClass ≠ ResolvedReference
    MabniClosedClass ≠ Certificate (until evidence blocks open-class path)

Architecture:
    U₅ (FunctionalRoleLayerObject) → CPB₆ → U₆ (MabniClosedClassLayerObject) → CPB₇ → PreWeightContract

Key Principle:
    U₆ reads U₅ functional role candidates and identifies closed-class mabni status.
    U₆ does NOT certify final meaning, reference, or grammatical status.

Example Analysis:
    From U₅ units [وَ, بِ, كِتَاب, ـهِمْ]:
        - وَ → CLOSED_CLASS_MABNI_CANDIDATE (HARF_ATF)
        - بِ → CLOSED_CLASS_MABNI_CANDIDATE (HARF_JARR)
        - كِتَاب → OPEN_CLASS_CORE (remains open for U₇+ root/weight)
        - ـهِمْ → CLOSED_CLASS_MABNI_CANDIDATE (ATTACHED_PRONOUN)

U₆ Output:
    Gives U₇:
        - Mabni closed-class candidates (particles, pronouns)
        - Open-class cores (for root/weight extraction)
        - Path blocking (closed-class units don't go to root extraction)
        - Residuals (ambiguities, lexicon misses)
        - Rank (zero → candidate → hypothesis → certificate)

U₆ Does NOT Give:
    - Root extraction (U₈)
    - Weight/pattern determination (U₉)
    - Meaning/semantic interpretation (U₁₅)
    - Reference resolution (U₁₅)
    - Grammatical hukm (U₇+)

PR: U6-MABNI-CLOSED-CLASS
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
from dal_core.u5_functional_role_carrier import (
    FunctionalRoleLayerObject,
    FunctionalRoleUnit,
    FunctionalRoleCandidate,
    RoleSort,
    ClosedClassRoleCandidate,
    PronounRoleCandidate
)
from dal_core.mabni_registry import (
    MabniRegistry,
    MabniEntry,
    MabniCategory,
    get_default_mabni_registry
)


# ============================================================================
# Type System - Mabni Closed Class Classification
# ============================================================================

class MabniClosedClassType(Enum):
    """
    Classification of functional role units into mabni/open-class categories.

    This is LEXICAL classification, not semantic or grammatical judgment.
    U₆ determines if unit is closed-class mabni, NOT its meaning or i'rab.
    """
    CLOSED_CLASS_MABNI_CANDIDATE = "closed_class_mabni_candidate"      # مبني أداة مغلقة
    ATTACHED_PRONOUN_CLOSED_CLASS = "attached_pronoun_closed_class"    # ضمير متصل مبني
    DETACHED_PRONOUN_CLOSED_CLASS = "detached_pronoun_closed_class"    # ضمير منفصل مبني
    OPEN_CLASS_CORE_CANDIDATE = "open_class_core_candidate"            # نواة مفتوحة (للجذر/الوزن)
    LEXICON_AMBIGUOUS = "lexicon_ambiguous"                            # مبهم معجمي
    BLOCKED = "blocked"                                                 # محظور


class ClosedClassSubtype(Enum):
    """
    Closed-class subtypes based on MabniRegistry categories.

    These are lexicon-based identifications, NOT grammatical assignments.
    """
    HARF_JARR = "حرف جر"                      # Preposition
    HARF_ATF = "حرف عطف"                      # Conjunction
    HARF_NASB = "حرف نصب"                     # Accusative particle
    HARF_JAZM = "حرف جزم"                     # Jussive particle
    HARF_TAWKID = "حرف توكيد"                 # Emphasis particle
    HARF_NAFY = "حرف نفي"                     # Negation particle
    HARF_ISTIFHAM = "حرف استفهام"            # Interrogative particle
    HARF_SHART = "حرف شرط"                    # Conditional particle
    HARF_NIDA = "حرف نداء"                    # Vocative particle
    FUTURE_MARKER = "أداة استقبال"           # Future marker (سَ، سَوْفَ)
    PRONOUN_ATTACHED = "ضمير متصل"           # Attached pronoun
    PRONOUN_DETACHED = "ضمير منفصل"          # Detached pronoun
    DEMONSTRATIVE = "اسم إشارة"              # Demonstrative
    RELATIVE = "اسم موصول"                   # Relative noun
    INTERROGATIVE_NOUN = "اسم استفهام"       # Interrogative noun
    CONDITIONAL_NOUN = "اسم شرط"             # Conditional noun
    ADVERB_MABNI = "ظرف مبني"                # Indeclinable adverb
    NAME_OF_VERB = "اسم فعل"                 # Name of verb
    COMPOUND_NUMBER = "عدد مركب"             # Compound number (11-19)
    GENERIC_PARTICLE = "أداة عامة"           # Generic particle


# ============================================================================
# Failure Types
# ============================================================================

class MabniClosedClassFailureType(Enum):
    """Failure types for mabni closed-class determination."""
    NO_FUNCTIONAL_ROLE_UNITS = "no_functional_role_units"
    LEXICON_NOT_AVAILABLE = "lexicon_not_available"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    INVALID_INPUT_LAYER = "invalid_input_layer"


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class MabniClosedClassCandidate:
    """
    A single mabni closed-class candidate for a functional role unit.

    This represents lexicon-based identification, NOT semantic assignment.
    Candidates become certificates only when open-class path is blocked by evidence.

    Forbidden fields:
        - root (that's U₈)
        - weight (that's U₉)
        - meaning (that's U₁₅)
        - hukm (that's U₇+)
        - resolved_reference (that's U₁₅)
    """
    uid: str
    mabni_type: MabniClosedClassType
    subtype: Optional[ClosedClassSubtype]  # Only for closed-class
    lexicon_support: float  # [0.0, 1.0] - Lexicon match strength, NOT semantic certainty
    evidence: Tuple[str, ...]  # Why this classification
    source_u5_unit_id: str  # Trace to U₅ functional role unit
    mabni_entry: Optional[MabniEntry]  # Reference to MabniRegistry entry if matched
    residuals: FrozenSet[Residual]
    rank: Rank

    def __post_init__(self):
        """Validate mabni closed-class candidate."""
        if not (0.0 <= self.lexicon_support <= 1.0):
            raise ValueError(f"Lexicon support must be in [0.0, 1.0], got {self.lexicon_support}")

        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("MabniClosedClassCandidate MUST NOT contain 'root' field (Axiom 6.4)")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("MabniClosedClassCandidate MUST NOT contain 'weight' field (Axiom 6.5)")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("MabniClosedClassCandidate MUST NOT contain 'meaning' field (Axiom 6.2)")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("MabniClosedClassCandidate MUST NOT contain 'hukm' field (Axiom 6.3)")

        # No resolved_reference field allowed
        if hasattr(self, 'resolved_reference'):
            raise ValueError("MabniClosedClassCandidate MUST NOT contain 'resolved_reference' field (Axiom 6.6)")


@dataclass(frozen=True)
class MabniClosedClassUnit:
    """
    U₆ mabni closed-class classification for a functional role unit.

    Contains classification and path blocking information.
    Closed-class units do NOT proceed to root/weight extraction.

    Example:
        بِ may be:
            - CLOSED_CLASS_MABNI_CANDIDATE (blocks root path)
            - (Future layers certify it as preposition with evidence)
    """
    uid: str
    surface: str  # Orthographic surface from U₅
    source_functional_role_unit_id: str  # Trace to U₅ functional role unit
    trace_5: Tuple[str, ...]  # Ordered trace to U₅
    mabni_classification: MabniClosedClassCandidate  # Primary classification
    blocked_paths: Tuple[str, ...]  # Paths blocked by this classification
    evidence: Tuple[str, ...]  # Evidence for classification
    residuals: FrozenSet[Residual]
    rank: Rank

    def __post_init__(self):
        """Validate mabni closed-class unit."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("MabniClosedClassUnit MUST NOT contain 'root' field")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("MabniClosedClassUnit MUST NOT contain 'weight' field")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("MabniClosedClassUnit MUST NOT contain 'meaning' field")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("MabniClosedClassUnit MUST NOT contain 'hukm' field")


@dataclass(frozen=True)
class MabniClosedClassLayerObject:
    """
    U₆ layer object containing mabni closed-class classifications.

    Separates closed-class mabni units from open-class cores.
    """
    uid: str
    units: Tuple[MabniClosedClassUnit, ...]  # Classified units
    source_functional_role_layer_id: str  # Trace to U₅ layer
    trace_5: Tuple[str, ...]  # Ordered trace to U₅
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None

    def __post_init__(self):
        """Validate mabni closed-class layer object."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("MabniClosedClassLayerObject MUST NOT contain 'root' field")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("MabniClosedClassLayerObject MUST NOT contain 'weight' field")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("MabniClosedClassLayerObject MUST NOT contain 'meaning' field")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("MabniClosedClassLayerObject MUST NOT contain 'hukm' field")


@dataclass(frozen=True)
class MabniClosedClassResult:
    """Result of mabni closed-class determination."""
    success: bool
    layer_object: Optional[MabniClosedClassLayerObject]
    failure_type: Optional[MabniClosedClassFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₆ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB6:
    """
    CPB₆: Completeness Predicate and Proof Builder for MabniClosedClass layer.

    Guards:
        - Classifications identified
        - Functional role trace preserved
        - No forbidden fields (root, weight, meaning, hukm)
        - Allowed next gate: U₇ PreWeightContract
    """

    @staticmethod
    def is_complete(layer_obj: MabniClosedClassLayerObject) -> bool:
        """Check if mabni closed-class layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_functional_role_layer_id:
            return False

        # Check no forbidden fields
        for unit in layer_obj.units:
            if (hasattr(unit, 'root') or hasattr(unit, 'weight') or
                hasattr(unit, 'meaning') or hasattr(unit, 'hukm')):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: MabniClosedClassLayerObject) -> ProofObject:
        """Build proof object for mabni closed-class layer."""
        # Count closed-class vs open-class
        closed_count = sum(
            1 for u in layer_obj.units
            if u.mabni_classification.mabni_type in [
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
                MabniClosedClassType.DETACHED_PRONOUN_CLOSED_CLASS
            ]
        )
        open_count = sum(
            1 for u in layer_obj.units
            if u.mabni_classification.mabni_type == MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE
        )

        return make_proof_object(
            claim="U₆ mabni closed-class paths identified",
            scope="U6_MABNI_CLOSED_CLASS",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"closed_class_count={closed_count}",
                f"open_class_count={open_count}",
                f"trace_preserved={bool(layer_obj.source_functional_role_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"pre_weight_contract_gate"}),
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
                "closed_class_blocks_root_path",
                "open_class_requires_root_weight",
            ]),
        )


# ============================================================================
# Mabni Closed-Class Classification Logic
# ============================================================================

# Known simple particles (not in MabniRegistry but clearly closed-class)
KNOWN_SIMPLE_PARTICLES = {
    "وَ": ClosedClassSubtype.HARF_ATF,
    "فَ": ClosedClassSubtype.HARF_ATF,
    "بِ": ClosedClassSubtype.HARF_JARR,
    "بِـ": ClosedClassSubtype.HARF_JARR,
    "لِ": ClosedClassSubtype.HARF_JARR,
    "لِـ": ClosedClassSubtype.HARF_JARR,
    "كَ": ClosedClassSubtype.HARF_JARR,
    "كَـ": ClosedClassSubtype.HARF_JARR,
    "سَ": ClosedClassSubtype.FUTURE_MARKER,
    "سَـ": ClosedClassSubtype.FUTURE_MARKER,
}


def _lookup_mabni_registry(
    surface: str,
    registry: MabniRegistry
) -> Tuple[Optional[MabniEntry], float, List[str]]:
    """
    Lookup surface in MabniRegistry.

    Args:
        surface: Orthographic surface
        registry: MabniRegistry instance

    Returns:
        (best_entry, match_score, evidence_items)
    """
    entries = registry.lookup(surface)

    if not entries:
        return (None, 0.0, [])

    # If exactly one match, return it with high confidence
    if len(entries) == 1:
        return (entries[0], 0.9, [f"registry_match_unique={surface}"])

    # Multiple matches (e.g., مَنْ as interrogative/relative/conditional)
    # Return first match with lower confidence (ambiguity)
    return (entries[0], 0.7, [f"registry_match_ambiguous={surface}", f"competitors={len(entries)}"])


def _classify_from_u5_roles(
    func_role_unit: FunctionalRoleUnit,
    registry: MabniRegistry
) -> Tuple[MabniClosedClassType, Optional[ClosedClassSubtype], Optional[MabniEntry], float, List[str]]:
    """
    Classify functional role unit into mabni closed-class category.

    Decision tree:
    1. Check MabniRegistry for exact match
    2. Check KNOWN_SIMPLE_PARTICLES
    3. Check U₅ role candidates for closed-class hints
    4. Default to OPEN_CLASS_CORE_CANDIDATE if no closed-class evidence

    Args:
        func_role_unit: U₅ functional role unit
        registry: MabniRegistry instance

    Returns:
        (mabni_type, subtype, mabni_entry, lexicon_support, evidence)
    """
    surface = func_role_unit.surface
    evidence = []

    # 1. Check MabniRegistry
    mabni_entry, match_score, reg_evidence = _lookup_mabni_registry(surface, registry)
    if mabni_entry:
        # Map MabniCategory to ClosedClassSubtype
        category_map = {
            MabniCategory.PRONOUN_ATTACHED: (
                MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
                ClosedClassSubtype.PRONOUN_ATTACHED
            ),
            MabniCategory.PRONOUN_DETACHED: (
                MabniClosedClassType.DETACHED_PRONOUN_CLOSED_CLASS,
                ClosedClassSubtype.PRONOUN_DETACHED
            ),
            MabniCategory.DEMONSTRATIVE: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.DEMONSTRATIVE
            ),
            MabniCategory.RELATIVE: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.RELATIVE
            ),
            MabniCategory.INTERROGATIVE: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.INTERROGATIVE_NOUN
            ),
            MabniCategory.CONDITIONAL: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.CONDITIONAL_NOUN
            ),
            MabniCategory.ADVERB_MABNI: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.ADVERB_MABNI
            ),
            MabniCategory.NAME_OF_VERB: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.NAME_OF_VERB
            ),
            MabniCategory.COMPOUND_NUMBER: (
                MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
                ClosedClassSubtype.COMPOUND_NUMBER
            ),
        }

        mabni_type, subtype = category_map.get(
            mabni_entry.category,
            (MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE, None)
        )
        evidence.extend(reg_evidence)
        evidence.append(f"mabni_category={mabni_entry.category.value}")
        return (mabni_type, subtype, mabni_entry, match_score, evidence)

    # 2. Check KNOWN_SIMPLE_PARTICLES
    if surface in KNOWN_SIMPLE_PARTICLES:
        subtype = KNOWN_SIMPLE_PARTICLES[surface]
        evidence.append(f"known_particle={surface}")
        evidence.append(f"subtype={subtype.value}")
        return (
            MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
            subtype,
            None,
            0.9,
            evidence
        )

    # 3. Check U₅ role candidates for closed-class hints
    has_closed_class_role = False
    has_pronoun_role = False

    for candidate in func_role_unit.role_candidates:
        if candidate.sort == RoleSort.CLOSED_CLASS:
            has_closed_class_role = True
            evidence.append(f"u5_closed_class_role={candidate.role.value}")
        if candidate.sort == RoleSort.PRONOUN:
            has_pronoun_role = True
            evidence.append(f"u5_pronoun_role={candidate.role.value}")

    # If U₅ has pronoun role, classify as pronoun
    if has_pronoun_role:
        # Determine if attached or detached based on surface
        if surface.startswith("ـ") or surface in ["ـهُ", "ـهَا", "ـهِمْ", "ـهُمْ", "ـكَ", "ـكِ", "ـنَا"]:
            return (
                MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
                ClosedClassSubtype.PRONOUN_ATTACHED,
                None,
                0.7,
                evidence
            )
        else:
            return (
                MabniClosedClassType.DETACHED_PRONOUN_CLOSED_CLASS,
                ClosedClassSubtype.PRONOUN_DETACHED,
                None,
                0.7,
                evidence
            )

    # If U₅ has closed-class role, classify as closed-class
    if has_closed_class_role:
        # Try to infer subtype from U₅ role
        subtype = ClosedClassSubtype.GENERIC_PARTICLE
        for candidate in func_role_unit.role_candidates:
            if candidate.role == ClosedClassRoleCandidate.HARF_JARR_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_JARR
            elif candidate.role == ClosedClassRoleCandidate.HARF_ATF_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_ATF
            elif candidate.role == ClosedClassRoleCandidate.HARF_NASB_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_NASB
            elif candidate.role == ClosedClassRoleCandidate.HARF_JAZM_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_JAZM
            elif candidate.role == ClosedClassRoleCandidate.HARF_TAWKID_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_TAWKID
            elif candidate.role == ClosedClassRoleCandidate.HARF_NAFY_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_NAFY
            elif candidate.role == ClosedClassRoleCandidate.HARF_ISTIFHAM_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_ISTIFHAM
            elif candidate.role == ClosedClassRoleCandidate.HARF_SHART_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_SHART
            elif candidate.role == ClosedClassRoleCandidate.HARF_NIDA_CANDIDATE:
                subtype = ClosedClassSubtype.HARF_NIDA

        return (
            MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
            subtype,
            None,
            0.6,
            evidence
        )

    # 4. Default to OPEN_CLASS_CORE_CANDIDATE (for root/weight extraction)
    evidence.append("no_closed_class_evidence")
    evidence.append("default_to_open_class")
    return (
        MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE,
        None,
        None,
        0.8,
        evidence
    )


# ============================================================================
# Mabni Closed-Class Operations
# ============================================================================

def mabni_closed_class_6(
    functional_role_layer: FunctionalRoleLayerObject,
    registry: Optional[MabniRegistry] = None
) -> MabniClosedClassResult:
    """
    Identify mabni closed-class candidates from U₅ functional role layer.

    Critical Examples:
        وَ → CLOSED_CLASS_MABNI_CANDIDATE (HARF_ATF)
        بِ → CLOSED_CLASS_MABNI_CANDIDATE (HARF_JARR)
        ـهِمْ → ATTACHED_PRONOUN_CLOSED_CLASS
        كِتَابٍ → OPEN_CLASS_CORE_CANDIDATE (for root extraction)

    Args:
        functional_role_layer: U₅ layer object with functional role candidates
        registry: Optional MabniRegistry (uses default if None)

    Returns:
        MabniClosedClassResult with classifications and path blocking

    Forbidden:
        - Direct jump to Root (U₈)
        - Direct jump to Weight (U₉)
        - Direct jump to Meaning (U₁₅)
        - Root extraction for closed-class mabni units
    """
    # Use default registry if not provided
    if registry is None:
        registry = get_default_mabni_registry()

    # Validate input
    if not functional_role_layer.units:
        return MabniClosedClassResult(
            success=False,
            layer_object=None,
            failure_type=MabniClosedClassFailureType.NO_FUNCTIONAL_ROLE_UNITS,
            message="No functional role units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot classify mabni without functional role units")])
        )

    # Classify each functional role unit
    mabni_units = []
    all_residuals = []

    for func_role_unit in functional_role_layer.units:
        # Classify unit
        mabni_type, subtype, mabni_entry, lexicon_support, evidence_items = _classify_from_u5_roles(
            func_role_unit,
            registry
        )

        # Determine blocked paths
        blocked_paths = []
        if mabni_type in [
            MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
            MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
            MabniClosedClassType.DETACHED_PRONOUN_CLOSED_CLASS
        ]:
            # Closed-class units do NOT go to root/weight extraction
            blocked_paths = ["root_extraction", "weight_determination"]
            evidence_items.append("blocks_root_weight_path")
        else:
            # Open-class units MUST go to root/weight extraction
            evidence_items.append("requires_root_weight_path")

        # Build MabniClosedClassCandidate
        mabni_classification = MabniClosedClassCandidate(
            uid=str(uuid4()),
            mabni_type=mabni_type,
            subtype=subtype,
            lexicon_support=lexicon_support,
            evidence=tuple(evidence_items),
            source_u5_unit_id=func_role_unit.uid,
            mabni_entry=mabni_entry,
            residuals=frozenset(),
            rank=Rank.CANDIDATE
        )

        # Build MabniClosedClassUnit
        mabni_unit = MabniClosedClassUnit(
            uid=str(uuid4()),
            surface=func_role_unit.surface,
            source_functional_role_unit_id=func_role_unit.uid,
            trace_5=(functional_role_layer.uid,),
            mabni_classification=mabni_classification,
            blocked_paths=tuple(blocked_paths),
            evidence=tuple(evidence_items),
            residuals=func_role_unit.residuals,  # Preserve residuals from U₅
            rank=func_role_unit.rank
        )
        mabni_units.append(mabni_unit)
        all_residuals.extend(list(func_role_unit.residuals))

    # Build layer object
    layer_obj = MabniClosedClassLayerObject(
        uid=str(uuid4()),
        units=tuple(mabni_units),
        source_functional_role_layer_id=functional_role_layer.uid,
        trace_5=(functional_role_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=functional_role_layer.rank,  # Inherit rank from U₅
        proof=None
    )

    # Build proof
    proof = CPB6.build_proof(layer_obj)
    layer_obj = MabniClosedClassLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_functional_role_layer_id=layer_obj.source_functional_role_layer_id,
        trace_5=layer_obj.trace_5,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return MabniClosedClassResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"Mabni closed-class classifications complete: {len(mabni_units)} units processed",
        residuals=layer_obj.residuals
    )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Core types
    'MabniClosedClassType',
    'ClosedClassSubtype',

    # Structures
    'MabniClosedClassCandidate',
    'MabniClosedClassUnit',
    'MabniClosedClassLayerObject',
    'MabniClosedClassResult',

    # Failures
    'MabniClosedClassFailureType',

    # CPB
    'CPB6',

    # Operations
    'mabni_closed_class_6',
]
