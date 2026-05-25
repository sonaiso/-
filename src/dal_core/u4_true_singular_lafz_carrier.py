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

class LafzStatus(Enum):
    """
    Status of lafẓ singularity.

    This is STRUCTURAL classification, not semantic or functional.
    """
    TRUE_SINGULAR = "true_singular"                  # كِتَابٌ (true single lafẓ)
    ORTHOGRAPHIC_COMPOUND = "orthographic_compound"  # بِكِتَابِهِ (written as one, structurally multiple)
    COMPOSITE_STRUCTURE = "composite_structure"      # Multiple units forming structure
    NOT_STANDALONE = "not_standalone"                # ـهُ (requires host, not true lafẓ alone)
    AMBIGUOUS = "ambiguous"                          # Cannot determine


class LafzComposition(Enum):
    """How lafẓ is composed from boundary units."""
    SINGLE_UNIT = "single_unit"                      # One boundary unit = one lafẓ
    PREFIX_PLUS_CORE = "prefix_plus_core"            # بِـ + كِتَاب
    CORE_PLUS_SUFFIX = "core_plus_suffix"            # كِتَابُ + ـهُ
    FULL_COMPOSITE = "full_composite"                # وَ + بِـ + كِتَابِ + ـهِمْ
    UNCERTAIN = "uncertain"


class LafzEvidence(Enum):
    """Evidence for lafẓ determination."""
    BOUNDARY_EVIDENCE = "boundary_evidence"          # From U₃ boundary detection
    STANDALONE_TEST = "standalone_test"              # Can appear alone in utterance
    LEXICON_ATTESTATION = "lexicon_attestation"      # Found in lexicon as singular
    MORPHOLOGICAL_INTEGRITY = "morphological_integrity"  # Forms complete morphological unit
    COMPOSITIONAL_STRUCTURE = "compositional_structure"  # Multiple morphemes
    AMBIGUOUS_EVIDENCE = "ambiguous_evidence"


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
class TrueLafzCandidate:
    """
    Candidate for true singular lafẓ.

    This represents STRUCTURAL analysis of whether boundary units form
    a true singular lafẓ or composite structure.

    Forbidden fields:
        - root (that's U₈)
        - weight (that's U₉)
        - functional_role (that's U₅)
        - meaning (that's U₁₅)
    """
    uid: str
    surface: str                                     # Surface form
    status: LafzStatus                               # Singularity status
    composition: LafzComposition                     # How composed from units
    boundary_unit_ids: Tuple[str, ...]               # Which boundary units
    evidence: FrozenSet[LafzEvidence]                # Why this classification
    trace_3: str                                     # Trace to U₃ layer
    residuals: FrozenSet[Residual]
    rank: Rank

    def __post_init__(self):
        """Validate true lafẓ candidate."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("TrueLafzCandidate MUST NOT contain 'root' field (Axiom 4.4)")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("TrueLafzCandidate MUST NOT contain 'weight' field (Axiom 4.5)")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("TrueLafzCandidate MUST NOT contain 'meaning' field (Axiom 4.6)")

        # No functional_role field allowed
        if hasattr(self, 'functional_role'):
            raise ValueError("TrueLafzCandidate MUST NOT contain 'functional_role' field (Axiom 4.3)")


@dataclass(frozen=True)
class TrueLafzLayerObject:
    """
    U₄ layer object containing true lafẓ analysis.

    Represents classification of boundary units into true singular lafẓ vs. composites.
    """
    uid: str
    candidates: Tuple[TrueLafzCandidate, ...]        # Identified lafẓ candidates
    trace_3: str                                     # Trace to boundary layer
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
        if not layer_obj.candidates:
            return False

        if not layer_obj.trace_3:
            return False

        # Check no forbidden fields
        for candidate in layer_obj.candidates:
            if hasattr(candidate, 'root') or hasattr(candidate, 'weight') or hasattr(candidate, 'meaning'):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: TrueLafzLayerObject) -> ProofObject:
        """Build proof object for true lafẓ layer."""
        return make_proof_object(
            layer_name="U4_TRUE_SINGULAR_LAFZ",
            is_complete=CPB4.is_complete(layer_obj),
            evidence_items=[
                f"candidates_count={len(layer_obj.candidates)}",
                f"trace_3={layer_obj.trace_3[:50]}...",
                f"rank={layer_obj.rank.value}",
            ],
            allowed_next_gates=frozenset({"functional_role_gate"}),
            forbidden_gates=frozenset({
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
        )


# ============================================================================
# True Lafẓ Operations (Skeleton)
# ============================================================================

def true_lafz_4(boundary_layer: BoundaryLayerObject) -> TrueLafzResult:
    """
    Determine true singular lafẓ from boundary units.

    Critical Examples:
        كِتَابٌ → TRUE_SINGULAR (single core unit)
        بِكِتَابٍ → ORTHOGRAPHIC_COMPOUND (preposition + noun written together)
        وَ → TRUE_SINGULAR (standalone conjunction)
        ـهُمْ → NOT_STANDALONE (requires host)

    Args:
        boundary_layer: U₃ layer object with boundary units

    Returns:
        TrueLafzResult with classified lafẓ candidates

    Forbidden:
        - Direct jump to Root (U₈)
        - Direct jump to Weight (U₉)
        - Direct jump to Meaning (U₁₅)
    """
    # SKELETON IMPLEMENTATION
    # TODO: Implement full true lafẓ determination algorithm

    if not boundary_layer.units:
        return TrueLafzResult(
            success=False,
            layer_object=None,
            failure_type=LafzFailureType.NO_BOUNDARY_UNITS,
            message="No boundary units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot determine lafẓ without boundary units")])
        )

    # For now, create simple lafẓ candidates from boundary units
    # Real implementation would analyze composition, standalone tests, lexicon

    candidates = []
    for unit in boundary_layer.units:
        candidate = TrueLafzCandidate(
            uid=str(uuid4()),
            surface=unit.surface,
            status=LafzStatus.AMBIGUOUS,  # Needs real determination
            composition=LafzComposition.UNCERTAIN,
            boundary_unit_ids=(unit.uid,),
            evidence=frozenset([LafzEvidence.BOUNDARY_EVIDENCE]),
            trace_3=boundary_layer.uid,
            residuals=frozenset([make_warning("skeleton_implementation", "U₄ true lafẓ is skeleton only")]),
            rank=Rank.CANDIDATE
        )
        candidates.append(candidate)

    layer_obj = TrueLafzLayerObject(
        uid=str(uuid4()),
        candidates=tuple(candidates),
        trace_3=boundary_layer.uid,
        residuals=frozenset([make_warning("skeleton_implementation", "U₄ is skeleton implementation")]),
        rank=Rank.CANDIDATE,
        proof=None
    )

    # Build proof
    proof = CPB4.build_proof(layer_obj)
    layer_obj = TrueLafzLayerObject(
        uid=layer_obj.uid,
        candidates=layer_obj.candidates,
        trace_3=layer_obj.trace_3,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return TrueLafzResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message="True lafẓ determination complete (skeleton)",
        residuals=layer_obj.residuals
    )
