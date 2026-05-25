"""
U₄ True Singular Lafẓ Carrier (حامل اللفظ المفرد الحقيقي)

Domain: U₄ = TrueSingularLafẓCarrier
Purpose: Distinguish true singular lafẓ from orthographic compounds WITHOUT functional role
Transition: U₃ (BoundaryAndAttachment) → U₄ (TrueSingularLafẓ) → U₅ (FunctionalRole)

Critical Laws (Axioms):
    - Axiom 4.1: لفظ مفرد حقيقي ≠ تركيب كتابي (True lafẓ ≠ orthographic compound)
    - Axiom 4.2: اللفظ الحقيقي بعد فصل الحدود (True lafẓ after boundary separation)
    - Axiom 4.3: اللفظ ≠ الدور الوظيفي (Lafẓ ≠ functional role)
    - Axiom 4.4: لا جذر في U₄ (No root in U₄)
    - Axiom 4.5: لا وزن في U₄ (No weight in U₄)
    - Axiom 4.6: لا معنى في U₄ (No meaning in U₄)

Type System:
    TrueLafẓ ≠ Root
    TrueLafẓ ≠ Weight
    TrueLafẓ ≠ FunctionalRole
    TrueLafẓ ≠ Meaning
    TrueLafẓ ≠ Hukm

Architecture:
    U₃ (BoundaryLayerObject) → CPB₄ → U₄ (TrueLafẓLayerObject) → CPB₅ → FunctionalRole

Example Analysis:
    From U₃ boundary units [وَ, بِـ, كِتَاب, ـهِمْ]:
        - وَ → TRUE_LAFZ (standalone conjunction)
        - بِـكِتَابِـهِمْ → ORTHOGRAPHIC_COMPOUND (written together, but 3 units)

    Decision: Are they true singular lafẓ or composite?
        وَ = true_singular (standalone)
        بِـ = true_singular (can standalone as question marker)
        كِتَاب = true_singular (lexical core)
        ـهِمْ = NOT_STANDALONE (requires host)
        بِكِتَاب = COMPOSITE (preposition + noun)
        كِتَابِهِمْ = COMPOSITE (noun + pronoun)
        بِكِتَابِهِمْ = COMPOSITE (all three)

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
from dal_core.u3_boundary_attachment_carrier import (
    BoundaryUnit,
    BoundaryLayerObject
)


# ============================================================================
# Type System - Lafẓ Classification
# ============================================================================

class TrueLafzUnitType(Enum):
    """
    Classification of boundary units into lafẓ eligibility types.

    This is STRUCTURAL classification, not semantic or functional.
    U₄ determines eligibility to be a true singular lafẓ, NOT the meaning/role/root.
    """
    TRUE_SINGULAR_CORE_CANDIDATE = "true_singular_core_candidate"  # كِتَابٌ (eligible as true lafẓ)
    BOUND_PROCLITIC = "bound_proclitic"                            # وَ, فَ, بِـ, لِـ, سَـ
    ATTACHED_ENCLITIC = "attached_enclitic"                        # Generic enclitic
    ATTACHED_PRONOUN_CANDIDATE = "attached_pronoun_candidate"      # ـهُ, ـهَا, ـهِمْ
    ORTHOGRAPHIC_COMPOSITE = "orthographic_composite"              # Multiple units written together
    BLOCKED = "blocked"                                            # Cannot be determined


# ============================================================================
# Failure Types
# ============================================================================

class LafzFailureType(Enum):
    """Failure types for lafẓ determination."""
    NO_BOUNDARY_UNITS = "no_boundary_units"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    ORPHAN_ATTACHMENT = "orphan_attachment"


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class TrueLafzUnit:
    """
    U₄ classification of a boundary unit's lafẓ eligibility.

    This represents STRUCTURAL analysis: can this unit be a true singular lafẓ?
    NOT what the unit means, its role, root, or weight.

    Forbidden fields:
        - root (that's U₈)
        - weight (that's U₉)
        - functional_role (that's U₅)
        - meaning (that's U₁₅)
        - hukm (that's U₇+)
        - iʿrab (that's U₇+)
    """
    uid: str
    surface: str                                     # Orthographic surface from U₃
    unit_type: TrueLafzUnitType                      # Classification type
    source_boundary_unit_id: str                     # Trace to U₃ boundary unit
    trace_3: Tuple[str, ...]                         # Ordered trace to U₃
    evidence: Tuple[str, ...]                        # Why this classification
    residuals: FrozenSet[Residual]
    rank: Rank

    def __post_init__(self):
        """Validate true lafẓ unit."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'root' field (Axiom 4.4)")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'weight' field (Axiom 4.5)")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'meaning' field (Axiom 4.6)")

        # No functional_role field allowed
        if hasattr(self, 'functional_role'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'functional_role' field (Axiom 4.3)")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'hukm' field")

        # No iʿrab field allowed
        if hasattr(self, 'iʿrab') or hasattr(self, 'i3rab'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'iʿrab' field")


@dataclass(frozen=True)
class TrueLafzLayerObject:
    """
    U₄ layer object containing true lafẓ eligibility analysis.

    Represents classification of boundary units into lafẓ eligibility categories.
    """
    uid: str
    units: Tuple[TrueLafzUnit, ...]                  # Classified units
    source_boundary_layer_id: str                    # Trace to U₃ layer
    trace_3: Tuple[str, ...]                         # Ordered trace to U₃
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None


@dataclass(frozen=True)
class TrueLafzResult:
    """Result of true lafẓ determination."""
    success: bool
    layer_object: Optional[TrueLafzLayerObject]
    failure_type: Optional[LafzFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₄ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB4:
    """
    CPB₄: Completeness Predicate and Proof Builder for TrueSingularLafẓ layer.

    Guards:
        - Candidates identified
        - Boundary trace preserved
        - No forbidden fields (root, weight, meaning, functional_role)
        - Allowed next gate: U₅ FunctionalRole ONLY
    """

    @staticmethod
    def is_complete(layer_obj: TrueLafzLayerObject) -> bool:
        """Check if true lafẓ layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_boundary_layer_id:
            return False

        # Check no forbidden fields
        for unit in layer_obj.units:
            if (hasattr(unit, 'root') or hasattr(unit, 'weight') or
                hasattr(unit, 'meaning') or hasattr(unit, 'functional_role') or
                hasattr(unit, 'hukm') or hasattr(unit, 'iʿrab')):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: TrueLafzLayerObject) -> ProofObject:
        """Build proof object for true lafẓ layer."""
        return make_proof_object(
            claim="U₄ true singular lafẓ eligibility determination complete",
            scope="U4_TRUE_SINGULAR_LAFZ",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"trace_preserved={bool(layer_obj.source_boundary_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"functional_role_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
                "i3rab_certificate",
            }),
            limitations=frozenset([
                "no_root_extraction",
                "no_weight_determination",
                "no_meaning_assignment",
                "no_functional_role_commitment",
                "no_hukm_judgment",
                "no_i3rab_assignment",
            ]),
        )


# ============================================================================
# True Lafẓ Classification Logic
# ============================================================================

# Known proclitics (particles that attach before core)
KNOWN_PROCLITICS = frozenset([
    "وَ", "فَ",           # Conjunctions (standalone capable)
    "بِ", "بِـ",         # Preposition (requires host)
    "لِ", "لِـ",         # Preposition (requires host)
    "كَ", "كَـ",         # Comparison (requires host)
    "سَ", "سَـ",         # Future marker (requires host)
])

# Known pronoun enclitics (attach after core)
KNOWN_PRONOUN_ENCLITICS = frozenset([
    "ـهُ", "هُ",         # 3ms
    "ـهَا", "هَا",       # 3fs
    "ـهُمْ", "هُمْ",     # 3mp
    "ـهِمْ", "هِمْ",     # 3mp genitive
    "ـكَ", "كَ",         # 2ms
    "ـكِ", "كِ",         # 2fs
    "ـنَا", "نَا",       # 1p
])


def _classify_boundary_unit(unit: BoundaryUnit) -> TrueLafzUnitType:
    """
    Classify a boundary unit into lafẓ eligibility type.

    Decision tree:
    1. If unit.surface in KNOWN_PROCLITICS → BOUND_PROCLITIC
    2. If unit.surface in KNOWN_PRONOUN_ENCLITICS → ATTACHED_PRONOUN_CANDIDATE
    3. If unit_type == STANDALONE_CORE or CORE_CANDIDATE → TRUE_SINGULAR_CORE_CANDIDATE
    4. If unit_type == ATTACHED_ENCLITIC → ATTACHED_ENCLITIC (or PRONOUN if known)
    5. Else → TRUE_SINGULAR_CORE_CANDIDATE (conservative default)
    """
    from dal_core.u3_boundary_attachment_carrier import BoundaryUnitType

    surface = unit.surface

    # Check known proclitics
    if surface in KNOWN_PROCLITICS:
        return TrueLafzUnitType.BOUND_PROCLITIC

    # Check known pronoun enclitics
    if surface in KNOWN_PRONOUN_ENCLITICS:
        return TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE

    # Check boundary unit type from U₃
    if unit.unit_type == BoundaryUnitType.STANDALONE_CORE:
        return TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    if unit.unit_type == BoundaryUnitType.CORE_CANDIDATE:
        return TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    if unit.unit_type == BoundaryUnitType.STANDALONE_PROCLITIC:
        return TrueLafzUnitType.BOUND_PROCLITIC

    if unit.unit_type == BoundaryUnitType.ATTACHED_PROCLITIC:
        return TrueLafzUnitType.BOUND_PROCLITIC

    if unit.unit_type == BoundaryUnitType.ATTACHED_ENCLITIC:
        # Check if it's a known pronoun
        if surface in KNOWN_PRONOUN_ENCLITICS:
            return TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE
        else:
            return TrueLafzUnitType.ATTACHED_ENCLITIC

    if unit.unit_type == BoundaryUnitType.ORTHOGRAPHIC_COMPOUND:
        return TrueLafzUnitType.ORTHOGRAPHIC_COMPOSITE

    if unit.unit_type == BoundaryUnitType.UNRESOLVED:
        return TrueLafzUnitType.BLOCKED

    # Conservative default: treat as core candidate
    return TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE


# ============================================================================
# True Lafẓ Operations
# ============================================================================

def true_lafz_4(boundary_layer: BoundaryLayerObject) -> TrueLafzResult:
    """
    Determine true singular lafẓ eligibility from boundary units.

    Critical Examples:
        كَتَبَ → TRUE_SINGULAR_CORE_CANDIDATE (single core unit)
        بِكِتَابٍ → بِـ (BOUND_PROCLITIC) + كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
        وَبِكِتَابِهِمْ → وَ (BOUND_PROCLITIC) + بِـ (BOUND_PROCLITIC) + كِتَابِ (TRUE_SINGULAR_CORE_CANDIDATE) + ـهِمْ (ATTACHED_PRONOUN_CANDIDATE)
        ـهُمْ → ATTACHED_PRONOUN_CANDIDATE (not standalone)

    Args:
        boundary_layer: U₃ layer object with boundary units

    Returns:
        TrueLafzResult with classified lafẓ eligibility units

    Forbidden:
        - Direct jump to Root (U₈)
        - Direct jump to Weight (U₉)
        - Direct jump to Meaning (U₁₅)
        - Direct jump to FunctionalRole (U₅) without going through U₄
    """
    # Validate input
    if not boundary_layer.units:
        return TrueLafzResult(
            success=False,
            layer_object=None,
            failure_type=LafzFailureType.NO_BOUNDARY_UNITS,
            message="No boundary units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot determine lafẓ eligibility without boundary units")])
        )

    # Classify each boundary unit
    lafz_units = []
    all_residuals = []

    for unit in boundary_layer.units:
        # Determine unit type
        unit_type = _classify_boundary_unit(unit)

        # Build evidence
        evidence_items = [
            f"boundary_type={unit.unit_type.value}",
            f"surface={unit.surface}",
            f"classified_as={unit_type.value}",
        ]

        # Create TrueLafzUnit
        lafz_unit = TrueLafzUnit(
            uid=str(uuid4()),
            surface=unit.surface,
            unit_type=unit_type,
            source_boundary_unit_id=unit.uid,
            trace_3=(boundary_layer.uid,),
            evidence=tuple(evidence_items),
            residuals=unit.residuals,  # Preserve residuals from U₃
            rank=unit.rank
        )
        lafz_units.append(lafz_unit)
        all_residuals.extend(list(unit.residuals))

    # Build layer object
    layer_obj = TrueLafzLayerObject(
        uid=str(uuid4()),
        units=tuple(lafz_units),
        source_boundary_layer_id=boundary_layer.uid,
        trace_3=(boundary_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=boundary_layer.rank,  # Inherit rank from U₃
        proof=None
    )

    # Build proof
    proof = CPB4.build_proof(layer_obj)
    layer_obj = TrueLafzLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_boundary_layer_id=layer_obj.source_boundary_layer_id,
        trace_3=layer_obj.trace_3,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return TrueLafzResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"True lafẓ eligibility determined: {len(lafz_units)} units classified",
        residuals=layer_obj.residuals
    )
